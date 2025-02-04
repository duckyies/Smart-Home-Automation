from threading import Lock
import linkedlist

def sortLL(self):
        with self.lock:
            temp_array = self._make_array_list()  # Convert linked list to a Python list
            temp_array.sort()  # Sort the list in ascending order
            self.clear()  # Clear the linked list

            for val in temp_array:  # Reinsert sorted elements into the linked list
                self.add_end(val)



def _make_array_list(self):
    temp = self.head
    array_list = []

    while temp:
        array_list.append(temp.val)
        temp = temp.next

    return array_list
