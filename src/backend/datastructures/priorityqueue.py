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


    def dequeue(self):                           # Dequeuing the element with the most priority.
        with self.lock:
            if not self.queue:
                raise EmptyListAccessException("The queue is empty")
            self.queue.pop(0)
    

    def peek(self):                  # Returns the element with the most priority without dequeuing the element if the queue isn't empty.
        with self.lock:
            if self.queue:
              return self.queue[0] 
            
            else:
              return None
            

    def print_queue(self):          # Prints the queue with the priorities too.
        with self.lock:
            for task in self.queue:
                print(f"Priority: {task.priority}, Task: {task.task}")

            
    def is_empty(self):             # Checks if the queue is empty.
        with self.lock:
            if len(self.queue):
                return True
            
            else:
                return False
            
    
    def size(self):                    # Checks the size of the queue.
        with self.lock:
            return len(self.queue)


    def clear(self):                    #clears the queue.
        with self.lock:
            self.queue.clear()


    def contains(self, task):           # Checks if the task is in the queue.
        with self.lock:
            if task in self.queue:
                return True
            
            else:
                return False
        


    def get_priority(self, task_content):               # Gets the priority of a given task.
        with self.lock:
            for task in self.queue:
                if task.task == task_content:
                    return task.priority
            return -1
        

    def get_task(self, priority):               # Gets the first task the matches the priority.
        with self.lock:
            for task in self.queue:
                if task.priority == priority:
                    return task
            return None
        
    
pq = PriorityQueue()
pq.enqueue(Task("Do laundry", 3))
pq.enqueue(Task("Finish report", 1))
pq.enqueue(Task("Buy groceries", 2))

print("\nQueue after enqueuing:")
pq.print_queue()

print("\nDequeuing highest priority task")
pq.dequeue()
pq.print_queue()

print("\nPeeking at the highest priority task:")
print(pq.peek())

pq.print_queue()  