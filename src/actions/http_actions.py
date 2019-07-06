
from .base_action import *
import requests
import json


@Actions.register("http.get")
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


@Actions.register("http.postForm")
class HttpPostFormAction(BaseAction):
    """
    """

    def execute(self, context):
        action_config = self.get_action_config()
        # TODO:
        param0 = self.get_param_var_name()

        data = context.get_context_var(param0)
        
        post_url = context.evaluate(action_config['url'])
        resp = requests.post(post_url, data=data)
        value = resp.text
        print(value)
        if 'content_type' in action_config and action_config['content_type'] == 'json':
            value = json.loads(value)
        
        return_var = self.get_return_var_name()
        context.set_context_var(return_var, value)
        resp.connection.close()
        
        self.log(resp.text)

@Actions.register("http.postJson")
class HttpPostJsonAction(BaseAction):
    pass

@Actions.register("http.postFile")
class HttpPostFileAction(BaseAction):
    """
    """

    def execute(self, context):
        action_config = self.get_action_config()
        
        param0 = self.get_param_var_name()

        filename = context.evaluate(param0)
        print(filename)
        with open(filename, 'rb') as file:
            post_url = context.evaluate(action_config['url'])
            resp = requests.post(post_url, files={'file': file})
            value = resp.text
            print(value)
            if 'content_type' in action_config and action_config['content_type'] == 'json':
                value = json.loads(value)
            print(resp.text)
            return_var = self.get_return_var_name()
            context.set_context_var(return_var, value)
