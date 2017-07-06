
from .base_action import *
import requests
import json

@Actions.register("http_get")
class HttpGetAction(BaseAction):
    """
    """
    
    def execute(self, context):
        # print(context)
        action_config = self.get_action_config()
        url = context.evaluate(action_config['url'])
        
        resp = requests.get(url)
        self.log(resp.text)
        return_var = '_r'
        json_decode = False
        if 'return' in action_config:
            return_var = action_config['return']
        elif 'return_json' in action_config:
            return_var = action_config['return_json']
            json_decode = True
        
        context.set_context_var(return_var, resp.text)
        if json_decode:
            context.set_context_var(return_var, json.loads(resp.text))



@Actions.register("http_post")
class HttpPostAction(BaseAction):
    """
    """

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


@Actions.register("http_post_file")
class HttpPostFileAction(BaseAction):
    """
    """

    def execute(self, context):
        action_config = self.get_action_config()
        # TODO:
        param0 = '_r'
        if 'param0' in action_config:
            param0 = action_config['param0']

        filename = context.evaluate(context.get_context_var(param0))
        with open(filename, 'rb') as file:
        
            post_url = context.evaluate(action_config['url'])
            resp = requests.post(post_url, files={'file': file})
            print(resp.text)
            self.log(resp.text)
