import pygame
import sys
import time
import nivel_1
import nivel_2
import nivel_final
from nivel_final import BossFinal
import game_over  # Importa el módulo de Game Over
import subprocess

pygame.init()
clock = pygame.time.Clock()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Space Invaders - Juego")

# Variables de todos los elementos que estarán en el juego
fondo_juego = pygame.image.load("assets/background_game.png")
nave_jugador = pygame.image.load("assets/sprites_player/player.png")
bala_unidad = pygame.image.load("assets/shot.png")

# Imágenes del menú de pausa
menu_pausa = pygame.image.load("assets/menu de pausa.png")
boton_resume = pygame.image.load("assets/button_resume.png")
boton_restart = pygame.image.load("assets/button_restart_pause.png")
boton_main_menu = pygame.image.load("assets/button_main_menu.png")
paused = False  # Variable para controlar el estado de pausa

class Jugador:
    def __init__(self, x, y, velocidad, imagen):
        global vida
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.imagen = imagen
        self.vida = 5
        self.balas = []
        self.ultimo_disparo = 0
        self.cooldown_disparo = 0.8  # tiempo de recarga entre disparos
        self.puntaje = 0 #Aca se guardara el puntaje del jugador
        self.ultima_vida_extra = 0 #Nuevo atributo para controlar las vidas extras


    # Movimiento del jugador
    def mover(self, keys, screen_width):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidad
        if keys[pygame.K_RIGHT] and self.x < screen_width - self.imagen.get_width():
            self.x += self.velocidad

    # Disparar una bala
    def disparar(self):
        global balas
        if time.time() - self.ultimo_disparo >= self.cooldown_disparo:
            bala = Bala(self.x, self.y)
            balas.append(bala)
            self.ultimo_disparo = time.time()

    # Dibuja el jugador en la pantalla
    def dibujar(self, surface):
        surface.blit(self.imagen, (self.x, self.y))

    # Detecta colisiones entre las balas del jugador y los enemigos
    def detectar_colisiones(self, enemigos):
        global balas, balas_enemigas
        for bala in balas[:]:
            for enemigo in enemigos[:]:
                if bala.get_rect().colliderect(enemigo.get_rect()):
                    balas.remove(bala)
                    if enemigo.recibir_daño():
                        self.puntaje += enemigo.puntos #Incrementar el puntaje con respecto a la cantidad de puntos
                        enemigos.remove(enemigo)
                    break

    # Detecta las colisiones entre las balas enemigas y el jugador
    def colision_con_balas_enemigas(self, balas_enemigas):
        jugador_rect = pygame.Rect(self.x, self.y, self.imagen.get_width(), self.imagen.get_height())
        for bala in balas_enemigas[:]:
            if jugador_rect.colliderect(bala.get_rect()):
                print(self.vida)
                self.vida -= 1
                balas_enemigas.remove(bala)
                if self.vida <= 0:
                    game_over.game_over_screen()  # Llama a la pantalla de Game Over
                    return False  # El juego termina
        return True  # El jugador sigue con vida

    def chequear_vida_extra(self):
        # Otorga una vida extra por cada 500 puntos, pero solo una vez por umbral
        if self.puntaje >= self.ultima_vida_extra + 500:
            self.vida = min(self.vida + 1, 5)  # Máximo de 5 vidas
            self.ultima_vida_extra += 500

# Clase de la bala
class Bala:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.velocidad = 2  # Velocidad de la bala
    
    def mover(self):
        self.y -= self.velocidad  # Mover la bala hacia arriba
    
    def dibujar_bala(self, surface):
        surface.blit(bala_unidad, (self.x + (nave_jugador.get_width() // 2) - bala_unidad.get_width() // 2, self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x + (nave_jugador.get_width() // 2) - bala_unidad.get_width() // 2, self.y, bala_unidad.get_width(), bala_unidad.get_height())


# Variables del juego
def reiniciar_juego():
    global nave_x, nave_y, balas, enemigos, balas_enemigas, fondo_y, ultimo_disparo, Jugador
    nave_x = (screen_width - nave_jugador.get_width()) // 2
    nave_y = screen_height - nave_jugador.get_height() - 50
    balas = []
    balas_enemigas = []
    fondo_y = 0
    ultimo_disparo = 0
    enemigos = nivel_1.crear_enemigos_nivel_1()
    
# Inicialización de variables
reiniciar_juego()
velocidad_fondo = 0.7
velocidad_jugador = 0.8
cooldown_disparo = 0.8



# Dibuja todos los elementos en la pantalla del juego
def dibujar_pantalla_juego():
    global fondo_y
    
    # Mueve el fondo
    fondo_y += velocidad_fondo
    if fondo_y >= screen_height:
        fondo_y = 0
    
    screen.blit(fondo_juego, (0, fondo_y))  # Dibujar el fondo en la nueva posición
    screen.blit(fondo_juego, (0, fondo_y - screen_height))  # Para cubrir toda la pantalla
    
    for bala in balas:
        bala.dibujar_bala(screen)
    
    for bala_enemiga in balas_enemigas:
        bala_enemiga.dibujar_bala(screen)
        
    nivel_1.actualizar_enemigos(enemigos, balas_enemigas, screen)

# Muestra el menú de pausa y sus botones
def mostrar_menu_pausa():
    global paused  # Declara global antes de modificar la variable
    
    # Dibuja el fondo del juego borroso
    pausa_fondo = pygame.Surface((screen_width, screen_height))
    pausa_fondo.set_alpha(128)  # Hace que el fondo se vea translúcido
    pausa_fondo.fill((0, 0, 0))
    screen.blit(pausa_fondo, (0, 0))

    # Dibuja el menú de pausa
    menu_x = (screen_width - menu_pausa.get_width()) // 2
    menu_y = (screen_height - menu_pausa.get_height()) // 2
    screen.blit(menu_pausa, (menu_x, menu_y))

    # Dibuja los botones
    resume_x = (screen_width - boton_resume.get_width()) // 2
    resume_y = menu_y + 200
    restart_x = (screen_width - boton_restart.get_width()) // 2
    restart_y = resume_y + 60
    main_menu_x = (screen_width - boton_main_menu.get_width()) // 2
    main_menu_y = restart_y + 60
    
    screen.blit(boton_resume, (resume_x, resume_y))
    screen.blit(boton_restart, (restart_x, restart_y))
    screen.blit(boton_main_menu, (main_menu_x, main_menu_y))
    
    pygame.display.update()

    # Verifica si el mouse ha hecho clic sobre algún botón
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if mouse_click[0]:  # Si el botón izquierdo del ratón ha sido presionado
        if resume_x <= mouse_x <= resume_x + boton_resume.get_width() and resume_y <= mouse_y <= resume_y + boton_resume.get_height():
            paused = False  # Reanuda el juego
        elif restart_x <= mouse_x <= restart_x + boton_restart.get_width() and restart_y <= mouse_y <= restart_y + boton_restart.get_height():
            reiniciar_juego()  # Reinicia el juego
            paused = False  # Reanuda el juego
        elif main_menu_x <= mouse_x <= main_menu_x + boton_main_menu.get_width() and main_menu_y <= mouse_y <= main_menu_y + boton_main_menu.get_height():
            paused = False
            import main
            main.main()
            running = False

vidas_sprites = [pygame.image.load("assets/Vidas/lives.png")] + [pygame.image.load(f"assets/Vidas/{i}_lives.png") for i in range(4, 0, -1)]
def dibujar_vidas(jugador, surface):
    # Selecciona el sprite correspondiente al número de vidas del jugador
    if 1 <= jugador.vida <= 5:
        sprite_vida = vidas_sprites[5 - jugador.vida]  # Selecciona la imagen adecuada con base en las vidas
        x = 10  # Posición horizontal de la barra de vidas
        y = 10  # Posición vertical de la barra de vidas
        surface.blit(sprite_vida, (x, y))

def mostrar_puntaje(surface, puntaje, screen_width):
    font = pygame.font.Font("freesansbold.ttf", 24)  # Fuente para el texto
    texto = font.render(f"Puntaje: {puntaje}", True, (255, 255, 255))  # Texto en blanco
    texto_rect = texto.get_rect()  # Obtén las dimensiones del texto
    texto_rect.topright = (screen_width - 10, 10)  # Posición en la esquina superior derecha con un margen de 10 px
    surface.blit(texto, texto_rect)  # Dibujar el puntaje en la pantalla


# Ciclo principal del juego
def main():
    global nave_x, ultimo_disparo, enemigos, paused
    paused = False
    enemigos = nivel_1.crear_enemigos_nivel_1()
    jugador = Jugador(nave_x, nave_y, velocidad_jugador, nave_jugador)
    running = True
    nivel_actual = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Detecta la tecla ESC para pausar o reanudar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

            # Código de las teclas que disparan la bala
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                if not paused:
                    jugador.disparar()

        # Muestra el menú de pausa si el juego está en pausa
        if paused:
            mostrar_menu_pausa()
            continue  # Salta el resto del ciclo para mantener el juego pausado

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        jugador.mover(keys, screen_width)

        # Movimiento y eliminación de balas
        for bala in balas[:]:
            bala.mover()
            if bala.y < 0:
                balas.remove(bala)
        
        for bala_enemiga in balas_enemigas[:]:
            bala_enemiga.mover()
            if bala_enemiga.y > screen_height:
                balas_enemigas.remove(bala_enemiga)

        # Detecta colisiones
        jugador.detectar_colisiones(enemigos)
        jugador.colision_con_balas_enemigas(balas_enemigas)
        
        #Funcione que detecta y da una vida extra
        jugador.chequear_vida_extra()

        # Logica que se encarga de cargar los enemigos de cada nivel (1, 2 y 3)
        for enemigo in enemigos:
            enemigo.mover()
            enemigo.dibujar(screen)
            enemigo.disparar(balas_enemigas, enemigos)

            # En el nivel 3, gestionamos el jefe
            if nivel_actual == 3 and isinstance(enemigo, BossFinal):
                enemigo.disparar_rafaga(balas_enemigas)

        dibujar_pantalla_juego()
        jugador.dibujar(screen)
        dibujar_vidas(jugador, screen)
        mostrar_puntaje(screen, jugador.puntaje, screen_width)

        pygame.display.update()
        clock.tick(360)

        if nivel_1.nivel_terminado(enemigos) and nivel_actual == 1:
            print("Cargando nivel 2")
            pygame.display.update()
            time.sleep(3)
            enemigos = nivel_2.crear_enemigos_nivel_2()
            nivel_actual = 2

        elif nivel_2.nivel_terminado(enemigos) and nivel_actual == 2:
            print("Cargando nivel 3")
            pygame.display.update()
            time.sleep(3)
            enemigos = nivel_final.crear_enemigos_nivel_3()
            nivel_actual = 3

        # Si el nivel 3 ha terminado (ej. todos los enemigos y el jefe han sido eliminados)
        elif nivel_final.nivel_terminado(enemigos) and nivel_actual == 3:
            print("¡Has ganado el juego!")
            running = False

if __name__ == "__main__":
    main()