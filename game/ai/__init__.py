import os
import neat
import pygame
import random
import visualize
from app import App
from ai.agent import Agent
from environment import Environment
from sprites.snake import Snake

FRAME_RATE = 80
# Start game with 40 frame rate.
app = App(FRAME_RATE)

gen = 0
high_score = 0


def evaluate_on_collision_callback(agent: Agent):
    def on_collision(snake: Snake):
        agent.genome.fitness -= 3
    return on_collision


def evaluate_on_food_consume_callback(agent: Agent):
    def on_food_consume(env: Environment):
        agent.genome.fitness += 5
    return on_food_consume


def evaluate_move_callback(agent: Agent):
    def evaluate_move(env: Environment):
        vector = env.vector
        input = (env.food.x, env.food.y, env.snake.head.x,
                 env.snake.head.y, *vector.get_raw())
        output = agent.net.activate(input)
        successful = False
        if output[0] < -0.5:
            successful = env.snake.turnDown()
        elif output[0] < 0:
            successful = env.snake.turnLeft()
        elif output[0] < 0.5:
            successful = env.snake.turnUp()
        else:
            successful = env.snake.turnRight()

        if (successful):
            agent.genome.fitness += 0.01

    return evaluate_move


def eval_genomes(genomes, config):
    global gen
    global high_score
    gen += 1

    agents = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        agents.append(Agent(config, genome, app.newEnvironment()))

    run = True
    food_position = agents[0].environment.vector.any_not_occupied()
    for agent in agents:
        agent.environment.initiate(evaluate_on_collision_callback(agent), food_position)
        collision = app.begin(agent.environment.loop_game,
                  evaluate_move=evaluate_move_callback(agent),
                  on_food_consume=evaluate_on_food_consume_callback(agent))
        high_score = max(high_score, agent.environment.score)
    print(f"Highest Score: {high_score}")


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 500)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=False)

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
