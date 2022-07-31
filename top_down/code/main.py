import pygame, sys
import time
from settings import *
from level import *

class Game:
    def __init__(self):
        
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Game Mechanics')
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        previous_time = time.time()
        while True:
            # delta time -- frame independence
            dt = time.time() - previous_time
            previous_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            

            self.screen.fill('black')
            self.level.run(dt)
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run() 