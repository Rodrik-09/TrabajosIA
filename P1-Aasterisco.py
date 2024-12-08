import pygame

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("A")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
NARANJA = (255, 165, 0)
ROJO = (255, 0, 0)
AZUL = (0, 255, 255)
PURPURA = (128, 0, 128)

pygame.font.init()
FUENTE = pygame.font.SysFont("Arial", 16)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.vecinos = []
        self.g = float("inf")
        self.h = float("inf")
        self.f = float("inf")

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO
        self.g = float("inf")
        self.h = float("inf")
        self.f = float("inf")

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_abierto(self):
        self.color = AZUL

    def hacer_cerrado(self):
        self.color = NARANJA

    def hacer_camino(self):
        self.color = VERDE

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
        if self.color not in [BLANCO, NEGRO]:
            g = "0" if self.g == float("inf") else int(self.g)
            h = "0" if self.h == float("inf") else int(self.h)
            f = "0" if self.f == float("inf") else int(self.f)
            ventana.blit(FUENTE.render(f"G: {g}", True, NEGRO), (self.x + 5, self.y + 5))
            ventana.blit(FUENTE.render(f"H: {h}", True, NEGRO), (self.x + 5, self.y + 20))
            ventana.blit(FUENTE.render(f"F: {f}", True, NEGRO), (self.x + 5, self.y + 35))

    def actualizar_vecinos(self, grid, came_from):
        self.vecinos = []
        direcciones = [ # Movimientos
            (1, 0, 10), (-1, 0, 10), (0, 1, 10), (0, -1, 10),  # X, Y
            (1, 1, 14), (1, -1, 14), (-1, 1, 14), (-1, -1, 14) # Diagonales
        ]
        for d in direcciones:
            nueva_fila = self.fila + d[0]
            nueva_col = self.col + d[1]
            if 0 <= nueva_fila < self.total_filas and 0 <= nueva_col < self.total_filas:
                vecino = grid[nueva_fila][nueva_col]
                if not vecino.es_pared():
                    costo_g = self.g + d[2]
                    if costo_g < vecino.g:
                        vecino.g = costo_g
                        vecino.h = heuristica(vecino.get_pos(), fin.get_pos())
                        vecino.f = vecino.g + vecino.h
                        self.vecinos.append(vecino)

                        came_from[vecino] = self

def heuristica(p1, p2): # Manhattan
    x1, y1 = p1
    x2, y2 = p2
    return 10 * (abs(x1 - x2) + abs(y1 - y2))  

def reconstruir_camino(came_from, actual, dibujar):
    while actual in came_from:
        actual = came_from[actual]
        actual.hacer_camino()
        dibujar()
        pygame.time.delay(200)

def algoritmo_a_asterisco(dibujar, grid, inicio, fin):
    came_from = {}
    inicio.g = 0
    inicio.h = heuristica(inicio.get_pos(), fin.get_pos())
    inicio.f = inicio.g + inicio.h

    abiertos = [inicio]

    while abiertos:
        abiertos.sort(key=lambda nodo: nodo.f)
        nodo_actual = abiertos.pop(0)

        # Marcar nodo actual
        nodo_actual.color = ROJO
        dibujar()
        pygame.time.delay(200)  

        if nodo_actual == fin:
            fin.hacer_camino()
            reconstruir_camino(came_from, nodo_actual, dibujar)
            return True

        # Evaluar vecinos del nodo actual
        nodo_actual.actualizar_vecinos(grid, came_from)
        for vecino in nodo_actual.vecinos:
            if vecino == fin:
                came_from[vecino] = nodo_actual
                reconstruir_camino(came_from, vecino, dibujar)
                fin.hacer_camino()
                return True

            if vecino.color not in [NARANJA, AZUL, ROJO]:  
                vecino.hacer_abierto()  # Marcar vecino como evaluado
                if vecino not in abiertos:
                    abiertos.append(vecino)
                came_from[vecino] = nodo_actual

        nodo_actual.hacer_cerrado()
        dibujar()
        pygame.time.delay(200)  

    return False

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def main(ventana, ancho):
    global fin
    FILAS = 11
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    algoritmo_a_asterisco(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)

                if event.key == pygame.K_r:  # Reiniciar
                    inicio = None
                    fin = None
                    grid = crear_grid(FILAS, ancho)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)
