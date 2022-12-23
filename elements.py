import pygame, os, random

SCREEN_SIZE = WIDTH, HEIGHT = 500, 400

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
        self.hits =0


    def draw(self, SCREEN):
        SCREEN.blit(self.image,(self.pos.x,self.pos.y))
        pygame.draw.rect(SCREEN, self.color, (self.pos.x,self.pos.y,self.image.get_width(),self.image.get_height()),1)

    def update(self):
        if self.move_right:
            self.move(DIRECTION='RIGHT')
            #reset
            self.move_right = not self.move_right
        if self.move_left:
            self.move(DIRECTION='LEFT')
            self.move_left = not self.move_left
    
    def move(self,DIRECTION):
        
        increment_x = 10
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
        r = [s for s in range(-3,3)]
        r.remove(0)
        self.vel_x = random.choice(r)
        self.vel_y = random.choice(r)
        self.vel_muliplier_x = 3
        self.vel_muliplier_y = 3
        self.pos = pygame.Rect(self.pos_x,self.pos_y,img.get_width(),img.get_height())
        self.foul = False
        self.angle = 0
        self.old_pos = self.pos

    def draw(self, SCREEN):
        SCREEN.blit(self.image,(self.pos.x,self.pos.y))
        
    def get_slope(self,old,new):

        try:

            return (new[1]-old[1])/(new[0]-old[0])
        except ZeroDivisionError:
            return 0

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

        self.old_pos = self.pos.copy()

        self.pos.y += self.vel_y * self.vel_muliplier_y
        self.pos.x += self.vel_x * self.vel_muliplier_x
        
        self.angle = self.get_slope(self.old_pos.center,self.pos.center)
