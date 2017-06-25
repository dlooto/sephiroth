
from .baseaction import *

@Action.register("mysql_select")
class MySQLSelectAction(BaseAction):

    def __init__(self):
        pass

    def execute(self, context):
        print("SELECT")        