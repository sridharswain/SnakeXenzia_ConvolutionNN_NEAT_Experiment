import pygame
import config
from environment import Environment
from utils import colors

class App:
    def __init__(self, framerate):
        self.gameDisplay = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_WIDTH))
        pygame.display.set_caption("Snake AI")
        self.clock = pygame.time.Clock()
        self.frameRate = framerate
        self.environment = None

    """ Updates content on the screen.
        Called after bliting sprites on screen. """
    def updateFrame(self):
        pygame.display.update()
        self.clock.tick(self.frameRate)
    
    """Initiates Game loop.
        Game runtime in written here. """
    def begin(self, beforeFrame = None, afterFrame = None):
        self.gameDisplay.fill((255, 255, 255))
        while True:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    self.environment.gameOver = True
                    pygame.quit()
            self.gameDisplay.fill(colors["white"])
            if self.environment is None:
                continue
            if beforeFrame is not None:
                beforeFrame(self.environment)
            self.environment.loop_game()
            self.updateFrame()
            if afterFrame is not None:
                afterFrame(self.environment)

    def start(self):
        self.environment = Environment(self.gameDisplay)
        return self.environment

    def destroy(self):
        self.environment = None
