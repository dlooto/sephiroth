
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
        action_config = self.get_action_config()
        sql = context.evaluate(action_config['sql'])
        self.log("sql:" + sql)
        if "()" in sql:
            return False
        try:
            db = Resource.find_resource('global', 'mysqlconnection')
            with db.cursor() as cursor:
 
                cursor.execute(sql)
                result = cursor.fetchall()
                print("Fetch:", result)
                
                return_var = self.get_return_var_name()
                context.set_context_var(return_var, result)
                return True
        except Exception as e:
            print(e)
            Resource.clear_global_resource('mysqlconnection')
            return False
