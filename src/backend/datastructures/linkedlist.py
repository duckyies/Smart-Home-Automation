import numpy
import typing
from threading import Lock
import threading

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
        self.lock = threading.Lock()

    def add_front(self, val):
        with self.lock:
            new_node = Node(val)
            new_node.next = self.head
            self.head = new_node
            self.size += 1

    def add_end(self, val):
        new_node = Node(val)

        with self.lock:
            if not self.head:
                self.head = new_node

            else:
                temp = self.head
                while temp.next:
                    temp = temp.next
                temp.next = new_node
            self.size += 1

    def remove_front(self):
        with self.lock:
            if not self.head:
                return None
            val = self.head.val
            self.head = self.head.next
            self.size -= 1
            return val

    def remove_end(self):

        with self.lock:
            if not self.head:
                return None
            if not self.head.next:
                val = self.head.val
                self.head = None
                self.size -= 1
                return val
            
            temp = self.head
            while temp.next and temp.next.next:
                temp = temp.next

            val = temp.next.val
            temp.next = None
            self.size -= 1
            return val

    def peek(self):
        with self.lock:
            return self.head.val if self.head else None

    def peek_end(self):
        with self.lock:
            if not self.head:
                return None
            temp = self.head
            while temp.next:
                temp = temp.next
            return temp.val

    def get_size(self):

        with self.lock:
            return self.size

    def print_list(self):

        with self.lock:
            temp = self.head
            while temp:
                print(temp.val, end=" -> ")
                temp = temp.next
            print("None")

    def clear(self):

        with self.lock:
            self.head = None
            self.size = 0

    def is_empty(self):

        with self.lock:
            return self.size == 0
        
ll = LinkedList()
ll.add_end(10)
ll.add_end(20)
ll.add_front(5)
ll.print_list()
print(ll.remove_end())
print(ll.peek())
print(ll.get_size())


