
from threading import Timer, Thread
import time
from context import *
from clock import *
from baseaction import *

class Engine:
    """

    """
    args = 1

    def __init__(self, config):
        self.config = config

    @property
    def name(self):
        return self.config['main']['name']

    def run(self):
        try:
            self.__run()
        except Exception as e:
            print("Exception:\n", e)
        finally:
            Clock.trigger_followers(self)

    def start(self):
        """
        """
        
        # TODO: Register Engine in clock.tick for very 30 s
        triggers = self.config['main']['triggers']
        if isinstance(triggers, str):
            triggers = [triggers]
        for trigger in triggers:
            Clock.register(self, trigger)   


    def __run(self):
        """
        """
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
            if not action:
                raise Exception("No action loaded")
            self.run_action(action, context)

    def create_action(self, action_config):
        action_type = action_config['type']
        clz = Action.get_action_class(action_type)
        return clz()

    def load_actions(self, actions_config):
        """
        Action.main would be the first action
        """
        actions = []

        action_config = actions_config['main']
        while action_config:
            action = self.create_action(action_config)
            actions.append(action)

            next_action = action_config['next']
            if next_action not in actions_config:
                break
            
            action_config = actions_config[next_action]

        return actions

    def run_action(self, action, context):
        """
        """
        # TODO: Log
        print("Running")
        action.execute(context)

        

        
        