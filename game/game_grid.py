import measurement
import random
from pprint import pprint


class GameGrid:
    def __init__(self):
        self.gameVector = [[0 for i in range(measurement.GRID_LENGTH_X)] for j in range(
            measurement.GRID_LENGTH_Y)]
        self.not_occupied = {(i, j) for i in range(
            measurement.GRID_LENGTH_X) for j in range(measurement.GRID_LENGTH_Y)}

    def pin(self, x, y):
        gridX = x // measurement.SNAKE_NODE_WIDTH
        gridY = y // measurement.SNAKE_NODE_HEIGHT
        if (gridX > -1 and gridY > -1 and gridX < measurement.GRID_LENGTH_X and gridY < measurement.GRID_LENGTH_Y) and (gridX, gridY) in self.not_occupied:
            self.gameVector[gridY][gridX] = 1
            self.not_occupied.remove((gridX, gridY))

    def unpin(self, x, y):
        gridX = x // measurement.SNAKE_NODE_WIDTH
        gridY = y // measurement.SNAKE_NODE_HEIGHT
        if (gridX > -1 and gridY > -1 and gridX < measurement.GRID_LENGTH_X and gridY < measurement.GRID_LENGTH_Y):
            self.gameVector[gridY][gridX] = 0
            self.not_occupied.add((gridX, gridY))

    def any_not_occupied(self):
        return random.choice(tuple(self.not_occupied))

    def get_raw(self):
        return [item for sublist in self.gameVector for item in sublist]

    def print(self):
        for a in self.gameVector:
            x = ""
            for b in a:
                x = x + ", " + str(b)
            print(x)
        print("\n\n")
