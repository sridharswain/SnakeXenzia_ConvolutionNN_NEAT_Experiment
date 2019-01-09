import pygame
from sprites.snakenode import SnakeNode

# Directions :
# movement in (x, y)
# right : (1, 0)
# left : (-1, 0)
# up : (0, -1)
# down : (0, +1)

class Snake:
    def __init__(self, gameDisplay, initPosition, snakeLength):
        self.gameDisplay = gameDisplay
        self.headDirection = (1, 0)

        head = SnakeNode(self.gameDisplay, (1, 0), (initPosition[0], initPosition[1]), True, False)
        self.snakeNodes = [head]
        for i in range(snakeLength):
            self.addToSnake()
        
    def addToSnake(self):
        tailPos = self.snakeNodes[-1]
        newTail = SnakeNode(
            self.gameDisplay, 
            tailPos.direction,
            ((tailPos.x - tailPos.direction[0] * tailPos.width,
            tailPos.y - tailPos.direction[1] * tailPos.height)),
            False,
            False
        )
        self.snakeNodes.append(newTail)

    def draw(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and not (self.headDirection == (-1, 0)):
            self.headDirection = (1, 0)
        elif key[pygame.K_LEFT] and not (self.headDirection == (1, 0)):
            self.headDirection = (-1, 0)
        elif key[pygame.K_DOWN] and not (self.headDirection == (0, -1)):
            self.headDirection = (0, 1)
        elif key[pygame.K_UP] and not (self.headDirection == (0, 1)):
            self.headDirection = (0, -1)

        for i in range(len(self.snakeNodes) - 1, 0, -1):
            self.snakeNodes[i].draw()
            self.snakeNodes[i].setDirection(self.snakeNodes[i - 1].direction)
            self.snakeNodes[i].move()

        self.snakeNodes[0].draw()
        self.snakeNodes[0].setDirection(self.headDirection)
        self.snakeNodes[0].move()