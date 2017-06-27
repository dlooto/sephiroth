


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
    def __init__(self):
        pass

    def set_global_resources(self, global_resources):
        self.global_resources = global_resources

    def lookup_resource(self, resource_name):
        pass

    def execute(self, context):
        print("A")

from httpsenddataaction import *
from mysqlselectaction import *        