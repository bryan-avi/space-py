import pygame
import time
import random

# Cargar sprites de los enemigos
yellow = pygame.image.load("assets/yellow_enemy.png")
bala_enemiga = pygame.image.load("assets/shot.png")

#Numero maximo de disparos enemigos que puede haber en la pantalla
MAX_BALAS_ENEMIGAS = 2

# Definir la clase para el enemigo
class EnemigoYellow:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 0.4  # Velocidad de movimiento lateral
        self.direccion = 0.4  # 1 = derecha, -1 = izquierda
        self.vida = 1 #Vida del enemigo
        self.cooldown_disparo = random.uniform(1, 3) # Tiempo de espera entre disparo
        self.ultimo_disparo = 0 # Momento del ultimo disparo

    def mover(self):
        # Movimiento de lado a lado
        self.x += self.velocidad * self.direccion
        if self.x <= 0 or self.x >= 800 - yellow.get_width():
            self.direccion *= -1  # Cambia la dirección al llegar al borde
            self.y += 20  # Avanza hacia abajo al cambiar de dirección

    def dibujar(self, surface):
        surface.blit(yellow, (self.x, self.y))

    def get_rect(self): #Devuelve el rectangulo o la forma de colision del enemigp para que reciba daño
        return pygame.Rect(self.x, self.y, yellow.get_width(), yellow.get_height())
    
    def recibir_daño(self):
        self.vida -= 1
        return self.vida <= 0
    
    def puede_disparar(self, enemigos):
        #Esta funcion verifica si el enemigo no tiene otro delante en la misma columna
        for enemigo in enemigos:
            if enemigo != self and abs(enemigo.x - self.x) < yellow.get_width() and enemigo.y < self.y:
                return False
        return True
    
    def disparar(self, balas_enemigas, enemigos):
        #Solo dispara si el cooldown o tiempo ha pasado y no tiene ningun enemigo en frente
        if time.time() - self.ultimo_disparo >= self.cooldown_disparo and self.puede_disparar(enemigos):
            if len(balas_enemigas) < MAX_BALAS_ENEMIGAS:
                #Solo dispara si no se ha alcanzado el limite maximo de balas enemiga
                bala = BalaEnemiga(self.x + yellow.get_width() // 2 - bala_enemiga.get_width() // 2, self.y + yellow.get_height())
                balas_enemigas.append(bala)
                self.ultimo_disparo = time.time()

class BalaEnemiga:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 0.5

    def mover(self):
        self.y += self.velocidad #Mover la bala hacia abajo

    def dibujar_bala(self, surface):
        surface.blit(bala_enemiga, (self.x - bala_enemiga.get_width() // 2, self.y))  # Centrar la bala debajo del enemigo
    
    def get_rect(self):
        return pygame.Rect(self.x - bala_enemiga.get_width() // 2, self.y, bala_enemiga.get_width(), bala_enemiga.get_height())

# Crear una lista para almacenar los enemigos del nivel 1
def crear_enemigos_nivel_1():
    enemigos = []
    # Crear enemigos de tipo yellow en filas y columnas específicas
    for fila in range(3):  # 3 filas de enemigos
        for columna in range(10):  # 10 columnas de enemigos
            x = 50 + columna * 60  # Espacio entre enemigos
            y = 100 + fila * 50
            enemigo = EnemigoYellow(x, y)
            enemigos.append(enemigo)
    return enemigos

# Actualizar y dibujar enemigos en la pantalla
def actualizar_enemigos(enemigos, balas_enemigas, surface):
    for enemigo in enemigos:
        enemigo.mover()
        enemigo.dibujar(surface)
        enemigo.disparar(balas_enemigas, enemigos)

# Verificar condiciones de finalización del nivel
def nivel_terminado(enemigos):
    # Si todos los enemigos han sido eliminados, el nivel ha terminado
    return len(enemigos) == 0
