import pygame,os
from elements import Pong, Ball, SCREEN_SIZE, WIDTH, HEIGHT


pygame.init()

SCREEN = pygame.display.set_mode(SCREEN_SIZE)
FONT = pygame.font.Font('freesansbold.ttf', 20)

def main():

    global points
    points = 1

    clock = pygame.time.Clock()

    pong = Pong()
    ball = Ball()

    def score(velocity_tuple):
        global points
        if points % 10 == 0:
            velocity_tuple = (velocity_tuple[0]*1.1,velocity_tuple[1]*1.1)
        
        text = FONT.render(f'Points:  {str(points-1)}', True, (0, 0, 0))
        SCREEN.blit(text, (5, HEIGHT-40))
        return velocity_tuple


    RUN = True
    while RUN:
        SCREEN.fill((255,255,255))

        for event in pygame.event.get():
            
            # Enable game exit
            if event.type == pygame.QUIT:
                RUN = False
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LEFT: 
                    pong.move_right = False
                    pong.move_left = True
                elif event.key==pygame.K_RIGHT: 
                    pong.move_right = True
                    pong.move_left = False
            else:
                pong.move_right = False
                pong.move_left = False
        
        pong.update()
        ball.update()

        if ball.pos.left >= pong.pos.left and ball.pos.right <= pong.pos.right and ball.pos.bottom >= pong.pos.top:
            ball.vel_y*=-1
            points+=1

        
        if ball.pos.bottom >= pong.pos.bottom:
            RUN = False

        pong.draw(SCREEN)
        ball.draw(SCREEN)
        ball.velocity = score(ball.velocity)

        clock.tick(20)
        pygame.display.update()


if __name__ == '__main__':
    main()