
import time
import os
import sys
import pytoml as toml
import signal
import threading
from engine import *
from resource import *


def get_requires(config):
    if 'main' in config and 'require' in config['main']:
        return config['main']['require']
    return []

def merge_config(config, required_config):
    for key, value in required_config.items():
        if key == '__filename__':
            continue
        if key not in config:
            config[key] = value
        else:
            print(key, config[key])
            config[key].update(value)
    return config

def load_config(filename) -> dict:
    """
    Read toml into config dict.
    """
    with open(filename, "rb") as file:
        config = toml.load(file)
    return config


def load_configs() -> list:
    """
    Read toml files into a list of config.
    """    
    config_path_base = "../conf/"
    with open(config_path_base + "select.toml", "rb") as file:
        config = toml.load(file)
        # print(config)

    config_path = config_path_base + config['path']
    if not os.path.exists(config_path):
        return []
    
    # Load all the toml files
    config_map = dict()
    for fs in os.walk(config_path):
        for file in fs[2]:
            # Ignore the unused toml files
            if file.startswith('!'):
                continue

            config = load_config(os.path.join(fs[0], file))
            config['__filename__'] = file
            config_map[file] = config
    
    # Handle required sub toml config
    for file, config in config_map.items():
        requires = get_requires(config)
        if len(requires) > 0:
            for require in requires:
                print("require!!!", require)
                merge_config(config, config_map[require])

    return config_map.values()

def flush_all_logs():
    pass

def exit_handler(signum, frame):
    """
    Quit all the threads when Ctrl+C
    """
    flush_all_logs()
    sys.exit()


def main(configs):
    """
    """
    print("Main-ThreadId:", threading.get_ident())
    signal.signal(signal.SIGINT, exit_handler)
    Clock.tick()
    
    for config in configs:
        if config['__filename__'] == 'global.toml':
            Resource.initialize_global_resources(config)

    for config in configs:
        # Ignore the global resource file
        if config['__filename__'] == 'global.toml':
            continue

        if 'main' not in config:    # required toml would NOT have main section
            continue
        
        print(config)
        e = Engine(config)
        e.start()

if __name__ == '__main__':
    configs = load_configs()
    for config in configs:
        print('-' * 40)
        print(config)
        print('-' * 40)

    main(configs)
