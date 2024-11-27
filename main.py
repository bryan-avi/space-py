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

archivo_nombres = "nombres.txt"

font = pygame.font.Font(None, 36)
font_big = pygame.font.Font(None, 48)

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

# Función para guardar nombres en un archivo .txt
def guardar_nombre_en_txt(nombre, archivo=archivo_nombres):
    with open(archivo, "a") as file:  # "a" para agregar sin sobrescribir
        file.write(nombre + "\n")

# Función para leer nombres desde el archivo .txt
def leer_nombres_desde_txt(archivo=archivo_nombres):
    try:
        with open(archivo, "r") as file:  # "r" para leer
            nombres = file.readlines()
        return [nombre.strip() for nombre in nombres]  # Quitar saltos de línea
    except FileNotFoundError:
        return []  # Si el archivo no existe, retorna una lista vacía

# Verificar si el nombre ya existe en la lista de nombres
def nombre_existente(nombre, archivo=archivo_nombres):
    nombres = leer_nombres_desde_txt(archivo)
    return nombre in nombres

# Mostrar pop-up para ingresar el nombre
def solicitar_nombre():
    nombre = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter confirma el nombre
                    if nombre.strip():  # Validar que no esté vacío
                        # Si el nombre ya existe, no lo guardamos, pero dejamos que el jugador continúe
                        if not nombre_existente(nombre.strip()):
                            guardar_nombre_en_txt(nombre.strip())  # Guardar el nombre si no existe
                        return nombre.strip()
                elif event.key == pygame.K_BACKSPACE:  # Borrar caracteres
                    nombre = nombre[:-1]
                else:
                    nombre += event.unicode  # Agregar caracteres

        # Dibujar la pantalla de entrada de nombre
        screen.fill((0, 0, 0))  # Fondo negro para el pop-up
        texto_instruccion = font.render("Ingresa tu nombre y presiona Enter:", True, (255, 255, 255))
        texto_nombre = font_big.render(nombre, True, (255, 255, 255))
        
        # Centramos los textos en la pantalla
        screen.blit(texto_instruccion, (screen_width // 2 - texto_instruccion.get_width() // 2, screen_height // 2 - 50))
        screen.blit(texto_nombre, (screen_width // 2 - texto_nombre.get_width() // 2, screen_height // 2))
        pygame.display.update()

# Loop principal del juego
def main():
    nombre_jugador = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_over_button(event.pos):
                    nombre_jugador = solicitar_nombre()
                    if nombre_jugador:
                        pantalla_juego.main(nombre_jugador)
                        return
        mouse_pos = pygame.mouse.get_pos()
        if is_over_button(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        dibujar_pantalla_inicio()
        pygame.display.update()

if __name__ == "__main__":
    main()

