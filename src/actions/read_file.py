

from .base_action import *


@Actions.register("read_file")
class ReadFileAction(BaseAction):
    """
    """

    def execute(self, context):
        action_config = self.get_action_config()
        
        param0 = self.get_param_var_name()
        param0_value = context.evaluate(param0)
        
        with open(param0_value, 'r') as file:
            content = file.readlines()

            content = list(map(lambda x: x.strip(), content))
            
            return_var = self.get_return_var_name()

            context.set_context_var(return_var, content)
        return True