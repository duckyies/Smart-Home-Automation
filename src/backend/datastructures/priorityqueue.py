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
         return f"Task(priority={self.priority}, task={self.task})"



class PriorityQueue:
    def __init__(self, task=None):
        self.queue = []
        self.lock = threading.Lock()

        if task:
            self.queue.append(task)

            
    def enqueue(self, new_task):
        with self.lock:
            if not self.queue:
                self.queue.append(new_task)
                return
            
                                                        
            for i, task in enumerate(self.queue):           # Inserting the task in sorted order
                if task.priority > new_task.priority:
                    self.queue.insert(i, new_task)
                    return

           
            self.queue.append(new_task)          # If the task was not inserted earlier, we add it at the end


    def dequeue(self):
        with self.lock:
            if not self.queue:
                raise EmptyListAccessException("The queue is empty")
            self.queue.pop(0)
    

    def peek(self):
        with self.lock:
            return self.queue[0] if self.queue else None