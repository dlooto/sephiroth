
from .base_action import *
from resource import *
import MySQLdb.cursors

@Actions.register("mysql_select")
class MySQLSelectAction(BaseAction):

    def __init__(self):
        pass

    def execute(self, context):
        result = None
        db = Resource.find_resource('global', 'mysqlconnection')
        with db.cursor() as cursor:
            action_config = self.get_action_config()
            sql = context.evaluate(action_config['sql'])
            # Logger
            self.log(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            
            return_var = self.get_return_var_name()
            context.set_context_var(return_var, result)