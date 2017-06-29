
from baseaction import *
import requests
import json

@Action.register("http_get")
class HttpGetAction(BaseAction):
    """
    """
    def __init__(self):
        pass
    
    def execute(self, context):
        print(context)
        action_config = self.get_action_config()
        resp = requests.get(action_config['url'])
        context.set_return_value(resp.text)


@Action.register("http_post")
class HttpPostAction(BaseAction):
    """
    """
    def __init__(self):
        pass


    def execute(self, context):
        action_config = self.get_action_config()
        data = context.eval(action_config['data'])
        print("--" * 40)
        print(data)
        # data = self.convert_to_form(data)
        post_url = action_config['url']
        resp = requests.post(post_url, data=data)
        print(resp.text)
