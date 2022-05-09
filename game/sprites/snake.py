import pygame
import measurement
from sprites.snakenode import SnakeNode
from game_grid import GameGrid

# Directions :
# movement in (x, y)
# right : (1, 0)
# left : (-1, 0)
# up : (0, -1)
# down : (0, +1)

class Snake:
    def __init__(self, gameDisplay, initPosition, snakeLength):
        self.gameDisplay = gameDisplay

        # Initialize head
        self.headDirection = (1, 0)
        self.head = SnakeNode(self.gameDisplay, (1, 0), (initPosition[0], initPosition[1]), True)

        # Initialize Game vector
        self.vector = GameGrid()
        self.vector.pin(initPosition[0], initPosition[1])

        # Initialize rest of the body
        self.snakeNodes = [self.head]
        self.snakeNodeGroup = pygame.sprite.Group()
        for i in range(snakeLength - 1):
            self.addToSnake()
        
    def addToSnake(self):
        tailPos = self.snakeNodes[-1]
        nodePosX = tailPos.x - tailPos.direction[0] * tailPos.width
        nodePosY = tailPos.y - tailPos.direction[1] * tailPos.height
        newTail = SnakeNode(
            self.gameDisplay, 
            tailPos.direction,
            (nodePosX, nodePosY),
            False
        )
        self.snakeNodes.append(newTail)
        self.snakeNodeGroup.add(newTail)
        self.vector.pin(nodePosX, nodePosY)

    def turnRight(self):
        if not not (self.headDirection == (-1, 0)):
            self.headDirection = (1, 0)

    def turnLeft(self):
        if not (self.headDirection == (1, 0)):
            self.headDirection = (-1, 0)

    def turnDown(self):
        if not (self.headDirection == (0, -1)):
            self.headDirection = (0, 1)
    
    def turnUp(self):
        if not (self.headDirection == (0, 1)):
            self.headDirection = (0, -1)

    def draw(self):
        # key = pygame.key.get_pressed()
        # if key[pygame.K_RIGHT] and not (self.headDirection == (-1, 0)):
        #     self.headDirection = (1, 0)
        # elif key[pygame.K_LEFT] and not (self.headDirection == (1, 0)):
        #     self.headDirection = (-1, 0)
        # elif key[pygame.K_DOWN] and not (self.headDirection == (0, -1)):
        #     self.headDirection = (0, 1)
        # elif key[pygame.K_UP] and not (self.headDirection == (0, 1)):
        #     self.headDirection = (0, -1)

        self._check_body_collision()
        self._unpin_last_node()
        for i in range(len(self.snakeNodes) - 1, 0, -1):
            self.snakeNodes[i].setDirection(self.snakeNodes[i - 1].direction)
            self.snakeNodes[i].move()
            self.snakeNodes[i].draw()

        self.head.setDirection(self.headDirection)
        self.head.move()
        self.head.draw()
        self._pin_head()
        self._check_border_collision()

    def _check_body_collision(self):
        self_collision = pygame.sprite.spritecollide(self.head, self.snakeNodeGroup, False)
        if self_collision:
            # Game Over
            pygame.quit()

    def _check_border_collision(self):
        if self.head.x >= measurement.MAX_RIGHT or self.head.x <= measurement.MAX_LEFT or self.head.y >= measurement.MAX_BOTTOM or self.head.y <= measurement.MAX_TOP:
            # Game Over
            pygame.quit()

    def _unpin_last_node(self):
        lastNode = self.snakeNodes[-1]
        self.vector.unpin(lastNode.x, lastNode.y)

    def _pin_head(self):
        self.vector.pin(self.head.x, self.head.y)
