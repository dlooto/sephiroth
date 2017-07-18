
import os
import sys
import re
import pytoml as toml
import signal
import threading

import clock
import resource
import engine


#
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


def load_configs(work_path):
    """
    Read toml files into a list of config.
    """
    # Load __import__.toml first
    # If Not Unix absolute path, or Windows absolute path(c:/a/b)
    
    if not (work_path.startswith('/') or work_path[1] == ':'):
        work_path = os.path.join("../conf/", work_path)
    config_path = os.path.join(work_path, '__import__.toml')
    with open(config_path, "rb") as file:
        main_config = toml.load(file)
    
    # Load all the toml files
    config_map = dict()
    for fs in os.walk(work_path):
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
    clock.Clock.tick()
    
    for config in configs:
        if config['__filename__'] == 'global.toml':
            resource.Resource.initialize_global_resources(config)

    for config in configs:
        # Ignore the global resource file
        if config['__filename__'] == 'global.toml':
            continue
        
        # required .toml would NOT have main section
        if 'main' not in config:
            continue
        
        # Start an engine with its config including main section only.
        e = engine.Engine(config)
        e.start()


if __name__ == '__main__':
    work_path = ""
    if len(sys.argv) > 1:
        work_path = sys.argv[1]
    configs = load_configs(work_path)
    main(configs)
