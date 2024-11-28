import pygame
import sys
import main  # Importamos el archivo main.py para regresar al menú principal

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Ranking")

# Cargar la imagen de fondo del ranking
fondo_ranking = pygame.image.load("assets/background_ranking.png")  # Cambia la ruta si es necesario

# Cargar el botón de regreso
boton_volver = pygame.image.load("assets/button_back.png")  # Asegúrate de tener esta imagen en la carpeta correcta
boton_volver_x = 20  # Posición horizontal del botón
boton_volver_y = 20  # Posición vertical del botón

# Función para dibujar la pantalla del ranking
def dibujar_pantalla_ranking():
    # Dibujar el fondo
    screen.blit(fondo_ranking, (0, 0))
    # Dibujar el botón de regreso
    screen.blit(boton_volver, (boton_volver_x, boton_volver_y))

# Función para verificar si se hace clic en el botón
def is_over_button(pos, x, y, boton):
    return x <= pos[0] <= x + boton.get_width() and y <= pos[1] <= y + boton.get_height()

# Loop principal del ranking
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si se hace clic en el botón de regresar
                if is_over_button(event.pos, boton_volver_x, boton_volver_y, boton_volver):
                    return
        
        # Dibujar la pantalla del ranking
        dibujar_pantalla_ranking()
        pygame.display.update()

if __name__ == "__main__":
    main()
