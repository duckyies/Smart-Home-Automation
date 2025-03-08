import logging
from functools import total_ordering

@total_ordering
class LogTask:

    LEVEL_LIST = [
        logging.OFF,
        logging.SEVERE,
        logging.WARNING,
        logging.INFO,
        logging.CONFIG,
        logging.FINE,
        logging.FINER,
        logging.FINEST,
        logging.ALL
    ]

    def __init__(self, log_level, message):
       
        self.logLevel = log_level
        self.message = message

    def getLogLevel(self):

        return self.logLevel

    def getMessage(self):

        return self.message

    def setLogLevel(self, logLevel):

        self.logLevel = logLevel

    def setMessage(self, message):

        self.message = message

    def __eq__(self, other):
        
        if not isinstance(other, LogTask):
            return NotImplemented

        return self.logLevel == other.logLevel

    def __lt__(self, other):
       
        if not isinstance(other, LogTask):
            return NotImplemented
        try:

            taskLevel = LogTask.LEVEL_LIST.index(other.getLogLevel())
            currTaskLevel = LogTask.LEVEL_LIST.index(self.getLogLevel())

            if taskLevel > currTaskLevel:
                return True
            elif taskLevel < currTaskLevel:
                return False
            else:
                return False
            
        except ValueError:

            print(f"Warning: Log level not recognized: {self.logLevel} or {other.logLevel}")
            return False