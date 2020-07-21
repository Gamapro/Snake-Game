import pygame
import numpy as np
import time
import threading

class Food():
    
    def __init__(self,ocupadas):
        posibles = [(x,y) for x in range(ncx) for y in range(ncy)]

        def filtro(val): 
            for i in range(4):
                if (val[0],val[1],i) in ocupadas:
                    return False
            return True

        posibles = list(filter(filtro,posibles))

        index = np.random.randint(len(posibles))
        self.posx = posibles[index][0]
        self.posy = posibles[index][1]

    def getXY(self):
        return (self.posx,self.posy)

class Snake:

    def __init__(self,x,y):
        """Inicializando la snake"""
        self.length = 1
        self.vals = [(x,y,0)]
        self.direction = 0

    def getState(self):
        return self.vals

    def getSize(self):
        return len(self.vals)

    def new_direction(self,new_direction):
        #self.direction = new_direction
        if self.direction == 0 and new_direction != 1:   # Norte
            self.direction = new_direction
        elif self.direction == 1 and new_direction != 0: # Sur
            self.direction = new_direction
        elif self.direction == 2 and new_direction != 3: # Derecha
            self.direction = new_direction
        elif self.direction == 3 and new_direction != 2: # Izquierda
            self.direction = new_direction

    """
    ---- Direccion ----
    0 - Norte 
    1 - Sur
    2 - Derecha
    3 - Izquierda
    """

    def show(self,ncx,ncy,actFood):        
        """ Show State """
        for x in range(ncx):
            for y in range(ncy):
                coord = [
                    (round(x * dimCX),round(y * dimCY)),
                    (round((x+1) * dimCX),round(y * dimCY)),
                    (round((x+1) * dimCX),round((y+1) * dimCY)),
                    (round(x * dimCX),round((y+1) * dimCY))
                ]
                pygame.draw.polygon(screen,colorM,coord,1)

        for x,y,direction in self.vals:
            coord = [
                (round(x * dimCX),round(y * dimCY)),
                (round((x+1) * dimCX),round(y * dimCY)),
                (round((x+1) * dimCX),round((y+1) * dimCY)),
                (round(x * dimCX),round((y+1) * dimCY))
            ]
            pygame.draw.polygon(screen,colorV,coord,0)

        x,y = actFood.posx, actFood.posy
        coord = [
            (round(x * dimCX),round(y * dimCY)),
            (round((x+1) * dimCX),round(y * dimCY)),
            (round((x+1) * dimCX),round((y+1) * dimCY)),
            (round(x * dimCX),round((y+1) * dimCY))
        ]
        pygame.draw.polygon(screen,colorF,coord)
    
    def update(self,ncx,ncy,actFood,vivo):
        
        x,y,direction = self.vals[0]
        delta = 1
        if (x,y) == actFood.getXY():
            delta = 0
            coord = [
                (round(x * dimCX),round(y * dimCY)),
                (round((x+1) * dimCX),round(y * dimCY)),
                (round((x+1) * dimCX),round((y+1) * dimCY)),
                (round(x * dimCX),round((y+1) * dimCY))
            ]
            pygame.draw.polygon(screen,colorV,coord,0)
            actFood = Food(self.getState())

        tupla = ()
        if self.direction == 0:   # Norte
            tupla = (x,(y+ncy-1)%ncy,self.direction)
        elif self.direction == 1: # Sur
            tupla = (x,(y+1)%ncy,self.direction)
        elif self.direction == 2: # Derecha
            tupla = ((x+1)%ncx,y,self.direction)
        elif self.direction == 3: # Izquierda
            tupla = ((x+ncx-1)%ncx,y,self.direction)
        self.vals = [tupla] + self.vals[:len(self.vals) - delta]
        
        #print(self.vals)
        conteo = {}
        for tup in self.vals:
            val = str(tup[0])+","+str(tup[1])
            conteo[val] = 0
        for tup in self.vals:
            val = str(tup[0])+","+str(tup[1])
            conteo[val]+=1
            if conteo[val] > 1:
                vivo = False
                print("MUEREEEEEEEEEE")

        return actFood,vivo


# Init
pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width,height+80))
pygame.display.set_caption('Snake Game') 
vivo = True

# Background :v
background = (25, 25, 25)
screen.fill(background)
ncx, ncy = 20, 20                           # Num de celdas en x, y, z
dimCX, dimCY = width/ncx , height/ncy       # Ancho de los cuadrados
colorM, colorV, colorF = (128, 128, 128), (255,255,255), (255,0,0)

# Estado de las celdas
snk = Snake(ncx//2,ncy//2)
actFood = Food(snk.getState())
speed, rate = 20, 3.5
keyState = [0,0,0,0,0,0]

# Text
textX, textY = width // 2, height + 40
font = pygame.font.Font('freesansbold.ttf', 32)
screen.fill(background)

# INTRO

font = pygame.font.Font('freesansbold.ttf', 72)
text = font.render('SNAKE GAME', True, colorV, background)
textRect = text.get_rect()
textRect.center = (textX, 100)

fontIntro = pygame.font.Font('freesansbold.ttf', 40)
textIntro = fontIntro.render('PRESS INTRO TO CONTINUE', True, colorV, background)
textRectIntro = textIntro.get_rect()
textRectIntro.center = (textX, 300)

fontControls = pygame.font.Font('freesansbold.ttf', 40)
textControls = fontControls.render('Controls', True, colorV, background)
textRectControls = textControls.get_rect()
textRectControls.center = (textX, textY-150)

fontControls2 = pygame.font.Font('freesansbold.ttf', 16)
textControls2 = fontControls2.render('NORTH         SOUTH             LEFT             RIGHT             UP        DOWN', True, colorV, background)
textRectControls2 = textControls2.get_rect()
textRectControls2.center = (textX, textY-80)

fontControls3 = pygame.font.Font('freesansbold.ttf', 16)
textControls3 = fontControls3.render('UP_KEY    DOWN_KEY    LEFT_KEY    RIGHT_KEY    W_KEY    S_KEY', True, colorV, background)
textRectControls3 = textControls3.get_rect()
textRectControls3.center = (textX, textY-40)

screen.blit(text, textRect) 
screen.blit(textIntro, textRectIntro) 
screen.blit(textControls, textRectControls) 
screen.blit(textControls2, textRectControls2) 
screen.blit(textControls3, textRectControls3) 

pygame.display.flip()
   
while True:

    pygame.time.delay(speed)

    e = pygame.event.get()
    for event in e:
        if event.type == pygame.QUIT: run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_RETURN]:
        break


def checar():
    while vivo:
        """
        EVENT
        ---- Direccion ----
        0 - Norte 
        1 - Sur
        2 - Derecha
        3 - Izquierda
        """
           
        e = pygame.event.get()
        for event in e:
            if event.type == pygame.QUIT: run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            snk.new_direction(0)
        elif keys[pygame.K_DOWN]:
            snk.new_direction(1)
        elif keys[pygame.K_RIGHT]:
            snk.new_direction(2)
        elif keys[pygame.K_LEFT]:
            snk.new_direction(3)

        pygame.time.delay(speed)

t = threading.Thread(target=checar)
t.start()

# Ejecucion
while vivo:

    screen.fill(background) # Limpiar el CANVAS
    pygame.time.delay(int(speed*rate))

    text = font.render('Score:'+str(snk.getSize()), True, colorV, background)
    textRect = text.get_rect()
    textRect.center = (textX, textY)

    snk.show(ncx,ncy,actFood)
    screen.blit(text, textRect) 
    
    actFood, vivo = snk.update(ncx,ncy,actFood,vivo)
    pygame.display.flip()



font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Final Score: '+str(snk.getSize()), True, colorV, background)
textRect = text.get_rect()
textRect.center = (textX, textY-18)

text2 = font.render("PRESS ENTER TO EXIT.", True, colorV, background)
textRect2 = text2.get_rect()
textRect2.center = (textX, textY+18)

screen.fill(background)
snk.show(ncx,ncy,actFood)
screen.blit(text, textRect)
screen.blit(text2, textRect2)
pygame.display.flip()

print("PRESS ENTER TO CONTINUE.")
while True:
    e = pygame.event.get()
    for event in e:
        if event.type == pygame.QUIT: run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RETURN]:
        break


pygame.quit()


