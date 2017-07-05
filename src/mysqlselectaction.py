
from baseaction import *
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
            print("###", sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            return_var = '_r'
            if 'return' in action_config:
                return_var = action_config['return']
            context.set_context_value(return_var, result)
