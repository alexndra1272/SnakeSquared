import pygame
import sys
import random
import csv

from pygame.constants import MOUSEBUTTONDOWN, QUIT, RESIZABLE
from pygame.event import peek

#Inicializar
pygame.init()

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE =  (255, 255, 255)
FONT = pygame.font.Font(None, 32)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            
            else:
                self.active = False
            
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
          
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
          
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

#Constructor comida
class Food():
    def __init__(self):
        self.position = (0, 0)
        self.setpos()

    def setpos(self):
         self.position = (random.randint(10, grid_width-1)*grid, random.randint(10, grid_height-1)*grid)
    
    def draw(self, screen):
        #rata = pygame.image.load("Rata.png").convert_alpha()
        #screen.blit(rata, (self.position[0], self.position[1]))
        cuadrito = pygame.Rect((self.position[0], self.position[1]), (grid, grid))
        pygame.draw.rect(screen, (0, 0, 255), cuadrito)
        pygame.draw.rect(screen, (0, 0, 0), cuadrito, 1)

#Constructor serpiente
class Snake():
    def __init__(self, valor, color): 
        self.length = 1
        self.position = [((width/2), (height/2))]
        self.direction = random.choice([up, left, right, down])
        self.color = color
        self.score = 0
        self.valor = valor
    
    #Dibujar culebrita
    def draw(self, screen):
        for i in self.position:
            body = pygame.Rect((i[0], i[1]), (grid, grid))
            pygame.draw.rect(screen, self.color, body)
            pygame.draw.rect(screen, (0, 0, 0), body, 1)
    
    #Get position
    def get_position(self):
        return self.position[0]

    #Definir direction
    def set_direction(self, onedirection):
        if self.length > 1 and (onedirection[0]*-1, onedirection[1]*-1) == self.direction:
            return
        
        else:
            self.direction = onedirection

    #Mover
    def move(self):
        pos = self.get_position()
        x, y = self.direction
        newpos = (((pos[0] + (x * grid)) % width), 
                 ((pos[1] + (y * grid)) % height))
        
        #Colisiones
        if len(self.position) > 2 and newpos in self.position[2:]:
            gameOver(screen)
            self.setsnake()
        
        else:
            self.position.insert(0, newpos)
            if len(self.position) > self.length:
                self.position.pop()
    
    def setsnake(self):
        self.length = 1
        self.position = [((width/2), (height/2))]
        self.direction = random.choice([up, left, right, down])
        self.score = 0

    #Evento de teclas
    def evento(self):
        #Detecta todas las acciones que se realicen en la pantalla
        for i in pygame.event.get():
            if i.type == QUIT:
                pygame.quit()
                sys.exit()
            
            #Flechas direccionales
            if i.type == pygame.KEYDOWN:
                if self.valor == 1:
                    if i.key == pygame.K_UP:
                        self.set_direction(up)
                    elif i.key == pygame.K_DOWN:
                        self.set_direction(down)
                    elif i.key == pygame.K_LEFT:
                        self.set_direction(left)
                    elif i.key == pygame.K_RIGHT:
                        self.set_direction(right)
                elif self.valor == 2:
                    if i.key == pygame.K_w:
                        self.set_direction(up)
                    elif i.key == pygame.K_s:
                        self.set_direction(down)
                    elif i.key == pygame.K_a:
                        self.set_direction(left)
                    elif i.key == pygame.K_d:
                        self.set_direction(right)
            
        
                    

#Variables
grid = 20
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

#crear la pantalla
width = 880
height = 600
width_juego = 805
grid_width = int(width_juego/grid)
grid_height = int(455/grid)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Squared")

#Botones
letra = pygame.font.SysFont("Arial Black", 20)
izquierdo = Snake(1, (87, 181, 136))
color = (59, 73, 124, 1)
centro = Snake(2, (128, 87, 181, 1))


def pantallaP(screen):
    screen.fill(color)
    #Rectangulo de juego
    borde = pygame.Rect(15, 35, 850, 510)
    pygame.draw.rect(screen,(0,0,0), borde)
    game = pygame.Rect(20, 40, 840, 500)
    pygame.draw.rect(screen,(27, 33, 55, 1), game)
    controler = pygame.image.load("Controles.png").convert_alpha()
    screen.blit(controler, (5, 5))
    puntaje = pygame.image.load("Puntuación.png").convert_alpha()
    screen.blit(puntaje, (680, 13))
    
    derecho = Food()

    atraso = pygame.time.Clock()
    myfont = pygame.font.SysFont("monospace", 26)

    while True:
    #Controlar velocidad de la serpiente
        atraso.tick(8)
        screen.fill(color)
        pygame.draw.rect(screen,(0,0,0), borde)
        pygame.draw.rect(screen,(27, 33, 55, 1), game)
        screen.blit(puntaje, (680, 13))
        screen.blit(controler, (5, 5))
        izquierdo.evento()
        izquierdo.move()
        izquierdo.draw(screen)

        
        if izquierdo.get_position() == derecho.position:
            izquierdo.length += 1
            izquierdo.score += 1
            derecho.setpos()
        
        if izquierdo.get_position()[0] <= 0 or izquierdo.get_position()[0] >= 860 or izquierdo.get_position()[1] <= 30 or izquierdo.get_position()[1] >= 540:
            gameOver(screen)
            return
        
        text = myfont.render("{0}".format(izquierdo.score), 1, (255, 255, 255))
        screen.blit(text, (800, 7))
        derecho.draw(screen)
        pygame.display.flip()

    
def pantallaP2(screen):
    screen.fill(color)
    #Rectangulo de juego
    borde = pygame.Rect(15, 35, 850, 510)
    pygame.draw.rect(screen,(0,0,0), borde)
    game = pygame.Rect(20, 40, 840, 500)
    pygame.draw.rect(screen,(27, 33, 55, 1), game)
    controler = pygame.image.load("Controles.png").convert_alpha()
    screen.blit(controler, (5, 5))
    puntaje = pygame.image.load("Puntuación.png").convert_alpha()
    
    derecho = Food()

    atraso = pygame.time.Clock()
    myfont = pygame.font.SysFont("Arial Black", 13)

    while True:
    #Controlar velocidad de la serpiente
        atraso.tick(8)
        screen.fill(color)
        pygame.draw.rect(screen,(0,0,0), borde)
        pygame.draw.rect(screen,(27, 33, 55, 1), game)
        screen.blit(puntaje, (640, 13))
        screen.blit(puntaje, (380, 13))
        screen.blit(controler, (5, 5))
  
        centro.move()
        centro.draw(screen)

        izquierdo.move()
        izquierdo.draw(screen)

       
        for i in pygame.event.get():
            if i.type == QUIT:
                pygame.quit()
                sys.exit()            
            #Flechas direccionales
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_UP:
                    izquierdo.set_direction(up)
                elif i.key == pygame.K_DOWN:
                    izquierdo.set_direction(down)
                elif i.key == pygame.K_LEFT:
                    izquierdo.set_direction(left)
                elif i.key == pygame.K_RIGHT:
                    izquierdo.set_direction(right)
                elif i.key == pygame.K_w:
                    centro.set_direction(up)
                elif i.key == pygame.K_s:
                    centro.set_direction(down)
                elif i.key == pygame.K_a:
                    centro.set_direction(left)
                elif i.key == pygame.K_d:
                    centro.set_direction(right)

        if izquierdo.get_position() == derecho.position:
            izquierdo.length += 1
            izquierdo.score += 1
            derecho.setpos()

        elif centro.get_position() == derecho.position:
            centro.length += 1
            centro.score += 1
            derecho.setpos()
        
        if izquierdo.get_position()[0] <= 0 or izquierdo.get_position()[0] >= 860 or izquierdo.get_position()[1] <= 30 or izquierdo.get_position()[1] >= 540:
            gameOver2(screen)
            return
        
        elif centro.get_position()[0] <= 0 or centro.get_position()[0] >= 860 or centro.get_position()[1] <= 30 or centro.get_position()[1] >= 540:
            gameOver2(screen)
            return
        
        text = myfont.render("VERDE - {0}".format(izquierdo.score), 1, (255, 255, 255))
        text2 = myfont.render("MORADO - {0}".format(centro.score), 1, (255, 255, 255))
        screen.blit(text, (750, 12))
        screen.blit(text2, (500, 12))
        derecho.draw(screen)
        pygame.display.flip()

def gameOver2(screen):
    play1 = pygame.Rect(350, 420, 200, 40)
    fondo = pygame.Rect(0, 0, 880, 600)
    myfont = pygame.font.SysFont("monospace", 26)
    text = myfont.render("PLAYER", 1, (255, 255, 255))
    gameOver = pygame.image.load("GAMEOVER.png").convert_alpha()
    opc = 1
    
    while opc == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if play1.collidepoint(pygame.mouse.get_pos()):
                    opc = 0    
                    centro.setsnake()
                    izquierdo.setsnake()
                    menu(screen)
        pygame.draw.rect(screen,color, fondo)
        screen.blit(gameOver, (310, 80)) #Imagen
        boton(screen, play1, "MENÚ") #Boton
        if centro.score > izquierdo.score:
            text = myfont.render("¡GANADOR: MORADO!", 1, (255, 255, 255))
            screen.blit(text, (330, 340)) #Texto Player
        elif centro.score < izquierdo.score:
            text = myfont.render("¡GANADOR: VERDE!", 1, (255, 255, 255))
            screen.blit(text, (330, 340)) #Texto Player
        else: 
            text = myfont.render("¡EMPATE!", 1, (255, 255, 255))
            screen.blit(text, (400, 300)) #Texto Player
        
        

        
        pygame.display.update()

def gameOver(screen):
    play1 = pygame.Rect(350, 420, 200, 40)
    fondo = pygame.Rect(0, 0, 880, 600)
    myfont = pygame.font.SysFont("monospace", 26)
    text = myfont.render("PLAYER", 1, (255, 255, 255))
    gameOver = pygame.image.load("GAMEOVER.png").convert_alpha()
    opc = 1
    input_box1 = InputBox(350, 340, 250, 40)
    input_boxes = [input_box1]
    
    while opc == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for box in input_boxes:
                box.handle_event(event)

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if play1.collidepoint(pygame.mouse.get_pos()):
                    opc = 0
                    with open('registro.csv', 'a', newline='') as csvfile:
                        fieldnames = ['Player', 'Score']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow({'Player': box.text, 'Score': izquierdo.score})
                    izquierdo.setsnake()
                    menu(screen)

        for box in input_boxes:
            box.update()
            pygame.draw.rect(screen,color, fondo)
            screen.blit(gameOver, (310, 80)) #Imagen
            screen.blit(text, (410, 300)) #Texto Player
            boton(screen, play1, "GUARDAR") #Boton
            for box in input_boxes:
                box.draw(screen)
        
        pygame.display.update()
    
def score():
    screen.fill((39, 48, 80, 1))
    menu1 = pygame.Rect(360, 490, 140, 40)
    textomamalon = pygame.image.load("HIGH_SCORES.png").convert_alpha()
    screen.blit(textomamalon, (175, 60))

    #Contenedor de la puntuación
    contenido = pygame.Rect(170, 160, 530, 390) 
    pygame.draw.rect(screen,(59, 73, 124, 0.65), contenido, border_radius = 12)

    #Borde de los circulos
    pygame.draw.circle(screen, (0,0,0), (210, 190), 18)
    pygame.draw.circle(screen, (0,0,0), (660, 190), 18)
    pygame.draw.circle(screen, (0,0,0), (210, 500), 18)
    pygame.draw.circle(screen, (0,0,0), (660, 500), 18)
    
    #Circulitos
    pygame.draw.circle(screen, (87, 97, 181, 1), (210, 190), 15)
    pygame.draw.circle(screen, (87, 97, 181, 1), (660, 190), 15)
    pygame.draw.circle(screen, (87, 97, 181, 1), (210, 500), 15)
    pygame.draw.circle(screen, (87, 97, 181, 1), (660, 500), 15)
    
    #Agregamos los botones
    boton(screen, menu1, "REGRESAR")
    
    sco = pygame.font.SysFont("Algerian", 20)
    y = 220
    datos = []
    j = 0
    with open("registro.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            datos.append((int(row["Score"]), row["Player"]))
    
    datos = sorted(datos, reverse=True)

    cont = 0
    for i in datos:
        text1 = sco.render("{}".format(i[1]), True, (255, 255, 255))
        screen.blit(text1, (300, y))
        text2 = sco.render("{}".format(i[0]), True, (255, 255, 255))
        screen.blit(text2, (560, y))
        cont += 1
        if(cont == 8):
            break
        y += 30
    
    opc = 1
    while opc == 1:
        for i in pygame.event.get():
            if i.type == QUIT:
                pygame.quit()
                sys.exit()

            if i.type == MOUSEBUTTONDOWN and i.button == 1:
                if menu1.collidepoint(pygame.mouse.get_pos()):
                    opc = 0
                    menu(screen)
                    break

        pygame.display.update()
        
    print(datos)

def boton(screen, rectangule, text):
    pygame.draw.rect(screen, (0, 0, 0), [rectangule[0] - 3, rectangule[1] - 3, rectangule[2] + 6, rectangule[3] + 6], 9,border_radius = 13)
    pygame.draw.rect(screen, (87, 97, 181, 1), rectangule,border_radius = 12)
    text1 = letra.render(text, True, (255, 255, 255))
    text2 = letra.render(text, True, (0, 0, 0))
    screen.blit(text2, ((rectangule.x + (rectangule.width-text1.get_width())/2)-3, 
                        rectangule.y + (rectangule.height-text1.get_height())/2))
    screen.blit(text1, (rectangule.x + (rectangule.width-text1.get_width())/2, 
                        rectangule.y + (rectangule.height-text1.get_height())/2)) #Centrar

#Lo hago aquí para después unirlo
play = pygame.Rect(320, 270, 250, 40)
multiplayer = pygame.Rect(320, 360, 250, 40)
clasification = pygame.Rect(320, 450, 250, 40)

def menu(screen):
    screen.fill((39, 48, 80, 1))
    textomamalon = pygame.image.load("SnakeText1.png").convert_alpha()
    serpiente = pygame.image.load("serpiente1.png").convert_alpha()
    screen.blit(serpiente, (545, 50))
    serpiente2 = pygame.image.load("serpiente2.png").convert_alpha()
    screen.blit(serpiente2, (35, 50))
    screen.blit(textomamalon, (175, 50))
    
    #Contenedor de los botones
    contenido = pygame.Rect(210, 210, 460, 330) 
    pygame.draw.rect(screen,(59, 73, 124, 0.65), contenido, border_radius = 12)
    
    #Borde de los cierculos
    pygame.draw.circle(screen, (0,0,0), (250, 250), 18)
    pygame.draw.circle(screen, (0,0,0), (630, 250), 18)
    pygame.draw.circle(screen, (0,0,0), (250, 500), 18)
    pygame.draw.circle(screen, (0,0,0), (630, 500), 18)
    
    #Circulitos
    pygame.draw.circle(screen, (87, 97, 181, 1), (250, 250), 15)
    pygame.draw.circle(screen, (87, 97, 181, 1), (630, 250), 15)
    pygame.draw.circle(screen, (87, 97, 181, 1), (250, 500), 15)
    pygame.draw.circle(screen, (87, 97, 181, 1), (630, 500), 15)
    
    #Agregamos los botones
    boton(screen, play, "JUGAR")
    boton(screen, multiplayer, "MULTIJUGADOR")
    boton(screen, clasification, "CLASIFICACION")
    
    opc = 1
    while opc == 1:
        for i in pygame.event.get():
            if i.type == QUIT:
                pygame.quit()
                sys.exit()
    
            if i.type == MOUSEBUTTONDOWN and i.button == 1:
                if play.collidepoint(pygame.mouse.get_pos()):
                    opc = 0
                    pantallaP(screen)
                    break
    
                if multiplayer.collidepoint(pygame.mouse.get_pos()):
                    opc = 0
                    pantallaP2(screen)
                    break
    
                if clasification.collidepoint(pygame.mouse.get_pos()):
                    opc = 0
                    score()
                    break
    
        pygame.display.update()    

derecho = Food()
atraso = pygame.time.Clock()

menu(screen)    
while True:
    for i in pygame.event.get():
        if i.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()