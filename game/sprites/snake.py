import pygame
import config
import random
import measurement
import direction
from sprites.snakenode import SnakeNode
from game_grid import GameGrid


class Snake:
    def __init__(self, gameDisplay, initPosition, snakeLength, vector, on_collision):
        self.gameDisplay = gameDisplay
        self.on_collision = on_collision
        self.moves_taken = 0

        # Initialize head
        # self.headDirection = random.choice((direction.DOWN, direction.UP, direction.LEFT, direction.RIGHT))
        self.headDirection = direction.RIGHT
        self.head = SnakeNode(self.gameDisplay, self.headDirection,
                              (initPosition[0], initPosition[1]), True)

        # Initialize Game vector
        self.vector = vector
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
        possible = self.headDirection != direction.LEFT
        if not (self.headDirection == direction.RIGHT or self.headDirection == direction.LEFT):
            self.headDirection = direction.RIGHT
        return possible

    def turnLeft(self):
        possible = self.headDirection != direction.RIGHT
        if not (self.headDirection == direction.RIGHT or self.headDirection == direction.LEFT):
            self.headDirection = direction.LEFT
        return possible

    def turnDown(self):
        possible = self.headDirection != direction.UP
        if not (self.headDirection == direction.UP or self.headDirection == direction.DOWN):
            self.headDirection = direction.DOWN
        return possible

    def turnUp(self):
        possible = self.headDirection != direction.DOWN
        if not (self.headDirection == direction.UP or self.headDirection == direction.DOWN):
            self.headDirection = direction.UP
        return possible

    def draw(self):

        # Handle keyboard pressed scenario
        # key = pygame.key.get_pressed()
        # if key[pygame.K_RIGHT] and not (self.headDirection == (-1, 0)):
        #     self.headDirection = (1, 0)
        # elif key[pygame.K_LEFT] and not (self.headDirection == (1, 0)):
        #     self.headDirection = (-1, 0)
        # elif key[pygame.K_DOWN] and not (self.headDirection == (0, -1)):
        #     self.headDirection = (0, 1)
        # elif key[pygame.K_UP] and not (self.headDirection == (0, 1)):
        #     self.headDirection = (0, -1)

        collision = self._check_body_collision()
        self._unpin_last_node()
        for i in range(len(self.snakeNodes) - 1, 0, -1):
            self.snakeNodes[i].setDirection(self.snakeNodes[i - 1].direction)
            self.snakeNodes[i].move()
            self.snakeNodes[i].draw()

        self.head.setDirection(self.headDirection)
        self.head.move()
        self.head.draw()
        self._pin_head()
        collision = collision or self._check_border_collision()
        if not collision:
            self.moves_taken += 1
            if self.moves_taken > config.MAX_MOVES_REQUIRED_FOR_FOOD:
                self.on_collision(self, -10000)
                return True
        return collision

    def _check_body_collision(self):
        self_collision = pygame.sprite.spritecollide(
            self.head, self.snakeNodeGroup, False)
        if self_collision:
            # Game Over
            self.on_collision(self)
            return True
        return False

    def _check_border_collision(self):
        if self.head.x >= measurement.MAX_RIGHT or self.head.x <= measurement.MAX_LEFT or self.head.y >= measurement.MAX_BOTTOM or self.head.y <= measurement.MAX_TOP:
            # Game Over
            self.on_collision(self)
            return True
        return False

    def _unpin_last_node(self):
        lastNode = self.snakeNodes[-1]
        self.vector.unpin(lastNode.x, lastNode.y)

    def _pin_head(self):
        self.vector.pin(self.head.x, self.head.y)

    def distance_from_border_collision(self):
        if self.headDirection == direction.UP:
            return self.head.y // measurement.SNAKE_NODE_HEIGHT
        elif self.headDirection == direction.DOWN:
            return measurement.GRID_LENGTH_Y - self.head.y // measurement.SNAKE_NODE_HEIGHT
        elif self.headDirection == direction.LEFT:
            return measurement.GRID_LENGTH_X - self.head.x // measurement.SNAKE_NODE_WIDTH
        else:
            return self.head.x // measurement.SNAKE_NODE_WIDTH

    def distance_from_self_collision(self):
        if self.headDirection == direction.LEFT or self.headDirection == direction.RIGHT:
            i = GameGrid.dimension_index_x(self.head.x) + self.headDirection[0]
            while i >= 0 and i < measurement.GRID_LENGTH_X:
                if self.vector.at(i, GameGrid.dimension_index_y(self.head.y)) == 1:
                    return abs(GameGrid.dimension_index_x(self.head.x) - i)
                i += self.headDirection[0]

        if self.headDirection == direction.UP or self.headDirection == direction.DOWN:
            i = GameGrid.dimension_index_y(self.head.y) + self.headDirection[1]
            while i >= 0 and i < measurement.GRID_LENGTH_Y:
                if self.vector.at(GameGrid.dimension_index_x(self.head.x), i) == 1:
                    return abs(GameGrid.dimension_index_y(self.head.y) - i)
                i += self.headDirection[1]

        return -1
