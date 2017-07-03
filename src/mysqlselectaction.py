
from baseaction import *
from resource import *
import MySQLdb.cursors

@Action.register("mysql_select")
class MySQLSelectAction(BaseAction):

    def __init__(self):
        pass

    def execute(self, context):
        self.log("aaaaaa")
        result = None
        db = Resource.find_resource('global', 'mysqlconnection')
        with db.cursor() as cursor:
            action_config = self.get_action_config()
            cursor.execute(action_config['sql'])
            result = cursor.fetchall()
            context.set_return_value(result)
