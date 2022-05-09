import os
import neat
import pygame
from app import App
from ai.agent import Agent
from sprites.snake import Snake

FRAME_RATE = 25
# Start game with 40 frame rate.
app = App(FRAME_RATE)
app.begin()

gen = 0

def eval_genomes(genomes, config):
    global gen
    gen += 1

    agents = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        agents.append(Agent(config, genome, app.start()))


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
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    pygame.init()
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.abspath(local_dir + "/../neat_config.txt")
    run(config_path)