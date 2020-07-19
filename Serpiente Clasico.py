import pygame
import numpy as np
import time
import threading

vivo = True

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
                    (x * dimCX, y * dimCY),
                    ((x+1) * dimCX, y * dimCY),
                    ((x+1) * dimCX, (y+1) * dimCY),
                    (x * dimCX, (y+1) * dimCY)
                ]
                pygame.draw.polygon(screen,colorM,coord,1)

        for x,y,direction in self.vals:
            coord = [
                (x * dimCX, y * dimCY),
                ((x+1) * dimCX, y * dimCY),
                ((x+1) * dimCX, (y+1) * dimCY),
                (x * dimCX, (y+1) * dimCY)
            ]
            pygame.draw.polygon(screen,colorV,coord,0)

        x,y = actFood.posx, actFood.posy
        coord = [
            (x * dimCX, y * dimCY),
            ((x+1) * dimCX, y * dimCY),
            ((x+1) * dimCX, (y+1) * dimCY),
            (x * dimCX, (y+1) * dimCY)
        ]
        pygame.draw.polygon(screen,colorF,coord)
    
    def update(self,ncx,ncy,actFood,vivo):
        
        x,y,direction = self.vals[0]
        delta = 1
        if (x,y) == actFood.getXY():
            delta = 0
            coord = [
                (x * dimCX, y * dimCY),
                ((x+1) * dimCX, y * dimCY),
                ((x+1) * dimCX, (y+1) * dimCY),
                (x * dimCX, (y+1) * dimCY)
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
screen = pygame.display.set_mode((width,height))

# Background :v
background = (25, 25, 25)
screen.fill(background)

ncx, ncy = 20, 20                      # Num de celdas en x y y
dimCX, dimCY = width/ncx , height/ncy  # Ancho de los cuadrados
colorM, colorV, colorF = (128, 128, 128), (255,255,255), (255,0,0)

# Estado de las celdas
#gameState = np.random.randint(2,size=(ncx,ncy))
gameState = np.zeros((ncx,ncy))
gameState[ncx//2,ncy//2] = 1
snk = Snake(ncx//2,ncy//2)
actFood = Food(snk.getState())
speed = 20  # 20 ms

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
    #pygame.time.delay(50)
    #time.sleep(1)

    pygame.time.delay(speed*5)

    """
        mouseClick = pygame.mouse.get_pressed()
        sum = 0
        for x in mouseClick:
            sum+=x
        if sum > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX/dimCX)), int(np.floor(posY / dimCY))
            aux[celX,celY] = not mouseClick[2]
    """

    snk.show(ncx,ncy,actFood)
    actFood, vivo = snk.update(ncx,ncy,actFood,vivo)

    pygame.display.flip()

wait = input("PRESS ENTER TO CONTINUE.")
pygame.quit()
