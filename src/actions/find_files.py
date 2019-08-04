
from .base_action import *
import os


@Actions.register("find_files")
class FindFilesAction(BaseAction):
    """
    :param 
    """

    def set_filename(self, context, filename):
        return_var = self.get_return_var_name()
        context.set_context_var(return_var, filename) 

    def execute(self, context):
        param0 = self.get_param_var_name()
        param0 = context.evaluate(param0)
        for fs in os.walk(param0):
            for file in fs[2]:
                if not file.startswith('!'):
                    self.set_filename(context, os.path.join(fs[0], file))
        return True
