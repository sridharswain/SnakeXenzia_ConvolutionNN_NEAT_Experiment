import os
import ai
import pygame

# Determine path to configuration file. This path manipulation is
# here so that the script will run successfully regardless of the
# current working directory.
local_dir = os.path.dirname(__file__)
config_path = os.path.abspath(local_dir + "/neat_config.txt")
ai.run(config_path)