from xxlimited import foo
import neat
from environment import Environment

class Agent:
    def __init__(self, config, genome, environment: Environment, on_collision_callback, food_position = None):
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.environment = environment.initiate(on_collision_callback(self), food_position)
        nearest_reach_to_food = self.environment.distance_from_food()