import pygame
import sys

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Space Invaders - Juego")

#Variables de todos los perosonaje que estaran en el juego
fondo_juego = pygame.image.load("assets/background_game.png") 
nave_jugador = pygame.image.load("assets/player.png")
yellow = pygame.image.load("assets/yellow_enemy.png")
yellow2 = pygame.image.load("assets/yellow_enemy_v2.png")
red = pygame.image.load("assets/red_enemy.png")
joke = pygame.image.load("assets/joke_enemy.png")
boss_yellow = pygame.image.load("assets/boss_yellow.png")

nave_x = (screen_width - nave_jugador.get_width()) // 2
nave_y = screen_height - nave_jugador.get_height() - 50

fondo_y = 0
velocidad_fondo = 0.7

enemigos = [
    #F1
    (yellow2, 50, 225), (yellow, 100, 225), (yellow2, 150, 225), (yellow, 200, 225), (yellow2, 250, 225), (yellow, 300, 225),
    (yellow, 350, 225), (yellow2, 400, 225), (yellow, 450, 225), (yellow2, 500, 225), (yellow, 550, 225),
    (yellow, 600, 225), (yellow2, 650, 225), (yellow, 700, 225), 
    #F2
    (yellow2, 50, 170), (yellow, 100, 170), (red, 159, 170), (yellow2, 250, 170), (yellow, 300, 170),
    (red, 359, 170), (yellow, 450, 170), (yellow2, 500, 170), (red, 559, 170), (yellow2, 650, 170), (yellow, 700, 170), 
    #F3
    (yellow2, 50, 115), (yellow, 100, 115), (red, 159, 115), (yellow2, 250, 115), (joke, 295, 115),
    (red, 359, 115), (joke, 435, 115), (yellow2, 500, 115), (red, 559, 115), (yellow2, 650, 115), (yellow, 700, 115), 
    #F4
    (boss_yellow, 335, 25)
]

def dibujar_pantalla_juego():
    global fondo_y
    
    # Aqui se mueve el fondo
    fondo_y += velocidad_fondo
    if fondo_y >= screen_height:
        fondo_y = 0
    
    screen.blit(fondo_juego, (0, fondo_y))  # Dibujar el fondo en la nueva posición
    screen.blit(fondo_juego, (0, fondo_y - screen_height))  # Para asegurar que el fondo cubra todo
    
    screen.blit(nave_jugador, (nave_x, nave_y))
    
    for enemigo in enemigos:
        screen.blit(enemigo[0], (enemigo[1], enemigo[2]))

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        dibujar_pantalla_juego()
        pygame.display.update()

if __name__ == "__main__":
    main()

