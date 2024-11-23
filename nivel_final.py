import pygame
import time
import random


red = pygame.image.load("assets/red_enemy.png")
jefe_imagen = pygame.image.load("assets/boss_2.png")
bala_enemiga = pygame.image.load("assets/shot_enemy.png")

MAX_BALAS_ENEMIGAS = 6


class BalaEnemiga:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 0.7

    def mover(self):
        self.y += self.velocidad
    
    def dibujar_bala(self, surface):
        surface.blit(bala_enemiga, (self.x - bala_enemiga.get_width() // 2, self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x - bala_enemiga.get_width() // 2, self.y, bala_enemiga.get_width(), bala_enemiga.get_height())
    
class Enemigo_Red:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 0.1 #Mas lento que niveles anteriores
        self.direccion = 0.2
        self.vida = 3
        self.cooldown_disparo = random.uniform(0.8, 1.5)
        self.ultimo_disparo = 0
        self.puntos = 50
    
    def mover(self):
        self.x += self.velocidad * self.direccion
        if self.x <= 0 or self.x >= 800 - red.get_width():
            self.direccion *= -1
            self.y += 20

    def dibujar(self, surface):
        surface.blit(red, (self.x, self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, red.get_width(), red.get_height())
    
    def recibir_daño(self):
        self.vida -= 1
        return self.vida <= 0

    def puede_disparar(self, enemigos):
        for enemigo in enemigos:
            if enemigo != self and abs(enemigo.x - self.x) < red.get_width() and enemigo.y < self.y:
                return False
        return True

    def disparar(self, balas_enemigas, enemigos):
        if time.time() - self.ultimo_disparo >= self.cooldown_disparo and self.puede_disparar(enemigos):
            if len(balas_enemigas) < MAX_BALAS_ENEMIGAS:
                bala = BalaEnemiga(self.x + red.get_width() // 2, self.y + red.get_height())
                balas_enemigas.append(bala)
                self.ultimo_disparo = time.time()
    

class BossFinal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vida = 20  # Vida alta para el jefe
        self.ultimo_disparo = 0
        self.cooldown_rafaga = 1.5  # Tiempo entre ráfagas en segundos
        self.rafaga_actual = 0 # Contador de balas en la ráfaga
        self.velocidad = 0.001
        self.puntos = 100

    def mover(self):
        self.y += self.velocidad

    def dibujar(self, surface):
        surface.blit(jefe_imagen, (self.x, self.y))
    
    def disparar(self, balas_enemigas, enemigos):
        pass

    def disparar_rafaga(self, balas_enemigas):
        if self.rafaga_actual < 3:
            if time.time() - self.ultimo_disparo >= 0.5:
                bala = BalaEnemiga(self.x + jefe_imagen.get_width() // 2, self.y + jefe_imagen.get_height())
                balas_enemigas.append(bala)
                self.rafaga_actual += 1
                self.ultimo_disparo = time.time()
        elif time.time() - self.ultimo_disparo >= self.cooldown_rafaga:
            self.rafaga_actual = 0

    def recibir_daño(self):
        self.vida -= 1
        return self.vida <= 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, jefe_imagen.get_width(), jefe_imagen.get_height())

def crear_enemigos_nivel_3():
    enemigos = []
    
    # Posición del jefe
    boss_x = (800 - jefe_imagen.get_width()) // 2
    boss_y = 10
    boss = BossFinal(boss_x, boss_y)
    enemigos.append(boss)

    # Calcular la posición de los enemigos rojos debajo del jefe
    pos_enemigos_y = boss_y + jefe_imagen.get_height()  # Colocar enemigos justo debajo del jefe

    # Enemigos en el lado izquierdo
    for fila in range(2):  # Dos filas de enemigos
        for columna in range(3):  # Cuatro enemigos por fila
            x = 50 + columna * 80  # Enemigos en el lado izquierdo
            y = pos_enemigos_y + fila * 60  # Coloca los enemigos debajo del jefe
            enemigo = Enemigo_Red(x, y)
            enemigos.append(enemigo)

    # Enemigos en el lado derecho
    for fila in range(2):  # Dos filas de enemigos
        for columna in range(3):  # Cuatro enemigos por fila
            x = 400 + columna * 80  # Enemigos en el lado derecho
            y = pos_enemigos_y + fila * 60  # Coloca los enemigos debajo del jefe
            enemigo = Enemigo_Red(x, y)
            enemigos.append(enemigo)

    return enemigos

def actualizar_enemigos_nivel_3(enemigos, balas_enemigas, surface):
    for enemigo in enemigos:
        enemigo.mover()
        enemigo.dibujar(surface)
        enemigo.disparar(balas_enemigas, enemigos)
        if isinstance(enemigo, BossFinal):
            enemigo.disparar(balas_enemigas, enemigos)
            enemigo.disparar_rafaga(balas_enemigas)

# Verificar condiciones de finalización del nivel
def nivel_terminado(enemigos):
    # Si todos los enemigos han sido eliminados, el nivel ha terminado
    return len(enemigos) == 0
