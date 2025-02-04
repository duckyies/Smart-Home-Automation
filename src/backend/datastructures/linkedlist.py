import numpy
import typing
from threading import Lock   # The threading library contains lock that helps us during multi threading operations.
import threading

class Node:    # For creation of a node. Each node contains the data and the address of the next node.
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkedList:   # Linked list implementation.
    def __init__(self):
        self.head = None
        self.size = 0
        self.lock = threading.Lock()

    def add_front(self, val):    # Adding a node in the front of the linked list.
        with self.lock:
            new_node = Node(val)
            new_node.next = self.head
            self.head = new_node
            self.size += 1

    def add_end(self, val):     # Adding a node at the end of the linked list.
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

    def remove_front(self):         # Removes the node at the front of the linked list.
        with self.lock:
            if not self.head:
                return None
            val = self.head.val
            self.head = self.head.next
            self.size -= 1
            return val

    def remove_end(self):           # Removes the node at the end of the linked list.

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

    def peek(self):                 # Gives us the data in the very first node without popping it.
        with self.lock:
            return self.head.val if self.head else None

    def peek_end(self):             # Gives us the data at the last node without popping it.
        with self.lock:
            if not self.head:
                return None
            temp = self.head
            while temp.next:
                temp = temp.next
            return temp.val

    def get_size(self):             # Gives us the size of the linked list.

        with self.lock:
            return self.size

    def print_list(self):           # Displays the entire list.

        with self.lock:
            temp = self.head
            while temp:
                print(temp.val, end=" -> ")
                temp = temp.next
            print("None")

    def clear(self):                   # Clears the entire list.

        with self.lock:
            self.head = None
            self.size = 0

    def is_empty(self):                # Checks if the list is empty.

        with self.lock:
            return self.size == 0
        
    def PeekandRemoveEnd(self):
        with self.lock:
            if not self.head:
                return None  # List is empty
                
            if not self.head.next:
                val = self.head.val  # Only one element in the list
                self.head = None
                self.size -= 1
                return val
            
            temp = self.head
            while temp.next and temp.next.next:
                temp = temp.next
            
            val = temp.next.val  # Peek the last element
            temp.next = None  # Remove it
            self.size -= 1
            return val


    
        
ll = LinkedList()
ll.add_end(10)
ll.add_end(20)
ll.add_front(5)
ll.print_list()
print(ll.remove_end())
print(ll.peek())
print(ll.get_size())
print(ll.PeekandRemoveEnd())
print(ll.peek_end())
print(ll.PeekandRemoveEnd())