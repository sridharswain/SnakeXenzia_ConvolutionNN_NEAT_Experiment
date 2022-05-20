import os
import neat
import pygame
import random
import visualize
from app import App
from ai.agent import Agent
from environment import Environment
from sprites.snake import Snake
from game_grid import GameGrid

FRAME_RATE = 1000000000
# Start game with 160 frame rate.
app = App(FRAME_RATE)
stats = None
gen = 0
high_score = 0


def evaluate_on_collision_callback(agent: Agent):
    def on_collision(snake: Snake, reward = -10):
        agent.genome.fitness += reward
    return on_collision


def evaluate_on_food_consume_callback(agent: Agent):
    def on_food_consume(env: Environment):
        agent.genome.fitness += 20
        pass
    return on_food_consume


def evaluate_move_callback(agent: Agent):
    def evaluate_move(env: Environment):
        # dist_resiprocate = 100/env.distance_from_food() + 0.01
        agent.genome.fitness += 0.01

        # Activate Genome Net and get output
        vector = env.vector
        food_index = GameGrid.index(env.food.x, env.food.y)
        snake_head_index = GameGrid.index(env.snake.head.x, env.snake.head.y)
        distance_from_self_collision = env.snake.distance_from_self_collision()
        distance_from_border_collision = env.snake.distance_from_border_collision()
        snake_direction = env.snake.headDirection
        distance_from_food = env.distance_from_food()
        # print(f"Food Index : {food_index}, snake_head_index : {snake_head_index} distance_from_self_collision : {distance_from_self_collision}, distance_from_border_collision = {distance_from_border_collision} snake_direction : {snake_direction} distance_from_food : {distance_from_food}")
        input = (*food_index, *snake_head_index, distance_from_self_collision,
                 distance_from_border_collision, *snake_direction, distance_from_food)
        output = agent.net.activate(input)

        moved = False
        if output[0] < -0.6:
            moved = env.snake.turnDown()
        elif output[0] < -0.2:
            moved = env.snake.turnLeft()
        elif output[0] < 0.2:
            moved = env.snake.turnUp()
        elif output[0] < 0.6:
            moved = env.snake.turnRight()

    return evaluate_move


def eval_genomes(genomes, config):
    global gen
    global high_score
    gen += 1

    dummyEnv = app.newEnvironment().initiate(None, None)
    food_position = (dummyEnv.food.x, dummyEnv.food.y)
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        agent = Agent(config, genome, app.newEnvironment(),
                      evaluate_on_collision_callback, food_position)
        game_end = app.begin(agent.environment.loop_game,
                             evaluate_move=evaluate_move_callback(agent),
                             on_food_consume=evaluate_on_food_consume_callback(agent))
        high_score = max(high_score, agent.environment.score)

    print(f"Highest Score: {high_score}")


def run(config_file):
    global stats
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    #p = neat.Population(config)
    p = neat.Checkpointer.restore_checkpoint(os.path.abspath(local_dir + "/../neat-checkpoint-15527"))

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(100))

    # Run for up to 10000 generations.
    winner = p.run(eval_genomes, 1000000)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == 'ai':
    pygame.init()
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.abspath(local_dir + "/../neat_config.txt")
    run(config_path)
