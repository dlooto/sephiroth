
from .base_action import *

@Actions.register("find_files")
class FindFilesAction(BaseAction):
    """
    """

    def execute(self, context):
        action_config = self.get_action_config()
        
        param0 = action_config['param0']
        param0 = context.evaluate(param0)
        print("@", param0)
        return_var = self.get_return_var_name()
        
        context.set_context_var(return_var, "/Users/healer/a.go")
