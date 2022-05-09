import pygame
import config
from sprites.snake import Snake
from sprites.food import Food
import utils

class Environment:

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.gameOver = False
        self.snake = Snake(self.gameDisplay, (config.DISPLAY_WIDTH // 2, config.DISPLAY_WIDTH // 2), config.INITIAL_SNAKE_LENGTH)
        self.food = Food(self.gameDisplay, self.snake)
        self.score = 0
        

    def loop_game(self):
        # Draw Snake
        self.snake.draw()
        self.food.draw()
        pygame.display.set_caption(f"Snake AI, Score: {self.score}")
        if (self.food.isConsumed()):
            self.food = Food(self.gameDisplay, self.snake)
            self.snake.addToSnake()
            self.score += 1