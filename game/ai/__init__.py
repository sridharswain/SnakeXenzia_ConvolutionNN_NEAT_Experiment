import os
import neat
import pygame
import random
import direction
import visualize
from app import App
from ai.agent import Agent
from environment import Environment
from sprites.snake import Snake
from game_grid import GameGrid
import numpy as np

MAX_FOOD_DISTANCE = 113
DIRECTIONS = [direction.DOWN, direction.UP, direction.LEFT, direction.RIGHT]

FRAME_RATE = 100000000000
# Start game with 160 frame rate.
# pygame.init() # comment to remove display
app = App(FRAME_RATE)
stats = None
gen = 0
high_score = 0


def evaluate_on_collision_callback(agent: Agent):
    def on_collision(snake: Snake, reward = -2):
        agent.genome.fitness += reward
    return on_collision


def evaluate_on_food_consume_callback(agent: Agent):
    def on_food_consume(env: Environment):
        agent.genome.fitness += 2
    return on_food_consume


def evaluate_move_callback(agent: Agent):
    def evaluate_move(env: Environment):
        # dist_resiprocate = 100/env.distance_from_food() + 0.01

        # Activate Genome Net and get output
        vector = env.vector
        food_index = GameGrid.index(env.food.x, env.food.y)
        snake_head_index = GameGrid.index(env.snake.head.x, env.snake.head.y)
        distance_from_self_collision = env.snake.distance_from_self_collision()
        distance_from_border_collision = env.snake.distance_from_border_collision()
        snake_direction = env.snake.headDirection
        distance_from_food_x, distance_from_food_y, absolute_distance_from_food  = env.distance_from_food()
        # print(f"{agent.genomeId} Food Index : {food_index}, snake_head_index : {snake_head_index} distance_from_self_collision : {distance_from_self_collision}, distance_from_border_collision = {distance_from_border_collision} snake_direction : {snake_direction} distance_from_food : {absolute_distance_from_food}, coord: {distance_from_food_x}, {distance_from_food_y}")
        
        input = (*food_index, *snake_head_index, distance_from_self_collision,
                 distance_from_border_collision, *snake_direction, distance_from_food_x, distance_from_food_y)
        output = agent.net.activate(input)
        directionArg = np.argmax(output)


        moved = False
        if directionArg == 4:
            # For no operation
            moved = True
        else :
            directiontoMove = DIRECTIONS[directionArg]
            if directiontoMove == direction.DOWN:
                moved = env.snake.turnDown()
            elif directiontoMove == direction.LEFT:
                moved = env.snake.turnLeft()
            elif directiontoMove == direction.UP:
                moved = env.snake.turnUp()
            elif directiontoMove == direction.RIGHT:
                moved = env.snake.turnRight()
        
        if moved:
             reward_coefficient = 1 - (absolute_distance_from_food/MAX_FOOD_DISTANCE)
             agent.genome.fitness += (reward_coefficient * 0.1)
        else:
            agent.genome.fitness -= 1
    return evaluate_move


def eval_genomes(genomes, config):
    global gen
    global high_score
    gen += 1

    generation_high_score = 0

    dummyEnv = app.newEnvironment().initiate(None, None)
    food_position = (dummyEnv.food.x, dummyEnv.food.y)
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        agent = Agent(config, genome_id, genome, app.newEnvironment(),
                      evaluate_on_collision_callback, food_position)
        game_end = app.begin(agent.environment.loop_game,
                             evaluate_move=evaluate_move_callback(agent),
                             on_food_consume=evaluate_on_food_consume_callback(agent))
        high_score = max(high_score, agent.environment.score)
        generation_high_score = max(generation_high_score, agent.environment.score)

    print(f'Generation Highest Score: {generation_high_score}')
    print(f"Highest Score: {high_score}")


def run(config_file):
    global stats
    """
    runs the NEAT algorithm to train a neural network to play snake game.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    # p = neat.Population(config)

    local_dir = os.path.dirname(__file__)
    p = neat.Checkpointer.restore_checkpoint(os.path.abspath(local_dir + "/../../neat-checkpoint-1468"))

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(100))

    # Run for up to 10000 generations.
    winner = p.run(eval_genomes, 100000)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))
