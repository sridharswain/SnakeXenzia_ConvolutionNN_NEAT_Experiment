from difflib import context_diff
import math
import pygame
import config
import random
import measurement
from sprites.snake import Snake
from sprites.food import Food
from game_grid import GameGrid

class Environment:

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.gameOver = False
        # Initialize Game vector
        self.vector = GameGrid()
        self.score = 0
        
    def initiate(self, on_collision, food_position = None):
        #initPosition = (config.DISPLAY_WIDTH // 2, config.DISPLAY_HEIGHT // 2)
        initPosition = (random.randint(config.INITIAL_SNAKE_LENGTH + 1, measurement.GRID_LENGTH_X - 1) * measurement.SNAKE_NODE_WIDTH, random.randint(0, measurement.GRID_LENGTH_Y - 1) * measurement.SNAKE_NODE_HEIGHT)
        self.snake = Snake(self.gameDisplay, initPosition, config.INITIAL_SNAKE_LENGTH, self.vector, on_collision)
        self.food = Food(self.gameDisplay, self.snake, food_position)
        return self

    def distance_from_food(self):
        if GameGrid.dimension_index_x(self.snake.head.x) == GameGrid.dimension_index_x(self.food.x):
            return abs(GameGrid.dimension_index_y(self.snake.head.y) - GameGrid.dimension_index_y(self.food.y))
        elif GameGrid.dimension_index_y(self.snake.head.y) == GameGrid.dimension_index_y(self.food.y):
            return abs(GameGrid.dimension_index_x(self.snake.head.x) - GameGrid.dimension_index_x(self.food.x))
        return -1
        
    def loop_game(self, evaluate_move = None, on_food_consume = None):
        if evaluate_move is not None:
            evaluate_move(self)

        # Draw Snake
        collision = self.snake.draw()
        self.food.draw()
        pygame.display.set_caption(f"Snake AI, Score: {self.score}")
        if (self.food.isConsumed()):
            if on_food_consume is not None:
                on_food_consume(self)
            self.food = Food(self.gameDisplay, self.snake)
            self.snake.addToSnake()
            self.score += 1
        return collision