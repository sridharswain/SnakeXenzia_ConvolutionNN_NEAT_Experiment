from copyreg import constructor
import pygame
import measurement
from utils import colors
from pygame.sprite import Sprite
from sprites.snake import Snake

class Food(Sprite):
    def __init__(self, gameDisplay, snake: Snake, pos = None):
        pygame.sprite.Sprite.__init__(self)
        self.gameDisplay = gameDisplay
        self.width = measurement.SNAKE_NODE_WIDTH
        self.height = measurement.SNAKE_NODE_HEIGHT
        self.snake = snake
        self.x, self.y = pos if pos is not None else self.snake.vector.any_not_occupied()

    def draw(self):
         self.rect = pygame.draw.rect(self.gameDisplay, colors["black"], (self.x * measurement.SNAKE_NODE_WIDTH, self.y * measurement.SNAKE_NODE_HEIGHT, self.width, self.height))

    def isConsumed(self):
        consumed = self.rect.colliderect(self.snake.head)
        if consumed:
            self.snake.moves_taken = 0
        return consumed