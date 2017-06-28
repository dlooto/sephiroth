
from baseaction import *
import requests

@Action.register("http_get")
class HttpGetAction(BaseAction):

    def __init__(self):
        pass
    
    def execute(self, context):
        print(context)
        action_config = self.get_action_config()
        resp = requests.get(action_config['url'])
        context.set_return_value(resp.text)