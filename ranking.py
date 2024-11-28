import pygame
import sys
import main 

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Ranking")

fondo_ranking = pygame.image.load("assets/background_ranking.png")  


boton_volver = pygame.image.load("assets/button_back.png")  
boton_volver_x = 20  
boton_volver_y = 20  

# Función para dibujar la pantalla del ranking
def dibujar_pantalla_ranking():
    screen.blit(fondo_ranking, (0, 0))
    screen.blit(boton_volver, (boton_volver_x, boton_volver_y))

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
                
                if is_over_button(event.pos, boton_volver_x, boton_volver_y, boton_volver):
                    return
        
        
        dibujar_pantalla_ranking()
        pygame.display.update()

if __name__ == "__main__":
    main()
