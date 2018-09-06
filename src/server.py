

from flask import *
from flask_apscheduler import APScheduler
from executor import Executor


app = Flask(__name__, static_url_path='')

@app.route("/healthCheck")
def health_check():
    return "OK"


@app.route("/admin")
def admin():
    return "OK"

class AdminServer:
    """
    """
    def __init__(self, config):
        self.config = config
        self.scheduler = APScheduler()
        self.__logger = None
        self.executors = dict()

    def set_logger(self, logger):
        self.__logger = logger

    def get_logger(self):
        return self.__logger

    def start(self):
        pipelines = self.config.get_pipelines()
        
        for (pipeline_name, pipeline) in pipelines.items():
            self.get_logger().info("pipelines: %s" % pipeline_name)
            executor = Executor(config, pipeline_name, pipeline)
            self.executors[pipeline_name] = executor
            self.__add_job(pipeline_name, pipeline, executor)
                
        self.__server_run()
    
    def __add_job(self, pipeline_name, pipeline, executor: Executor):
        args = [pipeline_name]
        f_execute = getattr(executor, "execute")
        params = dict()
        params['func'] = f_execute
        params['id'] = pipeline_name
        params['args'] = args

        start_pipeline = pipeline[0]
        params['trigger'] = start_pipeline['trigger']
        if 'second' in start_pipeline:
            params['second'] = start_pipeline['second']
        elif 'minute' in start_pipeline:
            params['minute'] = start_pipeline['minute']
        self.scheduler.add_job(**params)
            
 
    def __server_run(self):
        self.scheduler.init_app(app)
        self.scheduler.start()
        app.run(debug=False)
