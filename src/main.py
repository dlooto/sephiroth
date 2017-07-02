
import time
import os
import sys
import pytoml as toml
import signal
import threading
from engine import *
from resource import *


def load_action_config(filename) -> dict:
    with open(filename, "rb") as file:
        config = toml.load(file)
        print(config)
    return config



def load_configs() -> list:
    config_path_base = "../conf/"
    with open(config_path_base + "select.toml", "rb") as file:
        config = toml.load(file)
        print(config)

    config_path = config_path_base + config['path']
    if not os.path.exists(config_path):
        return []
    
    # Load all the toml files
    configs = []
    for fs in os.walk(config_path):
        for file in fs[2]:
            # Ignore the unused toml files
            if file.startswith('!'):
                continue
            config = load_action_config(os.path.join(fs[0], file))
            config['filename'] = file
            configs.append(config)

    return configs

def exit_handler(signum, frame):
    """
    Quit all the threads when Ctrl+C
    """
    sys.exit()


def main(configs):
    """
    """
    print("Main-ThreadId:", threading.get_ident())
    signal.signal(signal.SIGINT, exit_handler)
    Clock.tick()
    
    for config in configs:
        if config['filename'] == 'global.toml':
            Resource.initialize_global_resources(config)
    for config in configs:
        # Ignore the global resource file
        if config['filename'] == 'global.toml':
            continue
        e = Engine(config)
        e.start()

if __name__ == '__main__':
    configs = load_configs()
    main(configs)
