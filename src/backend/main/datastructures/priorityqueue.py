import threading
from ..datastructures.linkedlist import LinkedList, Node
from ..misc import EmptyListAccessException


class Task:
    def __init__(self, task, priority):
        self.task = task
        self.priority = priority

    def getTask(self):
        return self.task

    def getPriority(self):
        return self.priority

    def setPriority(self, priority):
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return f"Task(priority={self.priority}, task={self.task})"

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.task == other.task and self.priority == other.priority
        return False


class PriorityQueue:
    def __init__(self, task=None):
        self.queue = LinkedList()  #Use Linked List instead of Python List
        self.lock = threading.Lock()

        if task:
            self.enqueue(task)  # Use enqueue to correctly insert into linked list.

    def enqueue(self, newTask):
         with self.lock:
            if self.queue.is_empty():
                self.queue.add_end(newTask) #Add to the end of linked list
                return

            current = self.queue.head #set the current
            prev = None #Set prev to none

            while current: #Traversing the array
                if newTask.getPriority() < current.val.getPriority():
                    #Add task to front if priority is higher.
                    if prev is None:
                        self.queue.add_front(newTask)
                    else:
                         new_node = Node(newTask)
                         new_node.next = current
                         prev.next = new_node
                         self.queue.size += 1

                    return
                prev = current
                current = current.next

            self.queue.add_end(newTask) #Add the task to the end if it is not added before
            

    def dequeue(self):  # Dequeuing the element with the most priority.
        with self.lock:
            if self.queue.is_empty():
                return None 
            return self.queue.remove_front() #Removes the front of the linked list

    def peek(self):  # Returns the element with the most priority
        with self.lock:
             if self.queue.is_empty():
                return None
             return self.queue.peek()

    def print(self):  # Prints the queue with the priorities too.
        with self.lock:
            current = self.queue.head
            while current:
                print(f"Priority: {current.val.getPriority()}, Task: {current.val.getTask()}")
                current = current.next

    def isEmpty(self):  # Checks if the queue is empty.
        with self.lock:
            return self.queue.is_empty()  # Check if linked list is empty

    def size(self):  # Checks the size of the queue.
        with self.lock:
            return self.queue.get_size()

    def clear(self):  # clears the queue.
        with self.lock:
            self.queue.clear()

    def contains(self, task):  # Checks if the task is in the queue.
        with self.lock:
            current = self.queue.head
            while current:
                if current.val == task:
                    return True
                current = current.next
            return False

    def getPriority(self, task_content):  # Gets the priority of a given task.
        with self.lock:
            current = self.queue.head
            while current:
                if current.val.getTask() == task_content:
                    return current.val.getPriority()
                current = current.next
            return -1

    def getTask(self, priority):  # Gets the first task the matches the priority.
        with self.lock:
            current = self.queue.head
            while current:
                if current.val.getPriority() == priority:
                    return current.val
                current = current.next
            return None

    def removeTask(self, task): #Removes the first matching task
        with self.lock:
            current = self.queue.head
            previous = None

            while current:
                if current.val == task: 
                    if previous:
                        previous.next = current.next  # Remove the task from the linked list
                    else:
                        self.queue.head = current.next 
                    self.queue.size -= 1
                    return
                previous = current
                current = current.next


    def removeTaskT(self, task):
        with self.lock:
            current = self.queue.head
            previous = None

            while current:
                if current.val.getTask() == task:  
                    if previous:
                        previous.next = current.next  # Remove the task from the linked list
                    else:
                        self.queue.head = current.next 
                    self.queue.size -= 1
                    return
                previous = current
                current = current.next
        
    def getTaskT(self, task): #Get Task Using the task's name
        with self.lock:
            current = self.queue.head
            while current:
                if current.val.getTask() == task:
                    return current.val
                current = current.next
            return None

    def updatePriority(self, task, priority): #Updates the priority of the task.
        with self.lock:
          self.removeTask(task)
          task.setPriority(priority)
          self.enqueue(task)

# Testing the code
pq = PriorityQueue()
pq.enqueue(Task("Do laundry", 3))
pq.enqueue(Task("Finish report", 1))
pq.enqueue(Task("Buy groceries", 2))

print("\nQueue after enqueuing:")
pq.print()

print("\nDequeuing highest priority task")
pq.dequeue()
pq.print()

print("\nPeeking at the highest priority task:")
print(pq.peek(), "\n")

pq.print()