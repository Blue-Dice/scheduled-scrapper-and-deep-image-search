from celery import Celery
from Helpers import Logger as Log
from decouple import config
import argparse

class CeleryWorker():
    def __init__(self) -> None:
        self.broker_uri = config('MESSAGE_BROKER_URI')
        self.app = Celery(
            'Scraper',
            broker = self.broker_uri,
            backend = self.broker_uri,
        )
        
    def celery_purge(self) -> None:
        self.app.start(['purge', '-Q', self.queues, '-f'])
    
    def celery_start(self) -> None:
        self.app.worker_main(['worker', '--pool=threads', '-Q', self.queues, '--loglevel=DEBUG'])
        
    def routes_tasks(self, routes) -> None:
        try:
            self.task_routes = {}
            for route in routes:
                self.task_routes[route[0]] = {'queue':route[1]}
            self.app.conf.update({'task_routes':self.task_routes})
            self.queues = ','.join([route[1] for route in routes])
            Log.success('Celery tasks routes successfully registerd')
        except Exception as e:
            Log.error(f'Celery task route error -> {e}')
            
    def discover_tasks(self, module_locations) -> None:
        try:
            self.task_modules = []
            for location in module_locations:
                self.task_modules.append(location)
            self.app.autodiscover_tasks(self.task_modules,force=True)
            Log.success('Celery tasks discovery completed')
        except Exception as e:
            Log.error(f'Celery task discover error -> {e}')

parser = argparse.ArgumentParser()
parser.add_argument('--start', action='store_true')
parser.add_argument('--purge', action='store_true')

if __name__ == '__main__':
    agent = CeleryWorker()
    agent.routes_tasks([
        ['task_name','queue_name']
    ])
    agent.discover_tasks([
        'folder_name'
    ])
    args = parser.parse_args()
    if args.purge and not args.start: agent.celery_purge()
    if args.start and not args.purge: agent.celery_start()