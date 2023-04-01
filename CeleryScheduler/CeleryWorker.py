from celery import Celery
from celery.schedules import crontab
from Helpers import Logger as Log
from decouple import config

class CeleryAgent():
    
    def __init__(self) -> None:
        self.broker_uri = config("MESSAGE_BROKER_URI", default="redis://127.0.0.1:6379/", cast=str)
        self.app = Celery(
            "Scraper",
            broker = self.broker_uri,
            backend = self.broker_uri,
        )
        
    def celery_purge(self) -> None:
        self.app.start(["purge", "-Q", self.queues, "-f"])
    
    def celery_start(self) -> None:
        self.app.worker_main(["worker", "-B", "--pool=threads", "-Q", self.queues, "--loglevel=INFO"])
        
    def route_tasks(self, routes) -> None:
        try:
            self.task_routes = {}
            for route in routes:
                self.task_routes[route[0]] = {"queue":route[1]}
            self.app.conf.update({"task_routes":self.task_routes})
            self.queues = ",".join([route[1] for route in routes])
            Log.success("Celery tasks routes registerd successfully")
        except Exception as e:
            Log.error(f"Celery task route error -> {e}")
            
    def discover_tasks(self, module_locations) -> None:
        try:
            self.task_modules = []
            for location in module_locations:
                self.task_modules.append(location)
            self.app.autodiscover_tasks(self.task_modules, force=True)
            Log.success("Celery tasks discovery completed")
        except Exception as e:
            Log.error(f"Celery task discover error -> {e}")
    
    def schedule_tasks(self) -> None:
        try:
            self.app.conf.beat_schedule = {
                "Daily_task": {
                    "task": "Task_Scheduler",
                    "schedule": crontab(minute=19, hour=14),
                    "args": (["weekly"]),
                },
                "Weekly_task": {
                    "task": "Task_Scheduler",
                    "schedule": crontab(minute=0, hour=0, day_of_week="sun"),
                    "args": (["weekly"]),
                },
                "Monthly_task": {
                    "task": "Task_Scheduler",
                    "schedule": crontab(minute=0, hour=0, day_of_month="1"),
                    "args": (["monthly"]),
                }
            }
            Log.success("Celery scheduled tasks registerd successfully")
        except Exception as e:
            Log.error(f"Celery task schedule error -> {e}")