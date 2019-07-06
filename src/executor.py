
from flask_apscheduler import APScheduler
from actions import *
from context import *
from config import Config

class Executor:
    """
    An Executor drives a pipeline which composed by a sequence of actions with a context
    """
    
    def __init__(self, config: Config, pipeline_name, pipeline):
        self.config = config
        self.pipeline_name = pipeline_name
        self.pipeline = pipeline
        self.__context = Context()
        from logger import Logger
        # Each Executor has its own log file
        self.logger = Logger("%s.log" % pipeline_name).get_logger()

    def start(self):
        pass

    def get_context(self):
        return self.__context

    def execute(self, args):
        """
        """
        self.__on_execute(args)

    def __on_execute(self, args):
        """
        """
        # self.logger.info(self.pipeline_name, self.pipeline)
        action_name = Config.get_start_action_name(self.pipeline)

    
        while action_name:
            
            action_config = Config.get_action_config(self.pipeline, action_name)
            if not action_config:
                break
            if 'type' not in action_config:
                print("No action type for ", action_name)
                exit(0)
            action_type = action_config['type']
            action_type = action_config['type']
            action = BaseAction.create_action(action_type, action_config)
            print(action_name, action)
            action.try_execute(self.get_context())

            action_name = action.get_next()


            
        