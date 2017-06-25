
from .baseaction import *

@Action.register("http_send")
class HttpSendDataAction(BaseAction):

    def __init__(self):
        pass
    
    def execute(self, context):
        print("SEND")