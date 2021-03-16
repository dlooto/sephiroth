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

        if 'd/cmd/fetch/history' in url:
            device_id = url.split('/')[-1]
            url = 'http://platform.scarletsun.wang/api/v1/device/data/retransmission/%s/fetch_history/' % device_id

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
        self.send_data2newplatform(post_url, data)
        try:
            # shanghai-3 is new station, not connect to http://www.nucurie.com:1024
            value = 'No need send data to http://www.nucurie.com:1024/newbackdemo/index.html'
            return_var = self.get_return_var_name()
            context.set_context_var(return_var, value)
        except Exception as e:
            self.log(e)
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
        post_url = context.evaluate(action_config['url'])

        self.upload2newplatform(filename, post_url)
        try:
            # shanghai-3 is new station, not connect to http://www.nucurie.com:1024
            value = 'No need send file to http://www.nucurie.com:1024/newbackdemo/index.html'
            return_var = self.get_return_var_name()
            context.set_context_var(return_var, value)
        except Exception as e:
            print(e)

        return True
