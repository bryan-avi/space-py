import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
running = True


while running:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
pygame.quit()
