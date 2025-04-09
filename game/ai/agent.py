from xxlimited import foo
import neat
from environment import Environment

class Agent:
    def __init__(self, config, genomeId, genome, environment: Environment, on_collision_callback, food_position = None):
        self.genome = genome
        self.genomeId = genomeId
        self.net = neat.nn.RecurrentNetwork.create(genome, config)
        self.environment = environment.initiate(on_collision_callback(self), food_position)