
from .base_action import *
import json

@Actions.register("json.check")
class JsonCheckAction(BaseAction):
    """
    :param url || string || @required
    :param content_type || string || @optional
    """
    
    def execute(self, context):
        
        d = json.loads(context.get_last_return_value())
        action_config = self.get_action_config()
        if 'assert_path' not in action_config:
            print("Must have a assert-path")
            exit(0)
        
        assert_path = action_config['assert_path']
        v = self.get_value(d, assert_path)

        if not v or not self.match_type(v, action_config['assert_type']):
            print("Type not matched")


    def get_value(self, data, path):
        v = data
        ps = path.split(".")
        for p in ps:
            v = v[p]
        return v

    def match_type(self, value, value_type):
        if value_type in ['array', 'list']:
            return type(value) is list
        return False
