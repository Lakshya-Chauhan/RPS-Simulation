import pygame
from pygame import mixer
from os import system
import time
import random
screenRes = [1600, 1000]
screenCenterVector = pygame.math.Vector2([screenRes[0]/2, screenRes[1]/2])
mixer.init()
audio = {
    "r" : mixer.Sound("audio/rock.mp3"),
    "p" : mixer.Sound("audio/paper.mp3"),
    "s" : mixer.Sound("audio/scissor.mp3")
}
soundON = True
class obj:
    neighbours = [[-1, -1], [-1, 0], [-1, 1],
                 [0, -1], [0, 0], [0, 1],
                 [1, -1], [1, 0], [1, 1]]
    gfactor = 200   #grid size factor
    rfactor = 40    #radius factor
    afactor = 10069*30    #attraction factor
    randFactor = 500  #2000   #randomness factor
    centralAcc = 1234/1.5   #acceleration towards center
    dmin = 2.7569
    maxFriendlyToleration = rfactor*1.5
    wallVelReduction = 0.9
    grid = list()
    gLen = [int(screenRes[0]//gfactor), int(screenRes[1]//gfactor)]
    velLimit = 300
    accelType = {
        'r' : pygame.math.Vector2([(0.5-random.random())*randFactor*50, (0.5-random.random())*randFactor*50]),
        'p' : pygame.math.Vector2([(0.5-random.random())*randFactor*50, (0.5-random.random())*randFactor*50]),
        's' : pygame.math.Vector2([(0.5-random.random())*randFactor*50, (0.5-random.random())*randFactor*50])
    }
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
    def enemy(self) -> str:
        if self.type == 'r': return 'p'
        elif self.type == 'p': return 's'
        elif self.type == 's': return 'r'
    def update(self, dt)->None:
        # if self.isDead == True:
        #     return

        self.vel[0] += (0.5-random.random())*obj.randFactor*dt
        self.vel[1] += (0.5-random.random())*obj.randFactor*dt
        self.vel += obj.accelType[self.type]*dt    #figured out the problem; its here
        
        accel = pygame.math.Vector2(obj.centralAcc)
        accel = accel.rotate(accel.angle_to(screenCenterVector-self.pos))

        self.vel += accel*dt

        # self.vel[1] += 981/4*dt
        
        ratio = obj.velLimit/self.vel.magnitude()
        if ratio < 1:
            self.vel *= ratio

        self.pos += self.vel*dt

        if self.pos[0] < 10:
            self.pos[0] = 11
            self.vel[0] = -self.vel[0]
            self.vel *= obj.wallVelReduction
        elif self.pos[0] > screenRes[0]-10:
            self.pos[0] = screenRes[0]-11
            self.vel[0] = -self.vel[0]
            self.vel *= obj.wallVelReduction
        
        if self.pos[1] < 10:
            self.pos[1] = 11
            self.vel[1] = -self.vel[1]
            self.vel *= obj.wallVelReduction
        elif self.pos[1] > screenRes[1]-10:
            self.pos[1] = screenRes[1]-11
            self.vel[1] = -self.vel[1]
            self.vel *= obj.wallVelReduction
        
        
        obj.grid[self.gi[0]][self.gi[1]].remove(self)
        self.gi = [int(self.pos[0]//obj.gfactor), int(self.pos[1]//obj.gfactor)]
        obj.grid[self.gi[0]][self.gi[1]].append(self)
    
    def convert(self, dt)->None:
        # if self.isDead == True:
        #     return
        for i in obj.neighbours:
            x = self.gi[0] + i[0]
            y = self.gi[1] + i[1]
            if 0<=x<obj.gLen[0] and 0<=y<obj.gLen[1]:
                attraction = pygame.math.Vector2([(0.5-random.random()), (0.5-random.random())])
                newA = pygame.math.Vector2([(0.5-random.random()), (0.5-random.random())])
                for elem in obj.grid[x][y]:
                    if elem != self: #and elem.isDead == False:
                        dist = (elem.pos-self.pos).magnitude()
                        newA= pygame.math.Vector2((elem.type==self.type)*((obj.afactor)/(dist*dist + obj.dmin)))
                        newA = newA.rotate(newA.angle_to(elem.pos-self.pos))
                        if dist > obj.maxFriendlyToleration:
                            attraction += newA
                        #if friendly particles are fare away they will attract; and if they come too near then they will repel; this would seem like collision but it isn't
                        else:
                            attraction -= newA*5
                        newA= 15*pygame.math.Vector2((elem.type==self.enemy())*((obj.afactor)/(dist*dist + obj.dmin)))
                        newA = newA.rotate(newA.angle_to(self.pos-elem.pos))
                        attraction += newA
                        newA= 3*pygame.math.Vector2((elem.enemy()==self.type)*((obj.afactor)/(dist*dist + obj.dmin)))
                        newA = newA.rotate(newA.angle_to(elem.pos-self.pos))
                        attraction += newA
                        if dist < obj.rfactor*0.75:
                            if self.type == 'r' and elem.type == 's':
                                elem.type = 'r'
                                if soundON == True:
                                    audio['r'].play()
                                # elem.isDead = True
                            elif self.type == 'p' and elem.type == 'r':
                                elem.type = 'p'
                                if soundON == True:
                                    audio['p'].play()
                                # elem.isDead = True
                            elif self.type == 's' and elem.type == 'p':
                                elem.type = 's'
                                if soundON == True:
                                    audio['s'].play()
                                # elem.isDead = True
                self.vel += attraction*dt
    def blit(self)->None:
        # if self.isDead == True:
        #     return
        if self.type == 'r':
            screen.blit(rock, [self.pos[0]-obj.rfactor*0.375, self.pos[1]-obj.rfactor*0.375])
        elif self.type == 'p':
            screen.blit(paper, [self.pos[0]-obj.rfactor*0.375, self.pos[1]-obj.rfactor*0.375])
        elif self.type == 's':
            screen.blit(scissor, [self.pos[0]-obj.rfactor*0.375, self.pos[1]-obj.rfactor*0.375])


        
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
def sign(n):
    return +1 if n>=0 else -1
rock = pygame.transform.scale(pygame.image.load("images/rock.png"), [obj.rfactor*0.75, obj.rfactor*0.75])
paper = pygame.transform.scale(pygame.image.load("images/paper.png"), [obj.rfactor*0.75, obj.rfactor*0.75])
scissor = pygame.transform.scale(pygame.image.load("images/scissor.png"), [obj.rfactor*0.75, obj.rfactor*0.75])

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
    # for i in range(150):
    #     objects.append(obj(random.choice(['r', 'p', 's']), [random.random()*screenRes[0], random.random()*screenRes[1]], [(0.5-random.random())*50, (0.5-random.random())*50], 0))
    for i in range(50):
        objects.append(obj('r', [random.random()*screenRes[0], random.random()*screenRes[1]], [(0.5-random.random())*50, (0.5-random.random())*50], 0))
    for i in range(50):
        objects.append(obj('p', [random.random()*screenRes[0], random.random()*screenRes[1]], [(0.5-random.random())*50, (0.5-random.random())*50], 0))
    for i in range(50):
        objects.append(obj('s', [random.random()*screenRes[0], random.random()*screenRes[1]], [(0.5-random.random())*50, (0.5-random.random())*50], 0))
    running = True
    clock = pygame.time.Clock()
    while running == True:
        initTime = time.time()
        clock.tick(frameRate*1.269)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(frameRate)
                soundON = not soundON
            if event.type == pygame.QUIT:
                running = False
        #Code Here
        screen.fill((10, 10, 10))
        obj.accelType['r'] = pygame.math.Vector2([(0.5-random.random())*2000, (0.5-random.random())*2000])
        obj.accelType['p'] = pygame.math.Vector2([(0.5-random.random())*2000, (0.5-random.random())*2000])
        obj.accelType['s'] = pygame.math.Vector2([(0.5-random.random())*2000, (0.5-random.random())*2000])
        for i in objects:
            i.blit()
            i.update(dt)
            i.convert(dt)

        pygame.display.update()
        endTime = time.time()
        dt = endTime-initTime
        if dt != 0:
            frameRate = 1/dt
        else:
            frameRate = 1000
