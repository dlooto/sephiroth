
import time
import os
import sys
import pytoml as toml

from engine import *



def load_action_config(filename):
    with open(filename, "rb") as file:
        config = toml.load(file)
        print(config)
    return config

    

def load_configs():
    config_path_base = "../conf/"
    with open(config_path_base + "select.toml", "rb") as file:
        config = toml.load(file)
        print(config)

    config_path = config_path_base + config['path']
    if not os.path.exists(config_path):
        return []
    
    configs = []
    for fs in os.walk(config_path):
        for file in fs[2]:
            configs.append(load_action_config(os.path.join(fs[0], file)))
    # TODO: load all the toml files

    return configs

def main(configs):
    for config in configs:
        e = Engine(config)
        e.start()

if __name__ == '__main__':
    configs = load_configs()
    main(configs)
