import threading
class EmptyListAccessException(Exception):
    pass
class Task:                             # Tasks with a set priority
    def __init__(self, task, priority):
        self.task = task
        self.priority = priority

