import pygame,os, sys, re
from elements import Pong, Ball, SCREEN_SIZE, WIDTH, HEIGHT
import neat, random

pygame.init()

SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Pong')
FONT = pygame.font.Font('freesansbold.ttf', 20)

def remove(index):
    pongs.pop(index)
    ge.pop(index)
    nets.pop(index)

def get_max_checkpoint():
    local_dir = os.path.dirname(__file__)
    try:
        last_check_point = max([int(f.split('point-')[1]) for f in os.listdir(local_dir) if re.match(r'neat-checkpoint+.*', f)])
    except ValueError:
        return None
    print(f'Found neat-checkout-{last_check_point}')
    return 'neat-checkpoint-'+str(last_check_point)

def random_velocity_change(velocity):

    rx = [0 for _ in range(50)]+[1]
    ry = [0 for _ in range(100)]+[1]

    if random.choice(rx) == 1: return velocity+0.01
    if random.choice(ry) == 1: return velocity+0.1
    return velocity

def eval_genomes(genomes,config):

    global points, pongs, ge, nets, game_speed
    points = 1
    game_speed = 1

    clock = pygame.time.Clock()

    # pong = Pong()
    ball = Ball()

    def score():
        global points, game_speed
        points+=1
        if points % 100 ==0:
            game_speed+=1
        text = FONT.render(f'Points:  {str(game_speed)}', True, (0, 0, 0))
        SCREEN.blit(text, (5, HEIGHT-40))


    pongs = []
    ge = []
    nets = []

    for genome_id,genome in genomes:
        pongs.append(Pong())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nets.append(net)
        genome.fitness = 0
        
    def statistics():
        global pongs
        text_1 = FONT.render(f'Pongs Alive:  {str(len(pongs))}', True, (0, 0, 0))
        text_2 = FONT.render(f'Generation:  {pop.generation+1}', True, (0, 0, 0))
        # text_3 = FONT.render(f'Game Speed:  {str(game_speed)}', True, (0, 0, 0))

        SCREEN.blit(text_1, (5, HEIGHT-60))
        SCREEN.blit(text_2, (5, HEIGHT-80))
        # SCREEN.blit(text_3, (50, 510))

    RUN = True
    while RUN:
        SCREEN.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for pong in pongs:
            pong.update()
            pong.draw(SCREEN)

        for i, pong in enumerate(pongs):
            output = nets[i].activate((
                                    ball.pos.midbottom[1],
                                    pong.pos.midtop[0] - ball.pos.midbottom[0],
                                    ball.angle
                                ))
            if output[0] > 0.5:
                pong.move_right = True
            if output[1] > 0.5:
                pong.move_left = True
        

        ball.update()

        for i,pong in enumerate(pongs):
            if ball.pos.left >= pong.pos.left and ball.pos.right <= pong.pos.right and ball.pos.bottom >= pong.pos.top:
                ball.vel_y*=-1
                ge[i].fitness += 1
                pong.hits+=1

            if (ball.pos.left >= pong.pos.left or ball.pos.right <= pong.pos.right) and ball.pos.bottom >= pong.pos.bottom:
                ge[i].fitness -= 1
                remove(i)

            
            if ball.pos.y > HEIGHT:
                break
            
            # Remove pongs which have not scored any poitns
            if game_speed > 10 and pong.hits == 0:
                ge[i].fitness -= 1
                remove(i)


        if len(pongs) == 0: RUN=False; points=1

        ball.draw(SCREEN)

        score()
        statistics()

        clock.tick(60)
        pygame.display.update()


# Setup the NEAT Neural Network
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    if get_max_checkpoint() != None:
        pop = neat.Checkpointer.restore_checkpoint(get_max_checkpoint())
        print('Checkout point found, resuming')
    else:
        print('No checkpoint found, Creating new population')
        pop = neat.Population(config)
    

    # Add stoud reported to show progress in the terminal
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(20))

    pop.run(eval_genomes,200)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)