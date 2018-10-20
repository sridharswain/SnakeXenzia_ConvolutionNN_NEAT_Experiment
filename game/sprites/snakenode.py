import pygame
from utils import colors

class SnakeNode:
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.width = 16
        self.height = 16

    def drawAt(self, x, y):
        pygame.draw.rect(self.gameDisplay, colors["black"], (x, y, self.width, self.height))