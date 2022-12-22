import pygame, os, random

SCREEN_SIZE = WIDTH, HEIGHT = 400, 600

PongIMG = pygame.image.load(os.path.join('assets','Pong.png'))
BallIMG = pygame.image.load(os.path.join('assets','Ball.png'))

class Pong:

    def __init__(self, img=PongIMG,id=0):
        self.image = img
        self.pos_x = WIDTH/2
        self.pos_y = HEIGHT-img.get_height()-2
        self.move_right = False
        self.move_left = False
        self.pos = pygame.Rect(self.pos_x,self.pos_y,img.get_width(),img.get_height())
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))



    def draw(self, SCREEN):
        SCREEN.blit(self.image,(self.pos.x,self.pos.y))
        pygame.draw.rect(SCREEN, self.color, (self.pos.x,self.pos.y,self.image.get_width(),self.image.get_height()),1)

    def update(self):
        if self.move_right:
            self.move(DIRECTION='RIGHT')
        if self.move_left:
            self.move(DIRECTION='LEFT')
    
    def move(self,DIRECTION):
        increment_x = 8
        if DIRECTION=='RIGHT':
            if self.pos.right+increment_x <= WIDTH:
                self.pos.x = self.pos.x+increment_x
        if DIRECTION=='LEFT':
            if self.pos.left-increment_x >= 0:
                self.pos.x = self.pos.x-increment_x


class Ball:

    def __init__(self, img=BallIMG,id=0) -> None:
        self.image = img
        self.pos_x = WIDTH/4
        self.pos_y = HEIGHT/3
        self.vel_x = self.vel_y = -2
        self.pos = pygame.Rect(self.pos_x,self.pos_y,img.get_width(),img.get_height())
        self.foul = False

    def draw(self, SCREEN):
        SCREEN.blit(self.image,(self.pos.x,self.pos.y))
        
    @property
    def velocity(self):
        return (self.vel_x, self.vel_y)
    
    @velocity.setter
    def velocity(self,value):
        self.vel_x = value[0]
        self.vel_y = value[1]

    def update(self):
        self.move()
    
    def move(self):
        if self.pos.left <= 0:
            self.vel_x*=-1
        if self.pos.bottom >= HEIGHT:
            self.foul=True
        if self.pos.right >= WIDTH:
            self.vel_x*=-1
        if self.pos.top <=0:
            self.vel_y*=-1

        self.pos.y -= self.vel_y * 3
        self.pos.x -= self.vel_x * 3

        
