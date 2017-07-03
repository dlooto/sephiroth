
from threading import Timer, Thread
import time
from context import *
from clock import *
from baseaction import *
from resource import *
import threading


# EngineState_Init -> EngineState_Start -> EngineState_Running -> EngineState_Waiting
# -> EngineState_Running
EngineState_Unknown     = 0
EngineState_Init        = 1
EngineState_Start       = 2
EngineState_Running     = 3
EngineState_Waiting     = 4


class Engine:
    """
    An engine drives a sequence of actions with a context
    """
    
    def __init__(self, config):
        self.config = config
        self.name = self.config['main']['name']
        self.__state = EngineState_Init

        Resource.initialize_local_resources(self.name, self.config)

    def get_state(self):
        return self.__state

    def run(self, context=None):
        """
        """
        try:
            self.__state = EngineState_Running
            print("ThreadId:", threading.get_ident())
            context = self.__run(context)
        except Exception as e:
            print("Exception:", e.with_traceback())
        finally:
            self.__state = EngineState_Waiting
            # Keep the context for the follower engines
            Clock.trigger_followers(Engine.run, self, context)

    def start(self):
        """
        """
        
        # TODO: Register Engine in clock.tick for very 30 s
        triggers = self.config['main']['triggers']
        if isinstance(triggers, str):
            triggers = [triggers]

        self.__state = EngineState_Start
        for trigger in triggers:
            Clock.register(self, trigger)



    def __run(self, context):
        """
        """
        if 'action' not in self.config:
            return
        actions_config = self.config['action']
        if 'main' not in actions_config:
            print("Counld NOT find main action!")
        else:
            print('Engine', self.config['main']['name'])

        if not context:
            print('Create new context')
            context = Context()
        actions = self.load_actions(actions_config)

        for action in actions:
            if not action:
                raise Exception("No action loaded")
            self.run_action(action, context)
        return context

    def create_action(self, action_name, action_config):
        """
        Create an action with its config
        """
        action_type = action_config['type']
        clz = Action.get_action_class(action_type)
        action = clz()
        action.set_info(self.name, action_name, self.config)
        return action

    def load_actions(self, actions_config):
        """
        Action.main would be the first action
        """
        actions = []

        action_config = actions_config['main']
        action_name = 'main'
        while action_config:
            action = self.create_action(action_name, action_config)
            actions.append(action)
            
            if 'next' not in action_config or action_config['next'] == '':
                break
            next_action = action_config['next']
            if next_action not in actions_config:
                raise Exception("No action provided")
            
            action_name = next_action
            action_config = actions_config[action_name]

        return actions

    def run_action(self, action, context):
        """
        """
        # TODO: Log
        print("-" * 40)
        action.execute(context)

        

        
        