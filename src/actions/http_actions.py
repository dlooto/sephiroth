from .base_action import *
import requests
import json

from urllib.parse import urlparse


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
        #self.log(value)
        print(value)
        return_var = self.get_return_var_name()
        print(return_var)
        if 'content_type' in action_config and action_config['content_type'] == 'json':
            value = json.loads(value)

        context.set_context_var(return_var, value)
        return True


@Actions.register("http_post")
class HttpPostAction(BaseAction):
    """
    """
    def send_data2newplatform(self, post_url, data):
        if '/d/send' not in post_url:
            return False

        device_id = post_url.split('/')[-1]
        api = 'http://platform.scarletsun.wang/api/v1/receive/device/data/%s/' % device_id
        try:
            resp = requests.post(api, data)
            self.log(resp.json())
        except:
            pass
        return True

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
        self.send_data2newplatform(post_url, data)
        return True


@Actions.register("http_post_file")
class HttpPostFileAction(BaseAction):
    """
    """

    def upload2newplatform(self, filename, post_url):
        parse_url = urlparse(post_url)
        query_params = parse_url.query
        api = 'http://platform.scarletsun.wang/api/v1/device/hpge/upload/?%s' % query_params
        with open(filename, 'rb') as file:
            try:
                resp = requests.post(api, files={'file': file})
                self.log(resp.status_code)
            except:
                pass

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

        self.upload2newplatform(filename, post_url)
        return True
