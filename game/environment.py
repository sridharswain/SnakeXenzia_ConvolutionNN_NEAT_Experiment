import pygame
import config
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
        initPosition = (config.DISPLAY_WIDTH // 2, config.DISPLAY_HEIGHT // 2)
        self.snake = Snake(self.gameDisplay, initPosition, config.INITIAL_SNAKE_LENGTH, self.vector, on_collision)
        self.food = Food(self.gameDisplay, self.snake, food_position)
        
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