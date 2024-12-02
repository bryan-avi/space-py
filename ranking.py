import pygame
import sys
import main 
from collections import defaultdict

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Ranking")

#Imagenes
fondo_ranking = pygame.image.load("assets/background_ranking.png")  
boton_volver = pygame.image.load("assets/button_back.png")

#Posicion del boton
boton_volver_x = 20  
boton_volver_y = 20

#Archivo de puntaje
archivo_puntaje = "puntaje.txt"

font = pygame.font.Font(None, 36)

# Función para leer y procesar los puntajes del archivo
def leer_puntajes(archivo):
    puntajes = defaultdict(int)  # Diccionario para guardar el mayor puntaje de cada jugador
    try:
        with open(archivo, "r") as file:
            for line in file:
                if ":" in line:  # Asegurar que la línea tiene el formato esperado
                    nombre, puntaje = line.strip().split(":")
                    nombre = nombre.strip().capitalize()  # Normalizar el nombre
                    puntaje = int(puntaje.strip())  # Convertir el puntaje a entero
                    # Guardar solo el mayor puntaje para cada jugador
                    if nombre in puntajes:
                        puntajes[nombre] = max(puntajes[nombre], puntaje)
                    else:
                        puntajes[nombre] = puntaje
    except FileNotFoundError:
        pass  # Si no existe el archivo, devuelve un diccionario vacío
    # Ordenar por puntaje de mayor a menor
    return sorted(puntajes.items(), key=lambda x: x[1], reverse=True)  # Ordenar por puntaje descendente

# Función para dibujar la pantalla del ranking
def dibujar_pantalla_ranking(puntajes):
    screen.blit(fondo_ranking, (0, 0))
    screen.blit(boton_volver, (boton_volver_x, boton_volver_y))

   
    y_offset = 320  
    espacio_entre_lineas = 50 

    font = pygame.font.Font("assets/Vermin Vibes 1989.ttf", 50)

    for idx, (nombre, puntaje) in enumerate(puntajes):
        texto_nombre = font.render(f"{idx + 1}. {nombre}", True, (255, 255, 255))  # Nombre alineado a la izquierda
        texto_puntaje = font.render(f"{puntaje}", True, (255, 255, 255))  # Puntaje alineado a la derecha
        screen.blit(texto_nombre, (150, y_offset))  # Posición del nombre
        screen.blit(texto_puntaje, (screen_width - 250, y_offset))  # Posición del puntaje
        y_offset += espacio_entre_lineas  # Incrementar la posición vertical

def is_over_button(pos, x, y, boton):
    return x <= pos[0] <= x + boton.get_width() and y <= pos[1] <= y + boton.get_height()

# Loop principal del ranking
def main():
    puntajes = leer_puntajes(archivo_puntaje)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if is_over_button(event.pos, boton_volver_x, boton_volver_y, boton_volver):
                    return
        
        dibujar_pantalla_ranking(puntajes)
        pygame.display.update()

if __name__ == "__main__":
    main()
