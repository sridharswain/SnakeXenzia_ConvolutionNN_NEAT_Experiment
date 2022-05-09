import neat
from environment import Environment

class Agent:
    def __init__(self, config, genome, environment: Environment):
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.snake = environment