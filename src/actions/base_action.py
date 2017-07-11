
from resource import *


class Actions:
    """
    Hold the registered class object
    """
    action_classes = dict()

    #
    @staticmethod
    def register(action_type):
        """
        Create a derived-action-class instance should use get_action_class()
        """
        def action_class(action_clz):
            Actions.action_classes[action_type] = action_clz
        return action_class

    #
    @staticmethod
    def get_action_class(action_type):
        if action_type in Actions.action_classes:
            return Actions.action_classes[action_type]
        raise Exception("No action[%s] register" % action_type)


class BaseAction:
    """
    """
    def __init__(self):
        self.context = None
        self.config = None
        self.engine_name = ""
        self.action_name = ""
        self.action_config = None

    def print_doc(self):
        print(self.__doc__)

    def __precheck(self, lines):
        # TODO: 
        for line in lines:
            if line.startswith(':param'):
                param = line[7:]
                ps = param.split('||')

    def precheck(self):
        doc = self.__doc__
        if not doc:
            return False
        lines = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), doc.split('\n'))))
        return self.__precheck(lines)

    #def set_global_resources(self, global_resources):
    #    self.global_resources = global_resources

    #
    def get_param_var_name(self, index=0):
        p = 'param%d' % index
        if p in self.action_config:
            return self.action_config[p]
        return None

    #
    def get_return_var_name(self):
        return_var_name = '_r'
        if 'return' in self.action_config:
            return_var_name = self.action_config['return']
        return return_var_name

    #
    def get_name(self, action_name):
        return self.action_name

    #
    def set_info(self, engine_name, action_name, config):
        """
        This function should be invoked in advanced.
        """
        self.config = config
        self.engine_name = engine_name
        self.action_name = action_name
        self.action_config = self.config['action'][self.action_name]

    def get_action_config(self):
        """
        """
        return self.action_config

    def log(self, line):
        if 'logto' not in self.action_config:
            return  # Log nothing if No logto field
        logto = self.action_config['logto']

        logto = self.context.evaluate(logto)

        logger = Resource.find_resource(self.engine_name, logto)
        if logger:
            logger.write(line)
        else:
            print(self.engine_name, logto)

    def try_execute(self, context):
        self.context = context
        self.execute(context)

        action_config = self.get_action_config()
        if 'exit_at' in action_config:
            exit_at = action_config['exit_at']
            expr = context.evaluate(exit_at)
            # If the express returns True, 
            # throw Exception to finish the whole execution of the pipeline.
            if eval(expr):
                raise Exception("exit at %s" % exit_at)

        self.context = None
