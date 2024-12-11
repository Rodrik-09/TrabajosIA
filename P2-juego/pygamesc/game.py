import pygame
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

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

# Lista para guardar los datos de velocidad, distancia y salto
datos_modelo = []

# Variables del modelo
clf_arbol = None  # Clasificador del árbol de decisión
model_nn = None   # Modelo de red neuronal
scaler = None     # Escalador para la red neuronal

# Rutas completas de las imágenes (ajusta las rutas según tu sistema)
jugador_frames = [
    pygame.image.load('ruta_a_sprite_1.png'),
    pygame.image.load('ruta_a_sprite_2.png'),
    pygame.image.load('ruta_a_sprite_3.png'),
    pygame.image.load('ruta_a_sprite_4.png')
]
bala_img = pygame.image.load('ruta_a_bala.png')
fondo_img = pygame.image.load('ruta_a_fondo.png')
nave_img = pygame.image.load('ruta_a_nave.png')

# Escalar la imagen de fondo
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear rectángulos para el jugador y objetos
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

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-9, -5)
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

# Función para actualizar el juego cada frame
def update():
    global bala, velocidad_bala, current_frame, frame_count

    # Animación del jugador 
    frame_count += 1
    
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0
    
    pantalla.fill(NEGRO)
    pantalla.blit(fondo_img, (0,0))
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala 
    if bala_disparada:
        bala.x += velocidad_bala
        
        if bala.x < 0:
            reset_bala()
        
        pantalla.blit(bala_img, (bala.x, bala.y))

# Función para guardar datos para entrenamiento 
def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0
    
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))

# Función para pausar el juego 
def pausa_juego():
    global pausa
    
    pausa = not pausa
    
    if pausa:
        print("Juego pausado. Datos registrados:", datos_modelo)

# Función para entrenar el modelo de árbol de decisión 
def entrenar_modelo_arbol():
    global clf_arbol
    
    if len(datos_modelo) > 0:
        df = pd.DataFrame(datos_modelo, columns=["velocidad_bala", "distancia", "salto"])
        
        X = df[["velocidad_bala", "distancia"]]
        y = df["salto"]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        clf_arbol = DecisionTreeClassifier()
        clf_arbol.fit(X_train.values.reshape(-1,2), y_train.values)

        print("Modelo de árbol de decisión entrenado.")

# Función para entrenar la red neuronal 
def entrenar_modelo_red():
    global model_nn
    
    if len(datos_modelo) > 0:
        df = pd.DataFrame(datos_modelo, columns=["velocidad_bala", "distancia", "salto"])
        
        X = df[["velocidad_bala", "distancia"]]
        y = df["salto"]
        
        # Escalar características 
        scaler.fit(X)
        X_scaled = scaler.transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y.values.reshape(-1), test_size=0.2)

        model_nn = Sequential([
            Dense(16, input_dim=2, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        
        model_nn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        
        model_nn.fit(X_train.reshape(-1), y_train.reshape(-1), epochs=30)

        loss, accuracy = model_nn.evaluate(X_test.reshape(-1), y_test.reshape(-1))
        print(f"Precisión en el conjunto de prueba: {accuracy:.2f}")
        
        datos_modelo.clear() # Limpiar después de entrenar

# Función principal para ejecutar el juego 
def main():
    global salto
    
    reloj = pygame.time.Clock()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:
                    salto = True
                    en_suelo=False
                
                if evento.key == pygame.K_p: # Pausar el juego 
                    pausa_juego()
                
                if evento.key == pygame.K_t: # Entrenar árbol de decisión 
                    entrenar_modelo_arbol()
                
                if evento.key == pygame.K_r: # Entrenar red neuronal 
                    entrenar_modelo_red()
                
                if evento.key == pygame.K_q: # Salir del juego 
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    return
        
        if not pausa:
            guardar_datos() # Guardar datos cada frame 
            update() # Actualizar estado del juego 
        
            if salto:
                manejar_salto()

            if not bala_disparada:
                disparar_bala()

            pygame.display.flip()
            reloj.tick(30) # Mantener tasa de frames 

if __name__ == "__main__":
    main()