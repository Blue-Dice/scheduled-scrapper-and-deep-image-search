import sys
import logging
import coloredlogs

INFO = logging.INFO
DEBUG = logging.DEBUG
ERROR = logging.ERROR
REPORT = INFO + 5
SUCCESS = REPORT + 1

logging.addLevelName(REPORT, "REPORT")
logging.addLevelName(SUCCESS, "SUCCESS")

class CustomLogger(logging.Logger):
    def __init__(self, name, console_level=INFO):
        super().__init__(name, console_level)
        self.streamHandler = logging.StreamHandler(sys.stdout)
        self.streamHandler.setFormatter(self._build_formatter())
        super().addHandler(self.streamHandler)

    def _build_formatter(self):
        return coloredlogs.ColoredFormatter('%(asctime)s | %(message)s', '%H:%M:%S', '%',
            {
                'debug': {'color': 'yellow', 'faint': True},
                'error': {'color': 'red', 'bold': True},
                'report': {'color': 'white', 'bold': True},
                'success': {'color': 'green', 'bold': True}
            }
        )

    def log(self, msg, level=INFO):
        super().log(level, msg)
logger = CustomLogger("ISR - Scheduler & Deep Image Search")

def error(msg):
    return logger.log(msg, level=ERROR)

def debug(msg):
    return logger.log(msg, level=DEBUG)

def report(msg):
    return logger.log(msg, level=REPORT)

def success(msg):
    return logger.log(msg, level=SUCCESS)