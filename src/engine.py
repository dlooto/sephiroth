
import threading
import traceback

from resource import Resource
from clock import Clock
from context import *
from actions import *


# EngineState_Init -> EngineState_Start -> EngineState_Running -> EngineState_Waiting
# -> EngineState_Running
EngineState_Unknown = 0
EngineState_Init = 1
EngineState_Start = 2
EngineState_Running = 3
EngineState_Waiting = 4


class Engine:
    """
    An engine drives a sequence of actions with a context
    """
    
    def __init__(self, config):
        self.config = config
        self.exec_times = 0
        self.trigger_time = 0
        self.name = self.config['main']['name']
        self.__state = EngineState_Init
        self.engine_instance_vars = dict()

        Resource.initialize_local_resources(self.name, self.config)
    
    def __str__(self):
        return "%s@%d" % (self.name, self.__state)

    def get_state(self):
        return self.__state

    def run(self, context=None):
        """
        """
        try:
            self.__state = EngineState_Running
            print("ThreadId:", threading.get_ident())
            context = self.__run(context)
            print(context)
            # trigger the followers
            Clock.trigger_followers(Engine.run, self, context)
        except Exception as e:
            print_exception = Resource.get_global_var('$print_exception')
            if print_exception == 1:
                print(traceback.format_exc())
            else:
                print("Exception:", e)
        finally:
            self.__state = EngineState_Waiting
            # Keep the context for the follower engines

    def set_trigger_time(self, trigger_time):
        self.trigger_time = trigger_time

    # !
    def initialize_vars(self, vars):
        """
        """
        for key, value in vars.items():
            self.engine_instance_vars[key] = value

    def start(self):
        """
        """
        if 'vars' in self.config:
            self.initialize_vars(self.config['vars'])

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
            print("Could NOT find main action!")
        else:
            print('Engine', self.config['main']['name'])

        if not context:
            context = Context()

        context.set_engine(self)
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
        clz = Actions.get_action_class(action_type)
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
                raise Exception("No action provided " + next_action)
            
            action_name = next_action
            action_config = actions_config[action_name]

        return actions

    def run_action(self, action, context):
        """
        """
        if action.precheck():
            pass
        action.try_execute(context)
        self.exec_times += 1

    def get_value(self, key, default_value=None):
        """
        Get engine instance variable value
        """
        if key == 'trigger_time':
            return self.trigger_time

        if key in self.engine_instance_vars:
            return self.engine_instance_vars[key]
        else:
            return default_value

    def set_value(self, key, value):
        self.engine_instance_vars[key] = value

