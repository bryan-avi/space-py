import pygame
import sys
import time
import nivel_1

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Space Invaders - Juego")

#Variables de todos los elementos que estaran en el juego
fondo_juego = pygame.image.load("assets/background_game.png") 
nave_jugador = pygame.image.load("assets/sprites_player/player.png")
yellow = pygame.image.load("assets/yellow_enemy.png")
yellow2 = pygame.image.load("assets/yellow_enemy_v2.png")
red = pygame.image.load("assets/red_enemy.png")
joke = pygame.image.load("assets/joke_enemy.png")
boss_yellow = pygame.image.load("assets/boss_yellow.png")
bala_unidad = pygame.image.load("assets/shot.png")

#Clase de la bala que maneja tanto su velocidad como su movimiento, su sprite/dibujo y su colision para dañar enemigos
class Bala:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.velocidad = 2 #Velocidad de la bala
    
    def mover(self):
        self.y -= self.velocidad #Mover la bala hacia arriba
    
    def dibujar_bala(self, surface):
        surface.blit(bala_unidad, (self.x + (nave_jugador.get_width() // 2) - bala_unidad.get_width() // 2, self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x + (nave_jugador.get_width() // 2) - bala_unidad.get_width() // 2, self.y, bala_unidad.get_width(), bala_unidad.get_height())

#Parte del codigo que se asegura de iniciar algunas variables necesarias en el juego
nave_x = (screen_width - nave_jugador.get_width()) // 2
nave_y = screen_height - nave_jugador.get_height() - 50
fondo_y = 0
velocidad_fondo = 0.7
velocidad_jugador = 0.8 #Velocidad base de la nave del jugador
balas = [] #Lista que almacena las balas
balas_enemigas = []
cooldown_disparo = 0.8 #Cantidad de tiempo que el jugador tiene que esperar para volver a disparar
ultimo_disparo = 0 #Tiempo del ultimo disparo
vida_jugador = 3

#Crea los enemigos para el nivel 1
enemigos = nivel_1.crear_enemigos_nivel_1()

def detectar_colisiones():
    global enemigos, balas
    for bala in balas[:]:
        for enemigo in enemigos[:]:
            if bala.get_rect().colliderect(enemigo.get_rect()):
                balas.remove(bala)
                if enemigo.recibir_daño():
                    enemigos.remove(enemigo)
                break

def colision_jugador_balas_enemigas():
    global vida_jugador, balas_enemigas
    jugador_rect = pygame.Rect(nave_x, nave_y, nave_jugador.get_width(), nave_jugador.get_height())
    for bala in balas_enemigas[:]:
        if jugador_rect.colliderect(bala.get_rect()):
            vida_jugador -= 1
            balas_enemigas.remove(bala)
            if vida_jugador <= 0:
                print("Game Over")
                pygame.quit()
                sys.exit()
#enemigos = [
    #F1
    #(yellow, 350, 225), (yellow2, 400, 225), (yellow, 450, 225), (yellow2, 500, 225), (yellow, 550, 225),
    #(yellow, 600, 225), (yellow2, 650, 225), (yellow, 700, 225), 
    #F2
    #(yellow2, 50, 170), (yellow, 100, 170), (red, 159, 170), (yellow2, 250, 170), (yellow, 300, 170),
    #(red, 359, 170), (yellow, 450, 170), (yellow2, 500, 170), (red, 559, 170), (yellow2, 650, 170), (yellow, 700, 170), 
    #F3
    #(yellow2, 50, 115), (yellow, 100, 115), (red, 159, 115), (yellow2, 250, 115), (joke, 295, 115),
    #(red, 359, 115), (joke, 435, 115), (yellow2, 500, 115), (red, 559, 115), (yellow2, 650, 115), (yellow, 700, 115), 
    #F4
    #(boss_yellow, 335, 25)
#]

#Codigo que dibuja y ordena todo lo que el jugador ve dentro del juego como el fondo, enemigos o balas
def dibujar_pantalla_juego():
    global fondo_y
    
    # Aqui se mueve el fondo
    fondo_y += velocidad_fondo
    if fondo_y >= screen_height:
        fondo_y = 0
    
    screen.blit(fondo_juego, (0, fondo_y))  # Dibujar el fondo en la nueva posición
    screen.blit(fondo_juego, (0, fondo_y - screen_height))  # Para asegurar que el fondo cubra todo
    
    screen.blit(nave_jugador, (nave_x, nave_y)) #Nave del jugador
    
    #for enemigo in enemigos:
        #screen.blit(enemigo[0], (enemigo[1], enemigo[2]))
    
    for bala in balas:
        bala.dibujar_bala(screen)
    
    for bala_enemiga in balas_enemigas:
        bala_enemiga.dibujar_bala(screen)

    nivel_1.actualizar_enemigos(enemigos, balas_enemigas, screen)

def main():
    global nave_x, ultimo_disparo #Variables globales para poder acceder a ellas desde cualquier parte del codigo
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            #Codigo de las teclas que disparan la bala
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                if time.time() - ultimo_disparo >= cooldown_disparo:
                    balas.append(Bala(nave_x, nave_y))
                    ultimo_disparo = time.time()

        #Codigo del movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys [pygame.K_LEFT] and nave_x > 0:
            nave_x -= velocidad_jugador
        if keys[pygame.K_RIGHT] and nave_x < screen_width - nave_jugador.get_width():
            nave_x += velocidad_jugador

        #Codigo que evita que se acumulen las balas dentro del juego y las borra cuando ya no son vistas y las mueve
        for bala in balas[:]:
            bala.mover()
            if bala.y < 0:
                balas.remove(bala)
        
        for bala_enemiga in balas_enemigas[:]:
            bala_enemiga.mover()
            if bala_enemiga.y > screen_height:
                balas_enemigas.remove(bala_enemiga)
        
        #Funciones que detectan las colisiones
        detectar_colisiones()
        colision_jugador_balas_enemigas()

        for enemigo in enemigos:
            enemigo.disparar(balas_enemigas, enemigos)

        dibujar_pantalla_juego()
        pygame.display.update()

if __name__ == "__main__":
    main()