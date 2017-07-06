
from .base_action import *

@Actions.register("find_files")
class FindFilesAction(BaseAction):
    """
    """

    def execute(self, context):
        action_config = self.get_action_config()
        
        return_var = self.get_return_var_name()
        
        context.set_context_var(return_var, "/Users/healer/a.go")