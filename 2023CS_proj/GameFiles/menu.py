import pygame
# import sprite manager
from utils import load_sprite

class Menu:
    
    def __init__(self):
        self.__init__pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.bg = pygame.transform.scale(load_sprite("bg"), (800, 600))
        
        # Game Clock & Speed
        self.clock = pygame.time.Clock()
        self.fps = 60

    def __init__pygame(self):
        pygame.init()
        pygame.display.set_caption("Protect The Hive")
    
    def draw(self):
        self.screen.fill((0, 0, 255))
        self.screen.blit(self.bg, (0, 0))
        pygame.display.flip()
        self.clock.tick(60)

    def game_loop(self):
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.draw()



