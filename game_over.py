# game_over.py
import pygame
import sys
import pantalla_juego
from main import main


pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Cargar los assets
fondo_game_over = pygame.image.load("assets/game_over_background.png")  # Fondo de Game Over
titulo_game_over = pygame.image.load("assets/logo_game_over.png")  # Título de Game Over
boton_menu = pygame.image.load("assets/button_menu_go.png")  # Botón para regresar al menú
boton_reiniciar = pygame.image.load("assets/button_restart.png")  # Botón para reiniciar el juego

# Posiciones de los elementos
titulo_x = (screen_width - titulo_game_over.get_width()) // 2
titulo_y = 100
boton_menu_x = (screen_width - boton_menu.get_width()) // 2
boton_menu_y = 330
boton_reiniciar_x = (screen_width - boton_reiniciar.get_width()) // 2
boton_reiniciar_y = 430

# Variables de movimiento para el fondo
fondo_y = 0
fondo_velocidad = 0.1  # Velocidad de movimiento del fondo

def is_over_button(pos, button_x, button_y, button_img):
    return button_x <= pos[0] <= button_x + button_img.get_width() and button_y <= pos[1] <= button_y + button_img.get_height()

# Función principal de la pantalla Game Over
def game_over_screen(nombre_jugador):
    global fondo_y
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_over_button(event.pos, boton_menu_x, boton_menu_y, boton_menu):
                    from pantalla_juego import jugador
                    pantalla_juego.reiniciar_juego(jugador)
                    import main
                    main.main()
                    running = False
                elif is_over_button(event.pos, boton_reiniciar_x, boton_reiniciar_y, boton_reiniciar):
                    # Reiniciar el juego en el nivel 1
                    from pantalla_juego import jugador
                    pantalla_juego.reiniciar_juego(jugador)  # Llamar a la función de reinicio
                    pantalla_juego.main(nombre_jugador)  # Llamar a la función main de la pantalla de juego
                    running = False

        # Actualizar la posición del fondo
        fondo_y += fondo_velocidad
        if fondo_y >= screen_height:
            fondo_y = 0

        # Dibujar el fondo en movimiento
        screen.blit(fondo_game_over, (0, fondo_y))
        screen.blit(fondo_game_over, (0, fondo_y - screen_height))

        # Dibujar el título y los botones
        screen.blit(titulo_game_over, (titulo_x, titulo_y))
        screen.blit(boton_menu, (boton_menu_x, boton_menu_y))
        screen.blit(boton_reiniciar, (boton_reiniciar_x, boton_reiniciar_y))

        # Cambiar el cursor cuando esté sobre un botón
        mouse_pos = pygame.mouse.get_pos()
        if is_over_button(mouse_pos, boton_menu_x, boton_menu_y, boton_menu) or is_over_button(mouse_pos, boton_reiniciar_x, boton_reiniciar_y, boton_reiniciar):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.update()





