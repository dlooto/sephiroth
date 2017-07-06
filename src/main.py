
import time
import os
import sys
import pytoml as toml
import signal
import threading
from engine import *
from resource import *

from actions import *

clz = Actions.get_action_class('read_file')
print(clz, clz())


def get_requires(config):
    """
    Get require sub toml files list
    """
    if 'main' in config and 'require' in config['main']:
        return config['main']['require']
    return []

def merge_config(config, required_config):
    """
    """
    for key, value in required_config.items():
        if key == '__filename__':
            continue
        if key not in config:
            config[key] = value
        else:
            config[key].update(value)


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
        main_config = toml.load(file)
        # print(config)

    config_path = config_path_base + main_config['path']
    if not os.path.exists(config_path):
        return []
    
    # Load all the toml files
    config_map = dict()
    for fs in os.walk(config_path):
        for file in fs[2]:
            # Ignore the unused toml files

            skip = False
            if 'exclude' in main_config:
                for exclude in main_config['exclude']:
                    if re.match(exclude, file):
                        skip = True
                        break

            if file.startswith('!') or skip:
                continue                

            config = load_config(os.path.join(fs[0], file))
            config['__filename__'] = file
            config_map[file] = config
    
    # Handle required sub toml config
    for file, config in config_map.items():
        requires = get_requires(config)
        if len(requires) > 0:
            for require in requires:
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
        
        # required toml would NOT have main section
        if 'main' not in config:
            continue
        
        # Start an engine with its config including main section only.
        e = Engine(config)
        e.start()

if __name__ == '__main__':
    configs = load_configs()
    main(configs)
