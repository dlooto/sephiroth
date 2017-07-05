
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
        url = context.evaluate(action_config['url'])
        
        resp = requests.get(url)
        self.log(resp.text)
        return_var = '_r'
        if 'return' in action_config:
            return_var = action_config['return']
        context.set_context_var(return_var, resp.text)


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
        
        post_url = context.evaluate(action_config['url'])
        resp = requests.post(post_url, data=data)
        self.log(resp.text)
