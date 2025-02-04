import threading
class EmptyListAccessException(Exception):
    pass


class Task:                             # Tasks with a set priority
    def __init__(self, task, priority):
        self.task = task
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority
    
    def __repr__(self):
         return f"Task(priority={self.priority}, task={self.task})

         

class PriorityQueue:
    def __init__(self, task=None):
        self.queue = []
        self.lock = threading.Lock()

        if task:
            self.queue.append(task)

    