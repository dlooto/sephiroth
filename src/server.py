

from flask import *
from flask_apscheduler import APScheduler
from executor import Executor


app = Flask(__name__, static_url_path='')

@app.route("/admin")
def admin():
    return "OK"

class AdminServer:
    """
    """
    def __init__(self, config):
        self.config = config
        self.scheduler = APScheduler()
        self.logger = None
        self.executors = dict()

    def set_logger(self, logger):
        self.logger = logger

    def get_logger(self):
        return self.logger

    def start(self):
        pipelines = self.config.get_pipelines()
        
        for (pipeline_name, pipeline) in pipelines.items():
            self.get_logger().info("pipelines: %s" % pipeline_name)
            executor = Executor(config, pipeline_name, pipeline)
            self.executors[pipeline_name] = executor
            args = ["Hello"]
            self.scheduler.add_job(
                func=getattr(executor, "execute"), 
                id=pipeline_name, args=args, trigger='cron', second='*/5')

        self.__server_run()
 
    def __server_run(self):
        self.scheduler.init_app(app)
        self.scheduler.start()
        app.run(debug=False)
