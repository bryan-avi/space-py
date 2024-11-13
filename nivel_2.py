import pygame 
import time
import random

yellow2 = pygame.image.load("assets/yellow_enemy_v2.png")
joker = pygame.image.load("assets/joke_enemy.png")
bala_enemiga = pygame.image.load("assets/shot_enemy.png")

MAX_BALAS_ENEMIGAS = 4

class BalaEnemiga:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 0.5

    def mover(self):
        self.y += self.velocidad  # Mover la bala hacia abajo

    def dibujar_bala(self, surface):
        surface.blit(bala_enemiga, (self.x - bala_enemiga.get_width() // 2, self.y))  # Centrar la bala debajo del enemigo
    
    def get_rect(self):
        return pygame.Rect(self.x - bala_enemiga.get_width() // 2, self.y, bala_enemiga.get_width(), bala_enemiga.get_height())

class Enemigo_Yellow_2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 0.4
        self.direccion = 0.4
        self.vida = 2
        self.cooldown_disparo = random.uniform(1, 3)
        self.ultimo_disparo = 0

    def mover(self):
        self.x += self.velocidad * self.direccion
        if self.x <= 0 or self.x >= 800 - yellow2.get_width():
            self.direccion *= -1
            self.y += 20
    
    def dibujar(self, surface):
        surface.blit(yellow2, (self.x, self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, yellow2.get_width(), yellow2.get_height())
    
    def recibir_daño(self):
        self.vida -= 1
        return self.vida <= 0

    def puede_disparar(self, enemigos):
        for enemigo in enemigos:
            if enemigo != self and abs(enemigo.x - self.x) < yellow2.get_width() and enemigo.y < self.y:
                return False
        return True

    def disparar(self, balas_enemigas, enemigos):
        if time.time() - self.ultimo_disparo >= self.cooldown_disparo and self.puede_disparar(enemigos):
            if len(balas_enemigas) < MAX_BALAS_ENEMIGAS:
                bala = BalaEnemiga(self.x + yellow2.get_width() // 2, self.y + yellow2.get_height())
                balas_enemigas.append(bala)
                self.ultimo_disparo = time.time()
    
class EnemigoJoker:
    def __init__(self):
        self.x = random.randint(100, 700)  # Posición inicial aleatoria en el rango visible
        self.y = random.randint(50, 200)  # Posición aleatoria dentro de la pantalla
        self.vida = 3
        self.cooldown_disparo = random.uniform(1, 2)  # El tiempo de espera entre disparos
        self.ultimo_disparo = 0  # Marca de tiempo del último disparo
        self.ultimo_telentransporte = time.time()

    def mover(self):
        # El Joker se "teletransporta" a una nueva posición aleatoria después de cierto tiempo
        if time.time() - self.ultimo_telentransporte >= 2:  # Teletransportarse cada 5 segundos
            self.x = random.randint(100, 700)
            self.y = random.randint(50, 200)
            self.ultimo_telentransporte = time.time()  # Actualizar la marca de tiempo

    def disparar(self, balas_enemigas, enemigos):
        # Disparar una bala si ha pasado el tiempo de cooldown
        if time.time() - self.ultimo_disparo >= self.cooldown_disparo:
            # Crear una nueva bala enemiga en la posición del Joker
            bala = BalaEnemiga(self.x + joker.get_width() // 2, self.y + joker.get_height())
            balas_enemigas.append(bala)
            self.ultimo_disparo = time.time()  # Actualizar la marca de tiempo

    def dibujar(self, surface):
        # Dibujar la imagen del Joker en la pantalla
        surface.blit(joker, (self.x, self.y))

    def get_rect(self):
        # Obtener el rectángulo de la imagen para la colisión
        return pygame.Rect(self.x, self.y, joker.get_width(), joker.get_height())
    
    def recibir_daño(self):
        self.vida -= 1
        return self.vida <= 0

# Crear una lista para los enemigos del nivel 2
def crear_enemigos_nivel_2():
    enemigos = []
    for fila in range(2):  # Menos filas, pero más resistentes
        for columna in range(8):  # Menos columnas, ajustando el espacio
            x = 50 + columna * 80
            y = 100 + fila * 60
            enemigo = Enemigo_Yellow_2(x, y)
            enemigos.append(enemigo)
    
    joker = EnemigoJoker()
    enemigos.append(joker)

    return enemigos

# Actualizar enemigos 
def actualizar_enemigos_nivel_2(enemigos, balas_enemigas, surface):
    for enemigo in enemigos:
        enemigo.mover()
        enemigo.dibujar(surface)
        enemigo.disparar(balas_enemigas, enemigos)
