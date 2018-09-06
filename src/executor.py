
from flask_apscheduler import APScheduler
from actions import *
from context import *

class Executor:
    """
    An Executor drives a pipeline which composed by a sequence of actions with a context
    """
    
    def __init__(self, config, pipeline_name, pipeline):
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
        action = BaseAction.create_action("http.get", self.pipeline[0])
        action.try_execute(self.get_context())
        print(self.__context.vars)