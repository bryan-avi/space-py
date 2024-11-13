import pygame
import sys
import time
import nivel_1
import nivel_2
import game_over  # Importa el módulo de Game Over

pygame.init()
clock = pygame.time.Clock()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Space Invaders - Juego")

# Variables de todos los elementos que estarán en el juego
fondo_juego = pygame.image.load("assets/background_game.png") 
nave_jugador = pygame.image.load("assets/sprites_player/player.png")
yellow = pygame.image.load("assets/yellow_enemy.png")
yellow2 = pygame.image.load("assets/yellow_enemy_v2.png")
red = pygame.image.load("assets/red_enemy.png")
boss_yellow = pygame.image.load("assets/boss_yellow.png")
bala_unidad = pygame.image.load("assets/shot.png")

# Clase de la bala que maneja tanto su velocidad como su movimiento, su sprite/dibujo y su colisión para dañar enemigos
class Bala:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.velocidad = 2  # Velocidad de la bala
    
    def mover(self):
        self.y -= self.velocidad  # Mover la bala hacia arriba
    
    def dibujar_bala(self, surface):
        surface.blit(bala_unidad, (self.x + (nave_jugador.get_width() // 2) - bala_unidad.get_width() // 2, self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x + (nave_jugador.get_width() // 2) - bala_unidad.get_width() // 2, self.y, bala_unidad.get_width(), bala_unidad.get_height())


# Variables del juego
def reiniciar_juego():
    global nave_x, nave_y, vida_jugador, balas, enemigos, balas_enemigas, fondo_y, ultimo_disparo
    nave_x = (screen_width - nave_jugador.get_width()) // 2
    nave_y = screen_height - nave_jugador.get_height() - 50
    vida_jugador = 10
    balas = []
    balas_enemigas = []
    fondo_y = 0
    ultimo_disparo = 0
    enemigos = nivel_1.crear_enemigos_nivel_1()

# Inicialización de variables
reiniciar_juego()
velocidad_fondo = 0.7
velocidad_jugador = 0.8
cooldown_disparo = 0.8

# Detecta colisiones entre balas y enemigos
def detectar_colisiones():
    global enemigos, balas
    for bala in balas[:]:
        for enemigo in enemigos[:]:
            if bala.get_rect().colliderect(enemigo.get_rect()):
                balas.remove(bala)
                if enemigo.recibir_daño():
                    enemigos.remove(enemigo)
                break

# Detecta colisiones entre balas enemigas y el jugador
def colision_jugador_balas_enemigas():
    global vida_jugador, balas_enemigas
    jugador_rect = pygame.Rect(nave_x, nave_y, nave_jugador.get_width(), nave_jugador.get_height())
    for bala in balas_enemigas[:]:
        if jugador_rect.colliderect(bala.get_rect()):
            vida_jugador -= 1
            balas_enemigas.remove(bala)
            if vida_jugador <= 0:
                game_over.game_over_screen()  # Llama a la pantalla de Game Over
                return  # Salir de la función para detener el juego

# Dibuja todos los elementos en la pantalla del juego
def dibujar_pantalla_juego():
    global fondo_y
    
    # Mueve el fondo
    fondo_y += velocidad_fondo
    if fondo_y >= screen_height:
        fondo_y = 0
    
    screen.blit(fondo_juego, (0, fondo_y))  # Dibujar el fondo en la nueva posición
    screen.blit(fondo_juego, (0, fondo_y - screen_height))  # Para cubrir toda la pantalla
    
    screen.blit(nave_jugador, (nave_x, nave_y))  # Nave del jugador
    
    for bala in balas:
        bala.dibujar_bala(screen)
    
    for bala_enemiga in balas_enemigas:
        bala_enemiga.dibujar_bala(screen)

    nivel_1.actualizar_enemigos(enemigos, balas_enemigas, screen)

# Ciclo principal del juego
def main():
    global nave_x, ultimo_disparo, enemigos
    enemigos = nivel_1.crear_enemigos_nivel_1()
    running = True
    nivel_actual = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Código de las teclas que disparan la bala
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                if time.time() - ultimo_disparo >= cooldown_disparo:
                    balas.append(Bala(nave_x, nave_y))
                    ultimo_disparo = time.time()

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and nave_x > 0:
            nave_x -= velocidad_jugador
        if keys[pygame.K_RIGHT] and nave_x < screen_width - nave_jugador.get_width():
            nave_x += velocidad_jugador

        # Movimiento y eliminación de balas
        for bala in balas[:]:
            bala.mover()
            if bala.y < 0:
                balas.remove(bala)
        
        for bala_enemiga in balas_enemigas[:]:
            bala_enemiga.mover()
            if bala_enemiga.y > screen_height:
                balas_enemigas.remove(bala_enemiga)
        
        # Detección de colisiones
        detectar_colisiones()
        colision_jugador_balas_enemigas()

        # Si estamos en el nivel 2, actualizamos los enemigos y el joker
        if nivel_actual == 2:
            for enemigo in enemigos:
                enemigo.mover()
                enemigo.dibujar(screen)
                enemigo.disparar(balas_enemigas, enemigos)
        
        # Si estamos en el nivel 1, simplemente actualizamos los enemigos
        if nivel_actual == 1:
            for enemigo in enemigos:
                enemigo.mover()
                enemigo.dibujar(screen)
                enemigo.disparar(balas_enemigas, enemigos)

        for enemigo in enemigos:
            enemigo.disparar(balas_enemigas, enemigos)

        dibujar_pantalla_juego()
        pygame.display.update()
        clock.tick(360)

        if nivel_1.nivel_terminado(enemigos) and nivel_actual == 1:
            print("Cargando nivel 2")
            pygame.display.update()
            time.sleep(3)
            enemigos = nivel_2.crear_enemigos_nivel_2()
            nivel_actual = 2

if __name__ == "__main__":
    main()
