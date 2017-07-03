
from resource import *

class Action:

    action_classes = dict()

    @staticmethod
    def register(action_type):
        def action_class(action_clz):
            Action.action_classes[action_type] = action_clz
        return action_class

    @staticmethod
    def get_action_class(action_type):
        if action_type in Action.action_classes:
            return Action.action_classes[action_type]
        raise Exception("No action[%s] register" % action_type)


class BaseAction:
    """
    """
    def __init__(self):
        pass

    def set_global_resources(self, global_resources):
        self.global_resources = global_resources

    def lookup_resource(self, resource_name):
        pass

    def get_name(self, action_name):
        return self.action_name

    def set_info(self, engine_name, action_name, config):
        self.config = config
        self.engine_name = engine_name
        self.action_name = action_name
        self.action_config = self.config['action'][self.action_name]

    def get_action_config(self):
        """
        """
        return self.action_config

    def log(self, line):
        if 'logto' not in self.action_config:
            return # Log nothing if No logto field
        logto = self.action_config['logto']
        print("LogTo", logto)
        
        logger = Resource.find_resource(self.engine_name, logto)
        if logger:
            print("LOG IT")
            logger.write(line)
            print("LOG IT")
        else:
            print(self.engine_name, logto)
            print(Resource.resource_map)





    def execute(self, context):
        raise Exception('No derived class implemention?')


from http_actions import *
from mysqlselectaction import *
from formdata import *      