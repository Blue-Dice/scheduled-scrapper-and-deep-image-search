import argparse
from CeleryScheduler.CeleryWorker import CeleryAgent

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--help", action="store_true")
parser.add_argument("--start", action="store_true")
parser.add_argument("--purge", action="store_true")

celery_help_message = """
Celery run commands:
--start : Start celery worker
--purge : Purge all celery queues
"""

if __name__ == "__main__":
    args = parser.parse_args()
    if args.help: print(celery_help_message)
    else:
        agent = CeleryAgent()
        agent.celery_start()
        agent.route_tasks([
            ["task_name","queue_name"]
        ])
        # discover remote celery tasks
        # agent.discover_tasks([
        #     "folder_name"
        # ])
        agent.schedule_tasks()
        if args.start: agent.celery_start()
        elif args.purge: agent.celery_purge()