import pygame
import measurement
from utils import colors
from game_grid import GameGrid

class SnakeNode(pygame.sprite.Sprite):
    def __init__(self, gameDisplay, direction, position, isHead):
        pygame.sprite.Sprite.__init__(self)
        self.gameDisplay = gameDisplay
        self.width = measurement.SNAKE_NODE_WIDTH
        self.height = measurement.SNAKE_NODE_HEIGHT
        self.direction = direction
        self.x = position[0]
        self.y = position[1]
        self.moveSpeed = self.width
        self.isHead = isHead
        self.draw()

    def drawAt(self, x, y):
        self.rect = pygame.draw.rect(self.gameDisplay, colors["black"], (x, y, self.width, self.height))
        self.x = x
        self.y = y

    def draw(self):
        self.rect = pygame.draw.rect(self.gameDisplay, colors["black"], (self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.direction[0] * self.moveSpeed
        self.y += self.direction[1] * self.moveSpeed


    def setDirection(self, direction):
        self.direction = direction