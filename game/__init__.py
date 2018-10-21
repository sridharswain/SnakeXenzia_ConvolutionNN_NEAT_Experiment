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
        self.move_power = 10
        self.initSnakeLength = 10

    def updateFrame(self):
        pygame.display.update()
        self.clock.tick(self.frameRate)
    
    def startEnvironment(self):
        self.gameOver = False
        self.gameDisplay.fill((255, 255, 255))
        self.snake = Snake(self.gameDisplay, (display_width // 2, display_height//2), self.initSnakeLength)
        while not self.gameOver:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    self.gameOver = True
            self.gameDisplay.fill(colors["white"])
            self.snake.draw()
            self.updateFrame()
        pygame.quit()

game = Game(10)
game.startEnvironment()
