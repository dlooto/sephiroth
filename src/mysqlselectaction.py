
from baseaction import *
from resource import *

@Action.register("mysql_select")
class MySQLSelectAction(BaseAction):

    def __init__(self):
        pass

    def execute(self, context):
        db = Resource.find_resource('mysqlconnection')
        with db.cursor() as cursor:
            cursor.execute('show tables')
            print(cursor.fetchall())