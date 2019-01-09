import pygame
import utils
from sprites.snake import Snake
from utils import colors

display_width = 400  #DISPLAY
display_height = 400  #DIMENSIONS

class Game:
    def __init__(self, framerate):
        self.gameDisplay = pygame.display.set_mode((display_width,display_height))
        pygame.display.set_caption("Snake AI")
        self.clock = pygame.time.Clock()
        self.frameRate = framerate
        self.move_power = 20
        self.initSnakeLength = 10

    """ Updates content on the screen.
        Called after bliting sprites on screen. """
    def updateFrame(self):
        pygame.display.update()
        self.clock.tick(self.frameRate)
    
    """Initiates Game loop.
        Game runtime in written here. """
    def begin(self):
        self.gameOver = False
        self.gameDisplay.fill((255, 255, 255))
        self.snake = Snake(self.gameDisplay, (display_width // 2, display_height // 2), self.initSnakeLength)
        while not self.gameOver:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    self.gameOver = True
            self.gameDisplay.fill(colors["white"])
            self.snake.draw()
            self.updateFrame()
        pygame.quit()

# Start game with 40 frame rate.
game = Game(40)
game.begin()
