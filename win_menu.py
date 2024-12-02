import pygame
import sys
import main 
import pantalla_juego

pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


# Imágenes
fondo_victoria = pygame.image.load("assets/background_win.png")  # Imagen del fondo de victoria
boton_menu = pygame.image.load("assets/button_menu_win.png")  # Botón para regresar al menú principal

# Posición del botón
boton_menu_x = screen_width // 2 - boton_menu.get_width() // 2
boton_menu_y = screen_height // 2 + 130

font = pygame.font.Font("assets/Vermin Vibes 1989.ttf", 60)

# Función para verificar si el mouse está sobre un botón
def is_over_button(pos, x, y, boton):
    return x <= pos[0] <= x + boton.get_width() and y <= pos[1] <= y + boton.get_height()

# Función para dibujar la pantalla de victoria
def dibujar_pantalla_victoria(puntaje):
    screen.blit(fondo_victoria, (0, 0))
    screen.blit(boton_menu, (boton_menu_x, boton_menu_y))

    # Muestra el puntaje del jugador en pantalla
    texto_puntaje = font.render(f" {puntaje}", True, (255, 255, 255))

    # Aca se ajusta la posición para bajar el texto (agregando 50 píxeles de desplazamiento)
    texto_puntaje_y = screen_height // 2 + 55

    # Se dibuja el texto en la pantalla
    screen.blit(texto_puntaje, (screen_width // 2 - texto_puntaje.get_width() // 2, texto_puntaje_y))

# Loop principal del menú de victoria
def main(puntaje):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_over_button(event.pos, boton_menu_x, boton_menu_y, boton_menu):
                    from pantalla_juego import jugador
                    pantalla_juego.reiniciar_juego(jugador)
                    import main
                    main.main()
                    running = False
        
        dibujar_pantalla_victoria(puntaje)
        pygame.display.update()

if __name__ == "__main__":
    main(0)
