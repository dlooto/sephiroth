
from flask_apscheduler import APScheduler

class Executor:
    """
    An engine drives a sequence of actions with a context
    """
    
    def __init__(self, config, pipeline_name, pipeline):
        self.config = config
        self.pipeline_name = pipeline_name
        self.pipeline = pipeline

        from logger import Logger
        # Each Executor has its own log file
        self.logger = Logger("%s.log" % pipeline_name).get_logger()

    def start(self):
        pass

    def execute(self, args):
        """
        """
        # print(self.pipeline_name)
        self.__on_execute(args)

    def __on_execute(self, args):
        """
        """
        self.logger.info(self.pipeline_name)
        