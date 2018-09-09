
from .base_action import *
import json

@Actions.register("json.check")
class JsonCheckAction(BaseAction):
    """
    :param url || string || @required
    :param content_type || string || @optional
    """
    
    def execute(self, context):
        print('-' * 20)
        print(context)