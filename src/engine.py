
from threading import Timer, Thread
import time
from context import *

class Engine:

    args = 1

    def __init__(self, config):
        print("?", str(Thread.name))
        self.config = config

    def __loop(self):
        try:
            self.run()
        except Exception as e:
            print("Ex", e)
        finally:
            interval = self.config['main']['interval']
            timer = Timer(int(interval), self.__loop)
            timer.start()

    def start(self):
        interval = self.config['main']['interval']
        timer = Timer(int(interval), self.__loop)
        timer.start()

    def run(self):
        interval = self.config['main']['interval']
        print(interval, type(interval), str(Thread.name))
        
        if 'action' not in self.config:
            return
        actions_config = self.config['action']
        if 'main' not in actions_config:
            print("Counld NOT find main action!")
        else:
            print(self.config['main']['name'] + "?")

        context = Context()
        actions = self.load_actions(actions_config)

        for action in actions:
            self.run_action(action, context)

    def load_actions(self, actions_config):
        """
        Action.main would be the first action
        """
        actions = []

        actions.append(None)
        return actions

    def run_action(self, action, context):
        print("Running")

        

        
        