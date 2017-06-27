
import MySQLdb

class Resource:

    global_respurce_map = dict()

    @staticmethod
    def initialize_global_resources(config):
        for sec in config:
            if sec == 'mysqlconnection':
                Resource.initialize_mysql_connection('G', config[sec])
            else:
                pass

        print("Global resource initialized")
    
    @staticmethod
    def initialize_mysql_connection(scope, config):
        resource_name = list(config.keys())[0]
        config = config[resource_name]
        db = MySQLdb.connect(**config)

        Resource.global_respurce_map[resource_name] = db


    @staticmethod
    def find_resource(resource_name):
        return Resource.global_respurce_map[resource_name]