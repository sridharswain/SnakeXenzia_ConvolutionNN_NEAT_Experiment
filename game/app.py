import os
import pygame
import config
from environment import Environment
from utils import colors

class App:
    def __init__(self, framerate):
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.display.init()
        self.gameDisplay = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_WIDTH))
        pygame.display.set_caption("Snake AI")
        self.clock = pygame.time.Clock()
        self.frameRate = framerate

    """ Updates content on the screen.
        Called after bliting sprites on screen. """
    def updateFrame(self):
        pygame.display.update()
        self.clock.tick(self.frameRate)
    
    """Initiates Game loop.
        Game runtime in written here. """
    def begin(self, loop = None, evaluate_move = None, on_food_consume = None):
        self.gameDisplay.fill((255, 255, 255))
        while True:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    self.environment.gameOver = True
                    pygame.quit()
            self.gameDisplay.fill(colors["white"])
            if loop is not None:
                game_end = loop(evaluate_move, on_food_consume)
                if (game_end):
                    return True
            self.updateFrame()

    def newEnvironment(self):
        return Environment(self.gameDisplay)
