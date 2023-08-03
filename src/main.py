import pygame
import sys
from settings import *
from level import Level
 

class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('The Legend of Py')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.level.toggle_upgrade_menu()
                    if event.key == pygame.K_q:
                        self.level.toggle_quest_menu()
                    if event.key == pygame.K_c:
                        self.level.toggle_control_menu()

            self.screen.fill(EDGE_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
