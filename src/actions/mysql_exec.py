
from .base_action import *
from resource import *

import MySQLdb
import MySQLdb.cursors
import MySQLdb.converters


@Actions.register("mysql_exec")
class MySQLExecAction(BaseAction):
    """
    :param sql || string
    :param mysqlconnection || string
    """

    def execute(self, context):
        result = None
        db = Resource.find_resource('global', 'mysqlconnection')
        
        with db.cursor() as cursor:
            action_config = self.get_action_config()
            sql = context.evaluate(action_config['sql'])
            # Logger
            self.log(sql)

            return_var = self.get_return_var_name()
            result = ()
            try:
                code = cursor.execute(sql)
                if code == 0:
                    if Resource.connect:
                        conn = Resource.connect()
                    
                        cursor = conn.cursor()
                        code = cursor.execute(sql)
                        result = cursor.fetchall()
                        cursor.close()
                        conn.close()
                        # Resource.reset_mysql_global_connection('mysqlconnection', conn)

                    print("Code", 0, "Refresh", code)
                    context.set_context_var(return_var, result)
                    return

                result = cursor.fetchall()

                print(sql)
                print(result)
            except:
                print("Exception")
            
            context.set_context_var(return_var, result)
