
import os
import sys
import re

try:
    import pytoml as toml
except:
    print("Please `pip install pytoml`")
    exit()
import signal
import threading

import clock
import resource
import engine
from logger import *


logger = Logger("a.log").get_logger()

logger.info("start sephiroth")

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


def load_configs(config_path):
    """
    Read toml files into a list of config.
    """
    # Load __import__.toml first
    # If Not Unix absolute path, or Windows absolute path(c:/a/b)
    
    if not (config_path.startswith('/') or config_path[1] == ':'):
        config_path = os.path.join("../conf/", config_path)
    
    if not config_path.endswith('.toml'):
        config_path = os.path.join(config_path, '__import__.toml')

    with open(config_path, "rb") as file:
        main_config = toml.load(file)

    
    # Load all the toml files
    config_map = dict()
    work_path = os.path.dirname(config_path)
    
    for fs in os.walk(work_path):
        for file in fs[2]:
            # Ignore the unused toml files
            if 'import' not in main_config:
                break
            skip = True
            for imports in main_config['import']:
                if imports == file:
                    skip = False
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


def exit_handler(signum, frame):
    """
    Quit all the threads when Ctrl+C
    """
    logger.info("exit.<Ctrl+C>")
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


def main2(toml, options, port):
    
    logger.info("start@thread(%s)" % threading.get_ident())
    signal.signal(signal.SIGINT, exit_handler)

    from config import Config
    config = Config(toml)
    config.load()

    if "without-admin" not in options:
        from server import AdminServer
        server = AdminServer(config)
        server.set_logger(logger)
        server.start()
    else:
        for n, executor in executors.items():
            executor.execute()


if __name__ == '__main__':
    from help import usage
    work_path = ""
    if len(sys.argv) == 1:
        print(usage.__doc__)
        exit(0)

    from optparse import OptionParser    
    parser = OptionParser()

    parser.add_option("-t", "--toml", action="store", dest="toml", help="Provide the main toml file")
    parser.add_option("-o", "--options", action="store", dest="options", help="Provide admin server", default="")
    parser.add_option("-p", "--port", action="store", dest="port", help="Provide admin server port", default=3344)
    # parser.add_option("-p", "--port", action="store", dest="port", help="Provide admin server port")

    options, args = parser.parse_args()

    if not options.toml:
        print("Please provide the main toml file.")
        print(usage.__doc__)
        exit(0)

    #configs = load_configs(options.toml)
    #if len(configs) > 0:
    #    main(configs)

    main2(options.toml, options.options, options.port)

