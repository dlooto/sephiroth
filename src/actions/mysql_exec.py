
from .base_action import *
from resource import *


@Actions.register("mysql_exec")
class MySQLExecAction(BaseAction):
    """
    :param sql || string
    :param mysqlconnection || string
    """

    def execute_impl(self, context, db):
        with db.cursor() as cursor:
            action_config = self.get_action_config()
            sql = context.evaluate(action_config['sql'])
            # Logger
            
            self.log(sql)
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
            except Error as e:
                return None
            
            print(result)
            return_var = self.get_return_var_name()
            context.set_context_var(return_var, result)

    def execute(self, context):
        result = None
        db = Resource.find_resource('global', 'mysqlconnection')
        result = self.execute_impl(context, db)
        if not result:
            Resource.reset_mysql_connection('global')
        # Retry
        db = Resource.find_resource('global', 'mysqlconnection')
        result = self.execute_impl(context, db)
