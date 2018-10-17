import pygame
import utils
from utils import colors

display_width = 1300  #DISPLAY
display_height = 500  #DIMENSIONS

class Game:
    def __init__(self, framerate):
        self.gameDisplay = pygame.display.set_mode((display_width,display_height))
        pygame.display.set_caption("Snake AI")
        self.clock = pygame.time.Clock()
        self.frameRate = framerate

    def updateFrame(self):
        self.clock.tick(self.frameRate)
    
    def startEnvironment(self):
        self.gameOver = False
        self.gameDisplay.fill((255, 255, 255))
        while not self.gameOver:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    self.gameOver = True
            self.gameDisplay.fill((255, 255, 255))
            self.updateFrame()
        pygame.quit()

game = Game(100)
game.startEnvironment()
