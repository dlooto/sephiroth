
from .base_action import *
from resource import *


@Actions.register("mysql_exec")
class MySQLExecAction(BaseAction):
    """
    :param sql || string
    :param mysqlconnection || string
    """

    def execute(self, context):
        result = None
        db = Resource.find_resource('global', 'mysqlconnection')
        
        try:
            with db.cursor() as cursor:
                action_config = self.get_action_config()
                sql = context.evaluate(action_config['sql'])
                # Logger
                
                self.log(sql)
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                
                return_var = self.get_return_var_name()
                context.set_context_var(return_var, result)
        except Exception as e:
            print(e.with_traceback())
