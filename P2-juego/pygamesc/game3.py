
import pygame
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None

# Variables de salto
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False

# Lista para guardar los datos de velocidad, distancia y salto
datos_modelo = []

# Variables del modelo
clf = None  # Clasificador del árbol de decisión

# Rutas completas de las imágenes
jugador_frames = [
    pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-juego/pygamesc/assets/sprites/mono_frame_1.png'),
    pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-juego/pygamesc/assets/sprites/mono_frame_2.png'),
    pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-juego/pygamesc/assets/sprites/mono_frame_3.png'),
    pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-juego/pygamesc/assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-juego/pygamesc/assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-juego/pygamesc/assets/game/fondo2.png')
nave_img = pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-juego/pygamesc/assets/game/ufo.png')

# Escalar la imagen de fondo
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear rectángulos
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)

# Variables de animación del jugador
current_frame = 0
frame_speed = 10
frame_count = 0

# Variables de la bala
velocidad_bala = -10
bala_disparada = False

# Fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50
    bala_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura
        salto_altura -= gravedad
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15
            en_suelo = True

# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    if fondo_x1 <= -w:
        fondo_x1 = w
    if fondo_x2 <= -w:
        fondo_x2 = w

    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        if not modo_auto:
            entrenar_modelo()
        reiniciar_juego()

# Función para guardar datos
def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))


def pausa_juego():
    global pausa, modo_auto, menu_activo

    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
        
        # Mostrar menú de pausa
        while pausa:
            pantalla.fill(NEGRO)
            texto_continuar = fuente.render("Presiona 'C' para continuar", True, BLANCO)
            texto_menu = fuente.render("Presiona 'M' para volver al menú principal", True, BLANCO)
            pantalla.blit(texto_continuar, (w // 4, h // 2 - 30))
            pantalla.blit(texto_menu, (w // 4, h // 2 + 10))
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_c:  # Continuar
                        pausa = False
                    elif evento.key == pygame.K_m:  # Volver al menú principal
                        if not modo_auto:  # Entrenar el modelo si no está en modo automático
                            entrenar_modelo_arbol()
                        reiniciar_juego()
                        pausa = not pausa
                        return


# Función para entrenar el modelo
def entrenar_modelo_arbol():
    global clf, datos_modelo
    if len(datos_modelo) > 0:
        df = pd.DataFrame(datos_modelo, columns=["velocidad_bala", "distancia", "salto"])
        X = df[["velocidad_bala", "distancia"]]
        y = df["salto"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        clf = DecisionTreeClassifier()
        clf.fit(X_train, y_train)
        print("Modelo entrenado con éxito.")

# Función de modo automático
def modo_juego_automatico_arbol():
    global clf, jugador, bala, velocidad_bala, salto, en_suelo
    print('sixd')
    if clf is not None:
        distancia = abs(jugador.x - bala.x)
        prediccion = clf.predict([[velocidad_bala, distancia]])[0]
        if prediccion == 1 and en_suelo:
            salto = True
            en_suelo = False

# Función para reiniciar el juego
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    print("Regresando al menú...")
    menu_activo = True
    mostrar_menu()
    jugador.x, jugador.y = 50, h - 100
    bala.x = w - 50
    nave.x, nave.y = w - 100, h - 100
    bala_disparada = False
    salto = False
    en_suelo = True

# Función para mostrar el menú
def mostrar_menu():
    global menu_activo, modo_auto
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, 'M' para Manual, o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 4, h // 2))
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    modo_auto = True
                    menu_activo = False
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

# Función principal
def main():
    global salto, en_suelo, bala_disparada

    reloj = pygame.time.Clock()
    mostrar_menu()
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa and not modo_auto:
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:
                    pausa_juego()
                if evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

        if not pausa:
            if modo_auto:
                modo_juego_automatico_arbol()
                if salto:
                    manejar_salto()
            else:
                guardar_datos()
                if salto:
                    manejar_salto()
            if not bala_disparada:
                disparar_bala()
            update()

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
