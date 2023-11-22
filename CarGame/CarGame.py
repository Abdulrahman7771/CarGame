import pygame
import pygame_widgets
from pygame_widgets.button import Button
from random import randint
import time
import os
from os.path import exists

sourceFileDir = os.path.dirname(os.path.abspath(__file__))

sprites = ["enemy1.png","enemy2.png","enemy3.png","enemy4.png"]

class sprite(pygame.sprite.Sprite):
    def __init__(self,img,pos,screen,layer):
        path = os.path.join(sourceFileDir , "assets", img)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos
        #pygame.draw.rect(self.image,"red",[0,0,self.rect.width,self.rect.height],5)
        screen.blit(self.image,self.rect)
        self._layer = layer

class car(sprite):
    def __init__(self,img,pos,screen,layer):
        super().__init__(img,pos,screen,layer)
        self.CollisionRect = self.rect.copy()
        self.CollisionRect.center = pygame.Vector2(pos.x+15,pos.y+15)
        self.CollisionRect.width -= 30
        self.CollisionRect.height -= 40
        #pygame.draw.rect(self.image,"green",[15,15,self.CollisionRect.width,self.CollisionRect.height],5)
    def update(self,pos):
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.CollisionRect.center = pygame.Vector2(pos.x+15,pos.y+15)
        #pygame.draw.rect(self.image,"green",[15,15,self.CollisionRect.width,self.CollisionRect.height],5)
        #pygame.draw.rect(self.image,"red",[0,0,self.rect.width,self.rect.height],5)
        screen.blit(self.image,self.rect)
        
class Enemy(sprite):
    def __init__(self,img,pos,screen,group,layer,speed):
        super().__init__(img,pos,screen,layer)
        self.speed = speed
        self.pos = pos
        pygame.sprite.Sprite.__init__(self,group)
    def update(self,lose):
        self.rect = self.image.get_rect()
        if(not lose):
            self.pos.y += (self.speed)*dt
        self.rect.center = self.pos
        #pygame.draw.rect(self.image,"red",[0,0,self.rect.width,self.rect.height],5)
        screen.blit(self.image,self.rect)
        self.reset()
    def reset(self):
        if(self.rect.y>=screen.get_height()):
            pygame.sprite.Sprite.__init__(self)
            path = os.path.join(sourceFileDir , "assets", sprites[randint(0,3)])
            self.image = pygame.image.load(path).convert_alpha()
            self.rect = self.image.get_rect()
            self.pos = pygame.Vector2(randint(int(x+50),int(lx)),-300)
            self.rect.center = self.pos
            #pygame.draw.rect(self.image,"red",[0,0,self.rect.width,self.rect.height],5)
            screen.blit(self.image,self.rect)
            self.speed = randint(int(1),int(2))
    def GetSpeed(self):
        return self.speed
    def SetSpeed(self,s):
        self.speed = s
    def SetPos(self,p):
        self.pos.x +=p
        
if(not(exists("score.txt"))):
            with open("score.txt", "w") as f:
                f.write("0")
            f.close()
            
pygame.init()

running = True
lost=False
CanModifyScore = True

dt = 0
score = 0
HighScore = 0

performance = "Good game"

clock = pygame.time.Clock()
StartTime = time.time()
screen = pygame.display.set_mode()  
roadpath = os.path.join(sourceFileDir , "assets", "road.png")
road = pygame.image.load(roadpath).convert()
pygame.draw.rect(road,"red",[0,0,road.get_rect().width,road.get_rect().height],5)
screen.blit(road,((screen.get_width() / 2 )-(road.get_width()/2), -10))
myfont = pygame.font.SysFont("monospace", 24)

def end():
    global running
    running = False


x = ((int(screen.get_width() / 2 ))-(int(road.get_width()/2))) + 100
lx = (x + road.get_width()) -300

PPos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 1.2)
player = car("player7.png",PPos,screen,1)

group = pygame.sprite.LayeredUpdates()
enemy0 = Enemy(sprites[randint(0,3)],pygame.Vector2(randint(int(x+50),int(lx)),randint(-400,-100)),screen,group,0,2)
enemy1 = Enemy(sprites[randint(0,3)],pygame.Vector2(randint(int(x+50),int(lx)),randint(-400,-100)),screen,group,0,3)
enemy2 = Enemy(sprites[randint(0,3)],pygame.Vector2(randint(int(x+50),int(lx)),randint(-400,-100)),screen,group,0,1)
enemy3 = Enemy(sprites[randint(0,3)],pygame.Vector2(randint(int(x+50),int(lx)),randint(-400,-100)),screen,group,0,2)
enemy4 = Enemy(sprites[randint(0,3)],pygame.Vector2(randint(int(x+50),int(lx)),randint(-400,-100)),screen,group,0,2)


while running:
    screen.fill("green")
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                if(lost):
                    running = False
            if event.key == pygame.K_r:
                if(lost):
                    pass

    screen.blit(road,((screen.get_width() / 2 )-(road.get_width()/2), -10))
    
    player.update(PPos)
    group.update(lost)
    group.draw(screen)
    
    coll = player.CollisionRect.collidelist(group.get_sprites_from_layer(0))
    if(coll != -1):
        lost = True

    if(not lost):
        keys = pygame.key.get_pressed()     
        if keys[pygame.K_a]:
            if(not((player.rect.x - (7 * dt))<=x)):
                PPos.x -= 7 * dt
        if keys[pygame.K_d]:
            if(not((player.rect.x + (7 * dt))>=lx)):
                PPos.x += 7 * dt
        enemies = group.sprites()
        for i, e1 in enumerate(enemies):
            for e2 in enemies[i+1:]:
                if pygame.sprite.collide_mask(e1, e2):
                    if(e1.rect.y<=e2.rect.y):
                        orspeed = e1.GetSpeed()
                        e1.SetSpeed(1)
                        if(e1.rect.x<=e2.rect.x):
                            if((e1.rect.x - 1 )>=x):
                                e1.SetPos(-1)
                        else:
                            if((e1.rect.x + 1 )<=lx):
                                e1.SetPos(1)   
                        e1.SetSpeed(orspeed)
                    else:
                        orspeed = e2.GetSpeed()
                        e2.SetSpeed(1)
                        if(e2.rect.x<=e1.rect.x):
                            if((e2.rect.x - 1 )>=x):
                                e2.SetPos(-1)
                        else:
                            if((e2.rect.x + 1 )<=lx):
                                e2.SetPos(1)   
                        e2.SetSpeed(orspeed)
        score = int((time.time() - StartTime))
    else:
        if(CanModifyScore):
            with open("score.txt", "r") as f:
                HighScore = f.read()
                f.close()
            with open("score.txt", "w") as f:
                if(int(HighScore)<score):
                    f.write(f"{score}")
                    if(score>int(HighScore)):
                        performance = "Great Game"
                    else:
                        performance = "Good Game"
                    HighScore = score
                else:
                    f.write(f"{HighScore}")
                f.close()
            CanModifyScore = False
        EndGameText = myfont.render(f"{performance} Score: {score}", 0, "red")
        HighText = myfont.render(f"HighScore: {HighScore}", 0, "red")
        congrats = myfont.render(f"Better luck next time", 0, "red")
        button = Button(
            screen, (screen.get_width() / 2),
            (screen.get_height()/2)
            , 200, 50, text='Quit',
            fontSize=24, margin=10,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick= lambda: end()
        )
        RecPivot = ((EndGameText.get_height()+HighText.get_height()+congrats.get_height()+button.getHeight())/2)
        button.setX(button.getX()-(button.getWidth()/2))
        button.setY(button.getY()-(button.getHeight())+RecPivot)
        pygame.draw.rect(screen,"#00FFB9"
                        ,[(screen.get_width() / 2)-(congrats.get_width()/2), (screen.get_height()/2) - RecPivot
                        ,congrats.get_width(),EndGameText.get_height()*3+button.getHeight()],0)
        screen.blit(EndGameText, ((screen.get_width() / 2)-(EndGameText.get_width()/2), (screen.get_height()/2)-RecPivot))
        screen.blit(HighText, ((screen.get_width() / 2)-(HighText.get_width()/2), (screen.get_height()/2)-RecPivot+EndGameText.get_height()))
        screen.blit(congrats, ((screen.get_width() / 2)-(congrats.get_width()/2), (screen.get_height()/2)-RecPivot+EndGameText.get_height()+HighText.get_height()))
        pygame_widgets.update(events)

    scoretext = myfont.render(f"Score: {score}", 0, "red")
    pygame.draw.rect(screen,"#00FFB9",[50,25,scoretext.get_width(),scoretext.get_height()],0)
    screen.blit(scoretext, (50, 25))
    
    pygame.display.update()
    
    dt = clock.tick(30) / 10
    
pygame.quit()