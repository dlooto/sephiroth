
from .base_action import *
import requests
import json


@Actions.register("http_get")
class HttpGetAction(BaseAction):
    """
    :param url || string || @required
    :param content_type || string || @optional
    """
    
    def execute(self, context):

        action_config = self.get_action_config()
        url = context.evaluate(action_config['url'])
        
        resp = requests.get(url)
        value = resp.text
        
        return_var = self.get_return_var_name()
                    
        if 'content_type' in action_config and action_config['content_type'] == 'json':
            value = json.loads(value)
        
        context.set_context_var(return_var, value)


@Actions.register("http_post")
class HttpPostAction(BaseAction):
    """
    """

    def execute(self, context):
        action_config = self.get_action_config()
        # TODO:
        param0 = self.get_param_var_name()

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
        
        param0 = self.get_param_var_name()

        filename = context.evaluate(context.get_context_var(param0))
        with open(filename, 'rb') as file:
            post_url = context.evaluate(action_config['url'])
            resp = requests.post(post_url, files={'file': file})
            print(resp.text)
            self.log(resp.text)
