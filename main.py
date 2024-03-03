import pygame
from os import system
import time
import random
screenRes = [1600, 1000]
class obj:
    neighbours = [[-1, -1], [-1, 0], [-1, 1],
                 [0, -1], [0, 0], [0, 1],
                 [1, -1], [1, 0], [1, 1]]
    gfactor = 40
    grid = list()
    gLen = [int(screenRes[0]//gfactor), int(screenRes[1]//gfactor)]
    velLimit = 300
    for i in range(gLen[0]):
        grid.append(list())
        for j in range(gLen[1]):
            grid[i].append(list())
    def __init__(self, type, pos, vel, acc) -> None:
        self.type = type # 'r' -> Rock; 'p' -> Paper; 's' -> Scissors
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(vel)
        self.acc = pygame.math.Vector2(acc) #this isn't needed currently so you can forget this
        self.gi = [int(pos[0]//obj.gfactor), int(pos[1]//obj.gfactor)]
        # self.isDead = False
        obj.grid[self.gi[0]][self.gi[1]].append(self)
    def update(self, dt)->None:
        # if self.isDead == True:
        #     return

        self.vel[0] += (0.5-random.random())*2000*dt
        self.vel[1] += (0.5-random.random())*2000*dt
        self.pos += self.vel*dt

        if self.pos[0] < 10:
            self.pos[0] = 11
            self.vel[0] = -self.vel[0]
        elif self.pos[0] > screenRes[0]-10:
            self.pos[0] = screenRes[0]-11
            self.vel[0] = -self.vel[0]
        
        if self.pos[1] < 10:
            self.pos[1] = 11
            self.vel[1] = -self.vel[1]
        elif self.pos[1] > screenRes[1]-10:
            self.pos[1] = screenRes[1]-11
            self.vel[1] = -self.vel[1]
        
        ratio = obj.velLimit/self.vel.magnitude()
        if ratio < 1:
            self.vel *= ratio
        
        obj.grid[self.gi[0]][self.gi[1]].remove(self)
        self.gi = [int(self.pos[0]//obj.gfactor), int(self.pos[1]//obj.gfactor)]
        obj.grid[self.gi[0]][self.gi[1]].append(self)
    
    def convert(self)->None:
        # if self.isDead == True:
        #     return
        for i in obj.neighbours:
            x = self.gi[0] + i[0]
            y = self.gi[1] + i[1]
            if 0<=x<obj.gLen[0] and 0<=y<obj.gLen[1]:
                for elem in obj.grid[x][y]:
                    if elem != self: #and elem.isDead == False:
                        if (elem.pos-self.pos).magnitude() < obj.gfactor*0.75:
                            if self.type == 'r' and elem.type == 's':
                                elem.type = 'r'
                                # elem.isDead = True
                            elif self.type == 'p' and elem.type == 'r':
                                elem.type = 'p'
                                # elem.isDead = True
                            elif self.type == 's' and elem.type == 'p':
                                elem.type = 's'
                                # elem.isDead = True
    def blit(self)->None:
        # if self.isDead == True:
        #     return
        if self.type == 'r':
            screen.blit(rock, [self.pos[0]-obj.gfactor*0.375, self.pos[1]-obj.gfactor*0.375])
        elif self.type == 'p':
            screen.blit(paper, [self.pos[0]-obj.gfactor*0.375, self.pos[1]-obj.gfactor*0.375])
        elif self.type == 's':
            screen.blit(scissor, [self.pos[0]-obj.gfactor*0.375, self.pos[1]-obj.gfactor*0.375])


        
FoNt = 0
FoNtprint = 0
def cls():
    system("cls")
def font(face:str,size=18):
    global FoNt
    FoNt = pygame.font.SysFont(face,size)
def printpy(text:str,coords=(100,400),color=(128,128,128)):
    global FoNt,FoNtprint
    FoNtprint = FoNt.render(text,True,color)
    screen.blit(FoNtprint,coords)

rock = pygame.transform.scale(pygame.image.load("images/rock.png"), [obj.gfactor*0.75, obj.gfactor*0.75])
paper = pygame.transform.scale(pygame.image.load("images/paper.png"), [obj.gfactor*0.75, obj.gfactor*0.75])
scissor = pygame.transform.scale(pygame.image.load("images/scissor.png"), [obj.gfactor*0.75, obj.gfactor*0.75])

if __name__ == "__main__":
    frameRate = 1000
    dt = 1/1000
    pygame.init()
    screen = pygame.display.set_mode(screenRes)
    #icon = pygame.image.load('')
    pygame.display.set_caption("Bozo's Experiment")
    #pygame.display.set_icon(icon)
    cls()
    objects = list()
    for i in range(150):
        objects.append(obj(random.choice(['r', 'p', 's']), [random.random()*screenRes[0], random.random()*screenRes[1]], [(0.5-random.random())*50, (0.5-random.random())*50], 0))
    # for i in range(50):
    #     objects.append(obj('r', [random.random()*screenRes[0], random.random()*screenRes[1]], [(0.5-random.random())*50, (0.5-random.random())*50], 0))
    # for i in range(50):
    #     objects.append(obj('p', [random.random()*screenRes[0], random.random()*screenRes[1]], [(0.5-random.random())*50, (0.5-random.random())*50], 0))
    # for i in range(50):
    #     objects.append(obj('s', [random.random()*screenRes[0], random.random()*screenRes[1]], [(0.5-random.random())*50, (0.5-random.random())*50], 0))
    running = True
    clock = pygame.time.Clock()
    while running == True:
        initTime = time.time()
        clock.tick(frameRate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #Code Here
        screen.fill((10, 10, 10))
        for i in objects:
            i.blit()
            i.update(dt)
            i.convert()

        pygame.display.update()
        endTime = time.time()
        dt = endTime-initTime
        if dt != 0:
            frameRate = 1/dt
        else:
            frameRate = 1000