
from baseaction import *
import requests
import json

@Actions.register("http_get")
class HttpGetAction(BaseAction):
    """
    """
    def __init__(self):
        pass
    
    def execute(self, context):
        # print(context)
        action_config = self.get_action_config()
        resp = requests.get(action_config['url'])
        self.log(resp.text)
        context.set_return_value(resp.text)


@Actions.register("http_post")
class HttpPostAction(BaseAction):
    """
    """
    def __init__(self):
        pass


    def execute(self, context):
        action_config = self.get_action_config()
        # TODO:
        param0 = '_r'
        if 'param0' in action_config:
            param0 = action_config['param0']

        data = context.get_context_var(param0)
        
        post_url = action_config['url']
        resp = requests.post(post_url, data=data)
        self.log(resp.text)
