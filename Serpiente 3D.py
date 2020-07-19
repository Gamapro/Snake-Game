import pygame
import numpy as np
import time
import threading

class Food():
    
    def __init__(self,ocupadas):

        posibles = [(x,y,z) for x in range(ncx) for y in range(ncy) for z in range(ncz)]

        def filtro(val): 
            for i in range(6):
                if (val[0],val[1],val[2],i) in ocupadas:
                    return False
            return True

        posibles = list(filter(filtro,posibles))

        index = np.random.randint(len(posibles))
        self.posx = posibles[index][0]
        self.posy = posibles[index][1]
        self.posz = posibles[index][2]

    def getXYZ(self):
        return (self.posx,self.posy,self.posz)

class Snake:

    def __init__(self,x,y,z):
        """Inicializando la snake"""
        self.vals = [(x,y,z,0)]
        self.direction = 0
        self.aux_direction = -1
        self.change = True

    def getState(self):
        return self.vals

    def getSize(self):
        return len(self.vals)

    def new_direction(self,new_direction):
        if new_direction == 4:       # ARRIBA
            # print("Arriba")
            if self.aux_direction != -1:
                return
            self.aux_direction = self.direction
            self.direction = new_direction
        elif new_direction == 5:       # ABAJO
            # print("Abajo")
            if self.aux_direction != -1:
                return
            self.aux_direction = self.direction
            self.direction = new_direction 
        elif self.direction == 0 and new_direction != 1:   # Norte
            # print("Norte")
            self.direction = new_direction
            self.aux_direction = -1
        elif self.direction == 1 and new_direction != 0: # Sur
            # print("Sur")
            self.direction = new_direction
            self.aux_direction = -1
        elif self.direction == 2 and new_direction != 3: # Derecha
            # print("Derecha")
            self.direction = new_direction
            self.aux_direction = -1
        elif self.direction == 3 and new_direction != 2: # Izquierda
            # print("Izquierda")
            self.direction = new_direction
            self.aux_direction = -1

    """
    ---- Direccion ----
    0 - Norte 
    1 - Sur
    2 - Derecha
    3 - Izquierda
    4 - Arriba
    5 - Abajo
    """

    def show(self,ncx,ncy,ncz,actFood):        
        """ Show State """
        for x in range(ncx):
            for y in range(ncy):
                for z in range(ncz):
                    coord = [
                        (x * dimCX + z * (width + 20), y * dimCY),
                        ((x+1) * dimCX + z * (width + 20), y * dimCY),
                        ((x+1) * dimCX + z * (width + 20), (y+1) * dimCY),
                        (x * dimCX + z * (width + 20),(y+1) * dimCY)
                    ]
                    pygame.draw.polygon(screen,colorM,coord,1)

        for x,y,z,direction in self.vals:
            coord = [
                (x * dimCX + z * (width + 20), y * dimCY),
                ((x+1) * dimCX + z * (width + 20), y * dimCY),
                ((x+1) * dimCX + z * (width + 20), (y+1) * dimCY),
                (x * dimCX + z * (width + 20), (y+1) * dimCY)
            ]
            pygame.draw.polygon(screen,colorV,coord,0)

        x,y,z = actFood.getXYZ()
        coord = [
            (x * dimCX + z * (width + 20), y * dimCY),
            ((x+1) * dimCX + z * (width + 20), y * dimCY),
            ((x+1) * dimCX + z * (width + 20), (y+1) * dimCY),
            (x * dimCX + z * (width + 20), (y+1) * dimCY)
        ]
        pygame.draw.polygon(screen,colorF,coord)
    
    def update(self,ncx,ncy,ncz,actFood,vivo):

        x,y,z,direction = self.vals[0]
        delta = 1
        if (x,y,z) == actFood.getXYZ():
            delta = 0
            coord = [
                (x * dimCX + z * (width + 20), y * dimCY),
                ((x+1) * dimCX + z * (width + 20), y * dimCY),
                ((x+1) * dimCX + z * (width + 20), (y+1) * dimCY),
                (x * dimCX + z * (width + 20), (y+1) * dimCY)
            ]
            pygame.draw.polygon(screen,colorV,coord,0)
            actFood = Food(self.getState())

        tupla = ()
        if self.direction == 0:   # Norte
            tupla = (x,(y+ncy-1)%ncy,z,self.direction)
        elif self.direction == 1: # Sur
            tupla = (x,(y+1)%ncy,z,self.direction)
        elif self.direction == 2: # Derecha
            tupla = ((x+1)%ncx,y,z,self.direction)
        elif self.direction == 3: # Izquierda
            tupla = ((x+ncx-1)%ncx,y,z,self.direction)
        elif self.direction == 4: # Arriba
            self.direction = self.aux_direction
            self.aux_direction = -1
            tupla = (x,y,(z+ncz-1)%ncz,self.direction)
        elif self.direction == 5: # Abajo
            self.direction = self.aux_direction
            self.aux_direction = -1
            tupla = (x,y,(z+1)%ncz,self.direction)


        self.vals = [tupla] + self.vals[:len(self.vals) - delta]
       
        self.change = True

        conteo = {}
        for tup in self.vals:
            val = str(tup[0])+","+str(tup[1])+","+str(tup[2])
            conteo[val] = 0
        for tup in self.vals:
            val = str(tup[0])+","+str(tup[1])+","+str(tup[2])
            conteo[val]+=1
            if conteo[val] > 1:
                vivo = False
                print("MUEREEEEEEEEEE")

        return actFood,vivo


# Init
pygame.init()
width, height = 550, 550
real_width, real_height = width*3+40, height+80
screen = pygame.display.set_mode((real_width,real_height))
pygame.display.set_caption('Snake Game') 
pausa = False
vivo = True

# Background :v
background = (25, 25, 25)
screen.fill(background)

ncx, ncy, ncz = 20, 20, 3                   # Num de celdas en x, y, z
dimCX, dimCY = width/ncx , height/ncy       # Ancho de los cuadrados
colorM, colorV, colorF = (128, 128, 128), (255,255,255), (255,0,0)

# Estado de las celdas
snk = Snake(ncx//2,ncy//2,1)
actFood = Food(snk.getState())
speed, rate = 20, 5 
keyState = [0,0,0,0,0,0]

# Text
textX, textY = real_width // 2, height + 40
font = pygame.font.Font('freesansbold.ttf', 32)
screen.fill(background)

# INTRO

font = pygame.font.Font('freesansbold.ttf', 72)
text = font.render('SNAKE GAME', True, colorV, background)
textRect = text.get_rect()
textRect.center = (textX, 100)

fontIntro = pygame.font.Font('freesansbold.ttf', 50)
textIntro = fontIntro.render('PRESS INTRO TO CONTINUE', True, colorV, background)
textRectIntro = textIntro.get_rect()
textRectIntro.center = (textX, 300)

fontControls = pygame.font.Font('freesansbold.ttf', 50)
textControls = fontControls.render('Controls', True, colorV, background)
textRectControls = textControls.get_rect()
textRectControls.center = (textX, textY-150)

fontControls2 = pygame.font.Font('freesansbold.ttf', 32)
textControls2 = fontControls2.render('NORTH         SOUTH             LEFT             RIGHT             UP        DOWN', True, colorV, background)
textRectControls2 = textControls2.get_rect()
textRectControls2.center = (textX, textY-80)

fontControls3 = pygame.font.Font('freesansbold.ttf', 32)
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
        4 - Arriba
        5 - Abajo
        """

        e = pygame.event.get()
        for event in e:
            if event.type == pygame.QUIT: run = False

        keys = pygame.key.get_pressed()

        pygame.time.delay(speed)

        if pausa:
            pygame.time.delay(speed)
            continue

        if snk.change == False:
            continue

        if keys[pygame.K_UP] and keyState[0] == 0:
            keyState[0] = 1
            snk.new_direction(0)
            continue
        elif not keys[pygame.K_UP]:
            keyState[0] = 0
    
        if keys[pygame.K_DOWN] and keyState[1] == 0:
            keyState[1] = 1
            snk.new_direction(1)
            continue
        elif not keys[pygame.K_DOWN]:
            keyState[1] = 0
        
        if keys[pygame.K_RIGHT] and keyState[2] == 0:
            keyState[2] = 1
            snk.new_direction(2)
            continue
        elif not keys[pygame.K_RIGHT]:
            keyState[2] = 0
        
        if keys[pygame.K_LEFT] and keyState[3] == 0:
            keyState[3] = 1
            snk.new_direction(3)
            continue
        elif not keys[pygame.K_LEFT]:
            keyState[3] = 0

        if keys[pygame.K_w] and keyState[4] == 0:
            keyState[4] = 1
            snk.new_direction(4)
            continue
        elif not keys[pygame.K_w]:
            keyState[4] = 0

        if keys[pygame.K_s] and keyState[5] == 0:
            keyState[5] = 1
            snk.new_direction(5)
            continue
        elif not keys[pygame.K_s]:
            keyState[5] = 0


t = threading.Thread(target=checar)
t.start()

# Ejecucion
while vivo:
    
    if pausa:
        pygame.time.delay(speed)
        continue

    screen.fill(background) # Limpiar el CANVAS
    pygame.time.delay(int(speed*rate))

    text = font.render('Score:'+str(snk.getSize()), True, colorV, background)
    textRect = text.get_rect()
    textRect.center = (textX, textY)

    snk.show(ncx,ncy,ncz,actFood)
    screen.blit(text, textRect) 
    
    actFood, vivo = snk.update(ncx,ncy,ncz,actFood,vivo)
    pygame.display.flip()

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Final Score: '+str(snk.getSize()), True, colorV, background)
textRect = text.get_rect()
textRect.center = (textX, textY-18)

text2 = font.render("PRESS ENTER TO EXIT.", True, colorV, background)
textRect2 = text2.get_rect()
textRect2.center = (textX, textY+18)

screen.fill(background)
snk.show(ncx,ncy,ncz,actFood)
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

