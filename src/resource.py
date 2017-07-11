
import MySQLdb
import MySQLdb.cursors
import MySQLdb.converters


class Resource:
    #
    resource_map = dict()

    #
    global_variables = dict()

    @staticmethod
    def initialize_global_resources(config):
        for sec in config:
            if sec == 'mysqlconnection':
                Resource.initialize_mysql_connection('global', config[sec])
            if sec == 'redisclient':
                Resource.initialize_redis_client('global', config[sec])                
            if sec == 'logger':
                Resource.initialize_logger('global', config[sec])
            if sec == 'vars':
                Resource.initialize_global_variables('global', config[sec])
            else:
                pass

        print("Global resource initialized")

    @staticmethod
    def initialize_local_resources(name, config):
        for sec in config:
            if sec == 'mysqlconnection':
                Resource.initialize_mysql_connection(name, config[sec])
            if sec == 'logger':
                Resource.initialize_logger(name, config[sec])
            else:
                pass

        print("Local resource initialized for %s" % name)   
    
    @staticmethod
    def get_resource_name(config):
        resource_name = list(config.keys())[0]
        return resource_name

    @staticmethod
    def initialize_mysql_connection(scope, config):
        resource_name = Resource.get_resource_name(config)
        config = config[resource_name]

        conv = MySQLdb.converters.conversions.copy()
        conv[12] = str
        db = MySQLdb.connect(**config, cursorclass=MySQLdb.cursors.DictCursor, conv=conv)

        resource_full_name = "%s.%s" % (scope, resource_name)
        Resource.resource_map[resource_full_name] = db

    @staticmethod
    def initialize_logger(scope, config):
        import log

        resource_name = Resource.get_resource_name(config)
        config = config[resource_name]
        logger = log.Logger(config)
        # logger.init()

        resource_full_name = "%s.%s" % (scope, resource_name)
        Resource.resource_map[resource_full_name] = logger

    @staticmethod
    def initialize_global_variables(scope, config):
        for var, value in config.items():
            Resource.global_variables['$' + var] = value
        
    @staticmethod
    def get_global_var(var):
        if var in Resource.global_variables:
            return Resource.global_variables[var]
        return None

    @staticmethod
    def find_resource(scope, resource_name):
        if scope == 'global':
            return Resource.find_global_resource(resource_name)
        else:
            return Resource.find_local_resource(scope, resource_name)

    @staticmethod
    def find_global_resource(resource_name):
        resource_full_name = "global.%s" % resource_name
        return Resource.resource_map[resource_full_name]

    @staticmethod
    def find_local_resource(scope, resource_name):
        resource_full_name = "%s.%s" % (scope, resource_name)
        return Resource.resource_map[resource_full_name]        