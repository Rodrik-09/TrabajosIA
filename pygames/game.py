import os
import pygame
import random
import matplotlib.pyplot as plt
import csv
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
menu = None

# Variables de salto
salto = False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-Juego/assets/sprites/mono_frame_1.png'),
    pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-Juego/assets/sprites/mono_frame_2.png'),
    pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-Juego/assets/sprites/mono_frame_3.png'),
    pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-Juego/assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-Juego/assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-Juego/assets/game/fondo2.png')
nave_img = pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-Juego/assets/game/ufo.png')
menu_img = pygame.image.load('C:/Users/rbece/Documents/iaP/TrabajosIA/P2-Juego/assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -10  # Velocidad de la bala hacia la izquierda
bala_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  # Restablecer la velocidad de salto
            en_suelo = True

# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        guardar_en_csv()
        reiniciar_juego()  # Terminar el juego y mostrar el menú
        

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    # Guardar velocidad de la bala, distancia al jugador y si saltó o no
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))

# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, 'M' para Manual, 'G' para Gráfica o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 6, h // 2))
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
                    file_path = 'datos_modelo.csv'
                    dataset = pd.read_csv(file_path)
                    X = dataset.iloc[:, :2]  # Las dos primeras columnas son las características
                    y = dataset.iloc[:, 2]   # La tercera columna es la etiqueta

                    # Dividir los datos en conjunto de entrenamiento y prueba
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                    # Crear el clasificador de Árbol de Decisión
                    clf = DecisionTreeClassifier()

                    # Entrenar el modelo
                    clf.fit(X_train, y_train)

                    # Exportar el árbol de decisión en formato DOT para su visualización
                    dot_data = export_graphviz(clf, out_file=None, 
                                            feature_names=['Feature 1', 'Feature 2'],  
                                            class_names=['Clase 0', 'Clase 1'],  
                                            filled=True, rounded=True,  
                                            special_characters=True)  

                    # Crear el gráfico con graphviz
                    graph = graphviz.Source(dot_data)

                    # Mostrar el gráfico
                    graph.view()
                    
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()
                elif evento.key == pygame.K_g:
                    mostrar_grafica()

def mostrar_grafica():
    if datos_modelo:
        velocidades, distancias, saltos = zip(*datos_modelo)  # Separar los datos en listas
        plt.figure()
        plt.scatter(distancias, velocidades, c=saltos, cmap='viridis', marker='o')
        plt.colorbar(label="Salto (0=No, 1=Sí)")
        plt.xlabel("Distancia al jugador")
        plt.ylabel("Velocidad de la bala")
        plt.title("Gráfica de Distancia vs Velocidad con Salto")
        plt.show()
    else:
        print("No hay datos para mostrar en la gráfica.")
# Función para reiniciar el juego tras la colisión

def guardar_en_csv(nombre_archivo="datos_modelo.csv"):
    ruta_proyecto = os.path.dirname(os.path.abspath(__file__))  # Ruta absoluta del archivo actual
    ruta_archivo = os.path.join(ruta_proyecto, nombre_archivo)  # Combinar con el nombre del archivo

    # Guardar los datos en la ruta especificada
    with open(ruta_archivo, mode='w', newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerows(datos_modelo)  # Escribir los datos
    print(f"Datos guardados en {ruta_archivo}")
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
    # Mostrar los datos recopilados hasta el momento
    print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo
modelo_entrenado = None  # Variable para guardar el modelo
columnas_caracteristicas = ['velocidad_bala', 'distancia']  # Nombres de las características

# Función para cargar el modelo desde los datos manuales
def entrenar_modelo():
    global modelo_entrenado
    file_path = 'C:/Users/rbece/Documents/iaP/TrabajosIA/P2-Juego/datos_modelo.csv'
    try:
        dataset = pd.read_csv(file_path)
        if dataset.empty:
            raise ValueError("El archivo está vacío. Recolecta datos en el modo manual antes de entrenar el modelo.")
        X = dataset.iloc[:, :2]  # Las dos primeras columnas son las características
        y = dataset.iloc[:, 2]   # La tercera columna es la etiqueta (salto)

        # Dividir los datos en conjunto de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Crear el clasificador de Árbol de Decisión
        modelo_entrenado = DecisionTreeClassifier()

        # Entrenar el modelo
        modelo_entrenado.fit(X_train, y_train)
        print("Modelo entrenado exitosamente.")
    except FileNotFoundError:
        print(f"No se encontró el archivo {file_path}. Entrena el modelo manualmente antes de usar el modo automático.")
        pygame.quit()
        exit()

# Función para que el juego use el modelo para jugar automáticamente
def jugar_automatico():
    global jugador, salto, en_suelo, bala, modelo_entrenado

    if modelo_entrenado:
        # Calcular las características actuales
        distancia = abs(jugador.x - bala.x)
        caracteristicas = [[velocidad_bala, distancia]]

        # Hacer una predicción
        prediccion = modelo_entrenado.predict(caracteristicas)

        # Si la predicción es 1 (saltar), iniciar el salto
        if prediccion[0] == 1 and en_suelo:
            salto = True
            en_suelo = False
    else:
        print("El modelo no está entrenado. Cambia al modo manual para recolectar datos.")

# Modificar el bucle principal para integrar el modo automático
def main():
    global salto, en_suelo, bala_disparada

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa and not modo_auto:  # Salto manual
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:  # Pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_q:  # Terminar el juego
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    guardar_en_csv()
                    pygame.quit()
                    exit()

        if not pausa:
            if modo_auto:
                # Usar el modelo para jugar automáticamente
                jugar_automatico()
            else:
                # Modo manual: controlar el salto
                if salto:
                    manejar_salto()
                guardar_datos()

            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(30)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    # Entrenar el modelo antes de iniciar el juego
    main()