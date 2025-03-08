from typing import Generic, TypeVar

T = TypeVar('T') 


class Task(Generic[T]):


    def __init__(self, task: T, priority: int):
       
        self.task: T = task
        self.priority: int = priority

    def setPriority(self, priority: int):

        self.priority = priority

    def setTask(self, task: T):

        self.task = task

    def getTask(self) -> T:
 
        return self.task

    def getPriority(self) -> int:
  
        return self.priority

    def __str__(self) -> str:

        return "Task: " + str(self.task) + ", Priority: " + str(self.priority)

    def __lt__(self, other: 'Task[T]') -> bool:

        return self.priority < other.priority

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Task):
            return NotImplemented

        return self.priority == other.priority and self.task == other.task


class TaskComparator:

    def compare(self, t1: 'Task[T]', t2: 'Task[T]') -> int:

        return t1.priority - t2.priority