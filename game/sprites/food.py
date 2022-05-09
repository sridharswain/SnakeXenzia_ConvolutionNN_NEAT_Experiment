import pygame
import measurement
from utils import colors
from pygame.sprite import Sprite
from sprites.snake import Snake

class Food(Sprite):
    def __init__(self, gameDisplay, snake: Snake):
        pygame.sprite.Sprite.__init__(self)
        self.gameDisplay = gameDisplay
        self.width = measurement.SNAKE_NODE_WIDTH
        self.height = measurement.SNAKE_NODE_HEIGHT
        self.snake = snake
        self.x, self.y = self.snake.vector.any_not_occupied()

    def draw(self):
         self.rect = pygame.draw.rect(self.gameDisplay, colors["black"], (self.x * measurement.SNAKE_NODE_WIDTH, self.y * measurement.SNAKE_NODE_HEIGHT, self.width, self.height))

    def isConsumed(self):
        return self.rect.colliderect(self.snake.head)