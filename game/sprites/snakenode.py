import pygame
from utils import colors

class SnakeNode:
    def __init__(self, gameDisplay, direction, position, isHead, isFood):
        self.gameDisplay = gameDisplay
        self.width = 10
        self.height = 10
        self.direction = direction
        self.x = position[0]
        self.y = position[1]
        self.moveSpeed = self.width
        self.isHead = isHead
        self.isFood = isFood

    def drawAt(self, x, y):
        self.node = pygame.draw.rect(self.gameDisplay, colors["black"], (x, y, self.width, self.height))
        self.x = x
        self.y = y

    def draw(self):
        self.node = pygame.draw.rect(self.gameDisplay, colors["black"], (self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.direction[0] * self.moveSpeed
        self.y += self.direction[1] * self.moveSpeed

    def setDirection(self, direction):
        self.direction = direction