import pygame
import sys
import pantalla_juego 

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Space Invaders - Pantalla de Inicio")

fondo = pygame.image.load("assets/background.png")
logo = pygame.image.load("assets/logo.png")
boton_start = pygame.image.load("assets/button_start.png")

fondo_x1 = 0
fondo_x2 = screen_width
velocidad_fondo = 0.2

logo_x = (screen_width - logo.get_width()) // 2
logo_y = 100
boton_x = (screen_width - boton_start.get_width()) // 2
boton_y = 400

# esta funcion es para que el fondo se mueva
def mover_fondo():
    global fondo_x1, fondo_x2
    fondo_x1 -= velocidad_fondo
    fondo_x2 -= velocidad_fondo
    if fondo_x1 <= -screen_width:
        fondo_x1 = screen_width
    if fondo_x2 <= -screen_width:
        fondo_x2 = screen_width
    screen.blit(fondo, (fondo_x1, 0))
    screen.blit(fondo, (fondo_x2, 0))

def dibujar_pantalla_inicio():
    mover_fondo()
    screen.blit(logo, (logo_x, logo_y))
    screen.blit(boton_start, (boton_x, boton_y))

# Lo que hace esta funcion es para que el cursor cambie cuando este arriba del boton
def is_over_button(pos):
    if boton_x <= pos[0] <= boton_x + boton_start.get_width() and boton_y <= pos[1] <= boton_y + boton_start.get_height():
        return True
    return False

# Loop principal del juego
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_over_button(event.pos):
                    pantalla_juego.main() 

        mouse_pos = pygame.mouse.get_pos()
        if is_over_button(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        dibujar_pantalla_inicio()
        pygame.display.update()

if __name__ == "__main__":
    main()
