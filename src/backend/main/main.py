#%% md
# # Smart Home Automation
# 
# **Team Number:** 1
# 
# **Team Members:**
# 
# *   Anirudh Jayan
# *   Abhinav Variyath
# *   Tara Samiksha
# *   Sarvesh Ram Kumar
# *   Aravind S Harilal
#%% md
# ## Introduction & Problem Statement
# 
# **Goal:** Create a Smart Home Automation System to manage electronic devices, optimize electricity consumption, and reduce energy wastage.
# 
# **Key Features:**
# 
# *   Device management using a **Priority Queue**
# *   Automation curr_rule implementation with a **Linked List**
# *   Energy-efficient device coordination
#%% md
# ## Priority Queue: Intelligent & Prioritized Device Task Handling
# 
# ### What is a Priority Queue?
# 
# A data structure that orders elements based on their priority, ensuring that higher priority elements are processed first.
# 
# ### Why Use a Priority Queue in a Smart Home?
# 
# *   **Real-world Prioritization:**  Different devices have varying levels of importance.
#     *   **Examples:**
#         *   Security Alarms (High Priority)
#         *   Lighting (Medium Priority)
#         *   Decorative Displays (Low Priority)
# *   **Resource Allocation:** Efficiently manages system resources by prioritizing critical tasks.
# 
# ### Priority Calculation
# 
# The priority of a device is determined by the following formula:
# Priority = Device Type Priority + Device Group Priority + (Location Occupancy * Weight)
# 
# 
# **Example:** A security camera in an occupied living room will have a higher priority than a decorative light in an empty bedroom.
#%% md
# # Normal Queue
# ![image.png](attachment:image.png)
# 
# # Priority Queue
# ![image-2.png](attachment:image-2.png)
#%%
import threading


class EmptyListAccessException(Exception):
    pass


class Task:  # Tasks with a set priority
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

            for i, task in enumerate(self.queue):  # Inserting the task in sorted order
                if task.priority > new_task.priority:
                    self.queue.insert(i, new_task)
                    return

            self.queue.append(new_task)  # If the task was not inserted earlier, we add it at the end

    def dequeue(self):  # Dequeuing the element with the most priority.
        with self.lock:
            if not self.queue:
                return None
            self.queue.pop(0)

    def peek(
            self):  # Returns the element with the most priority without dequeuing the element if the queue isn't empty.
        with self.lock:
            if self.queue:
                return self.queue[0]

            else:
                return None

    def print_queue(self):  # Prints the queue with the priorities too.
        with self.lock:
            for task in self.queue:
                print(f"Priority: {task.priority}, Task: {task.task}")

    def is_empty(self):  # Checks if the queue is empty.
        with self.lock:
            if len(self.queue):
                return True

            else:
                return False

    def size(self):  # Checks the size of the queue.
        with self.lock:
            return len(self.queue)

    def clear(self):  #clears the queue.
        with self.lock:
            self.queue.clear()

    def contains(self, task):  # Checks if the task is in the queue.
        with self.lock:
            if task in self.queue:
                return True

            else:
                return False

    def get_priority(self, task_content):  # Gets the priority of a given task.
        with self.lock:
            for task in self.queue:
                if task.task == task_content:
                    return task.priority
            return -1

    def get_task(self, priority):  # Gets the first task the matches the priority.
        with self.lock:
            for task in self.queue:
                if task.priority == priority:
                    return task
            return None

#%%
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

print(pq.get_priority("Buy groceries"))
pq.print_queue()
#%% md
# ## Linked List: Structured Rule Automation System
# 
# ### What is a Linked List?
# 
# A linear data structure where elements (nodes) are linked sequentially. It excels at dynamic insertion and deletion of elements.
# 
# ### Why Use a Linked List for Automation Rules?
# 
# *   **Ordered Rule Execution:**  Automation rules often need to be executed in a specific sequence.
# *   **Dynamic Rule Sets:** Easily add, remove, or modify rules without complex restructuring.
# 
# ### Rule Execution Process
# 
# 1. Rules are parsed from user input (or external sources) and converted into `Rule` objects.
# 2. `Rule` objects are added to the `LinkedList`.
#%% md
# # Normal List VS Linked List
# ![image.png](attachment:image.png)
#%%
# LINKED LIST IMPLEMENTATION
# The threading library contains lock that helps us during multi threading operations.
import threading


class Node:  # For creation of a node. Each node contains the data and the address of the next node.
    def __init__(self, val):
        self.val = val
        self.next = None


class LinkedList:  # Linked list implementation.
    def __init__(self):
        self.head = None
        self.size = 0
        self.lock = threading.Lock()

    def add_front(self, val):  # Adding a node in the front of the linked list.
        with self.lock:
            new_node = Node(val)
            new_node.next = self.head
            self.head = new_node
            self.size += 1

    def add_end(self, val):  # Adding a node at the end of the linked list.
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

    def remove_front(self):  # Removes the node at the front of the linked list.
        with self.lock:
            if not self.head:
                return None
            val = self.head.val
            self.head = self.head.next
            self.size -= 1
            return val

    def remove_end(self):  # Removes the node at the end of the linked list.

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

    def peek(self):  # Gives us the data in the very first node without popping it.
        with self.lock:
            return self.head.val if self.head else None

    def peek_end(self):  # Gives us the data at the last node without popping it.
        with self.lock:
            if not self.head:
                return None
            temp = self.head
            while temp.next:
                temp = temp.next
            return temp.val

    def get_size(self):  # Gives us the size of the linked list.

        with self.lock:
            return self.size

    def print_list(self):  # Displays the entire list.

        with self.lock:
            temp = self.head
            while temp:
                print(temp.val, end=" -> ")
                temp = temp.next
            print("None")

    def clear(self):  # Clears the entire list.

        with self.lock:
            self.head = None
            self.size = 0

    def is_empty(self):  # Checks if the list is empty.

        with self.lock:
            return self.size == 0

    def PeekandRemoveEnd(self):  # Peek and pop the last element.
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

    def PeekandRemove(self):  # Peeks and pops the first element
        with self.lock:
            if not self.head:
                return None  # List is empty
            val = self.head.val  # Peek the first element
            self.head = self.head.next  # Remove it
            self.size -= 1
            return val

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

    def reverse(self):  # Reverses the array
        with self.lock:
            temp_array = self.make_array_list()
            temp_array.reverse()
            self.clear()

            for val in temp_array:
                self.add_end(val)


#%%
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
ll.add_end(20)
print(ll.peek())
print(ll.PeekandRemove())
#%% md
# ## Energy-Efficient Device Coordination
# 
# This system employs a two-pronged approach to optimize energy consumption:
# 
# ### 1. Rule-Based Energy Optimization (Linked List)
# 
# *   Users can define energy-saving rules, such as:
#     *   "If the time is after 11 PM and motion is not detected in the living room for 15 minutes, turn off the living room lights."
# *   The `LinkedList` ensures that these rules are executed efficiently and in the correct order.
#%%
class Rule:
    def __init__(self, deviceId, flipState, turnOn, turnOff, setPowerLevel, powerLevel, groupName, turnGroupOff,
                 turnGroupOn, typeName, turnTypeOff, turnTypeOn, locationName, turnLocationOff, turnLocationOn):
        self.__deviceId = deviceId
        self.__flipState = flipState
        self.__turnOn = turnOn
        self.__turnOff = turnOff
        self.__setPowerLevel = setPowerLevel
        self.__powerLevel = powerLevel
        self.__groupName = groupName
        self.__turnGroupOff = turnGroupOff
        self.__turnGroupOn = turnGroupOn
        self.__typeName = typeName
        self.__turnTypeOff = turnTypeOff
        self.__turnTypeOn = turnTypeOn
        self.__locationName = locationName
        self.__turnLocationOff = turnLocationOff
        self.__turnLocationOn = turnLocationOn

    def get_deviceId(self):
        return self.__deviceId

    def set_deviceId(self, deviceId):
        self.__deviceId = deviceId

    def get_flipState(self):
        return self.__flipState

    def set_flipState(self, flipState):
        self.__flipState = flipState

    def get_turnOn(self):
        return self.__turnOn

    def set_turnOn(self, turnOn):
        self.__turnOn = turnOn

    def get_turnOff(self):
        return self.__turnOff

    def set_turnOff(self, turnOff):
        self.__turnOff = turnOff

    def get_setPowerLevel(self):
        return self.__setPowerLevel

    def set_setPowerLevel(self, setPowerLevel):
        self.__setPowerLevel = setPowerLevel

    def get_powerLevel(self):
        return self.__powerLevel

    def set_powerLevel(self, powerLevel):
        self.__powerLevel = powerLevel

    def get_groupName(self):
        return self.__groupName

    def set_groupName(self, groupName):
        self.__groupName = groupName

    def get_turnGroupOff(self):
        return self.__turnGroupOff

    def set_turnGroupOff(self, turnGroupOff):
        self.__turnGroupOff = turnGroupOff

    def get_turnGroupOn(self):
        return self.__turnGroupOn

    def set_turnGroupOn(self, turnGroupOn):
        self.__turnGroupOn = turnGroupOn

    def get_typeName(self):
        return self.__typeName

    def set_typeName(self, typeName):
        self.__typeName = typeName

    def get_turnTypeOff(self):
        return self.__turnTypeOff

    def set_turnTypeOff(self, turnTypeOff):
        self.__turnTypeOff = turnTypeOff

    def get_turnTypeOn(self):
        return self.__turnTypeOn

    def set_turnTypeOn(self, turnTypeOn):
        self.__turnTypeOn = turnTypeOn

    def get_locationName(self):
        return self.__locationName

    def set_locationName(self, locationName):
        self.__locationName = locationName

    def get_turnLocationOff(self):
        return self.__turnLocationOff

    def set_turnLocationOff(self, turnLocationOff):
        self.__turnLocationOff = turnLocationOff

    def get_turnLocationOn(self):
        return self.__turnLocationOn

    def set_turnLocationOn(self, turnLocationOn):
        self.__turnLocationOn = turnLocationOn

    def __str__(self):
        return f"Rule(deviceId={self.__deviceId}, flipState={self.__flipState}, turnOn={self.__turnOn}, turnOff={self.__turnOff}, setPowerLevel={self.__setPowerLevel}, powerLevel={self.__powerLevel}, groupName={self.__groupName}, turnGroupOff={self.__turnGroupOff}, turnGroupOn={self.__turnGroupOn}, typeName={self.__typeName}, turnTypeOff={self.__turnTypeOff}, turnTypeOn={self.__turnTypeOn}, locationName={self.__locationName}, turnLocationOff={self.__turnLocationOff}, turnLocationOn={self.__turnLocationOn})"


#TESTING
rule = Rule("123", True, False, True, False, 0, "Living Room", False, True, "Light", False, True, "Home", False, True)
print(rule)
#%% md
# ### 2. Priority Queue Driven Power Management
# 
# *   **Monitoring:** The system continuously monitors overall power consumption against a predefined threshold.
# *   **Threshold Exceeded:** If the power consumption threshold is exceeded, the `Priority Queue` identifies devices with lower priority.
# *   **Dynamic Rule Generation:** The system automatically creates and adds rules to the `LinkedList` to reduce power consumption for lower-priority devices. These rules might involve:
#     *   Turning off the device.
#     *   Reducing the power level (e.g., dimming lights).
# *   **Dynamic Adaptation:** The system continuously adapts to power usage, adjusting device states based on priority and rules to maintain energy efficiency in real-time.
# 
#%%
from datetime import datetime
import time


class Device:
    def __init__(self, device_id, device_name, device_type, location, device_group, battery_level, max_battery_capacity,
                 current_battery_capacity, is_on_battery, is_turned_on, base_power_consumption, power_level,
                 turned_on_time, is_interacted):
        self.__device_id = device_id
        self.__device_name = device_name
        self.__device_type = device_type
        self.__location = location
        self.__device_group = device_group
        self.__battery_level = battery_level
        self.__max_battery_capacity = max_battery_capacity
        self.__current_battery_capacity = current_battery_capacity
        self.__is_on_battery = is_on_battery
        self.__is_turned_on = is_turned_on
        self.__base_power_consumption = base_power_consumption
        self.__power_level = power_level
        self.__turned_on_time = turned_on_time
        self.__is_interacted = is_interacted

    def flip_interaction_state(self):
        self.__is_interacted = not self.__is_interacted

    def get_interaction_state(self) -> bool:
        return self.__is_interacted

    def get_minutes_since_turned_on(self):
        if self.__turned_on_time:
            return int((int(time.time()) - self.__turned_on_time) // 60)
        return 0

    def set_turned_on(self, status: bool):
        self.__is_turned_on = status

    def is_turned_on(self) -> bool:
        return self.__is_turned_on

    def set_battery_level(self, level: float):
        self.__battery_level = level

    def get_battery_level(self) -> float:
        return self.__battery_level

    def set_base_power_consumption(self, consumption: float):
        self.__base_power_consumption = consumption

    def get_base_power_consumption(self) -> float:
        return self.__base_power_consumption

    def set_battery_capacity(self, capacity: int):
        self.__max_battery_capacity = capacity

    def get_battery_capacity(self) -> int:
        return self.__max_battery_capacity

    def get_device_id(self) -> int:
        return self.__device_id

    def get_device_name(self) -> str:
        return self.__device_name

    def set_device_name(self, name: str):
        self.__device_name = name

    def get_device_type(self):
        return self.__device_type

    def set_device_type(self, type_: str):
        self.__device_type = type_

    def get_location(self):
        return self.__location

    def set_location(self, location: str):
        self.__location = location

    def get_device_group(self):
        return self.__device_group

    def set_device_group(self, group: str):
        self.__device_group = group

    def get_power_level(self) -> int:
        return self.__power_level

    def set_power_level(self, level: int):
        self.__power_level = level

    def is_on_battery_power(self) -> bool:
        return self.__is_on_battery

    def set_on_battery(self, status: bool):
        self.__is_on_battery = status

    def get_current_battery_capacity(self) -> float:
        return self.__current_battery_capacity

    def set_current_battery_capacity(self, capacity: float):
        self.__current_battery_capacity = capacity

    def set_turned_on_time(self, time: int):
        self.__turned_on_time = time

    def get_turned_on_time(self) -> int:
        return self.__turned_on_time

    def __str__(self):
        return (f"Device ID: {self.get_device_id()}\n"
                f"Device Name: {self.get_device_name()}\n"
                f"Device Type: {self.get_device_type()}\n"
                f"Device Group: {self.get_device_group()}\n"
                f"Location: {self.get_location()}\n"
                f"Power Status: {'On' if self.is_turned_on() else 'Off'}\n"
                f"Battery Level: {self.get_battery_level()}\n"
                f"Power Consumption: {self.get_base_power_consumption()} W\n"
                f"Power Level: {self.get_power_level()}\n")


#Test

device1 = Device(
    device_id=1,
    device_name="Light",
    device_type="Decorative",
    location="Living Room",
    device_group="LIGHTS",
    battery_level=85.0,
    max_battery_capacity=100,
    current_battery_capacity=85.0,
    is_on_battery=False,
    is_turned_on=True,
    base_power_consumption=10.0,
    power_level=5,
    turned_on_time=int(time.time()),
    is_interacted=False,

)

print(device1)

device1.set_battery_level(90.0)
device1.set_power_level(8)
device1.flip_interaction_state()

print(f"Battery Level after update: {device1.get_battery_level()}")
print(f"Power Level after update: {device1.get_power_level()}")
print(f"Interaction State: {device1.get_interaction_state()}")
print(f"Minutes since turned on: {device1.get_minutes_since_turned_on()} min")

#%%
class AirConditioner(Device):
    def __init__(self, device_name, device_type, device_group, location, is_turned_on, battery_level, power_consumption,
                 max_battery_capacity, power_level, mode):
        super().__init__(device_name, device_type, device_group, location, is_turned_on, battery_level,
                         power_consumption, max_battery_capacity, power_level)
        self.__mode = mode
        self.__simulation_temp_change_time = 0

    def get_mode(self) -> bool:
        return self.__mode

    def set_mode(self, mode: bool):
        self.__mode = mode

    def toggle_mode(self):
        self.__mode = not self.__mode

    def get_simulation_temp_change_time(self) -> int:
        return self.__simulation_temp_change_time

    def set_simulation_temp_change_time(self, simulation_temp_change_time: int):
        self.__simulation_temp_change_time = simulation_temp_change_time

    def get_minutes_since_temp_change(self) -> int:
        return int((int(time.time()) - self.__simulation_temp_change_time) // 60)

    def __str__(self) -> str:
        return super().__str__() + " Mode: " + ("Cooling" if self.__mode else "Heating")

#%% md
# ### 3. Enum Based Priority Calculation
# 
# *   **Easy Modification:** Modifying priority values is as simple as changing one number
# *   **Fast and Easy Calculation:** All priority values can be accessed and calculated very easily
# *   **Ease of Use** User does not have to manually include priority values for every single device added
#%%
from enum import Enum


class DeviceGroupEnum(Enum):
    LIGHTS = 10
    FANS = 9
    ALARMS = 15
    CAMERAS = 14
    AIRCONDITIONERS = 8
    HEATERS = 8
    APPLIANCES = 6
    GARDENING = 3
    ENTERTAINMENT = 2
    CLEANING = 5
    LAUNDRY = 4
    WEARABLES = 7
    BATHROOM = 12
    OTHERS = 1

    dict = {"abc": 1}

    def get_priority(self):
        return self.value


class DeviceGroup:
    def __init__(self, group_name: str):
        self.group_name = group_name
        self.devices = []

    def add_device(self, device: Device):
        self.devices.append(device)

    def remove_device(self, device: Device):
        if device in self.devices:
            self.devices.remove(device)

    def get_devices(self):
        return self.devices

    def turn_off_all_devices(self):
        for device in self.devices:
            device.set_turned_on(False)

    def turn_on_all_devices(self):
        for device in self.devices:
            device.set_turned_on(True)

    def get_device_by_name(self, name: str):
        name_lower = name.lower()
        return next((device for device in self.devices if name_lower in device.get_device_name().lower()), None)

    def get_device_by_id(self, device_id: int):
        return next((device for device in self.devices if device.get_device_id() == device_id), None)

    def get_group_name(self):
        return self.group_name
#%%
from enum import Enum


class DeviceTypeEnum(Enum):
    DECORATIVE = 1,
    HEALTH = 15,
    ENTERTAINMENT = 3,
    SECURITY = 20,
    PERSONALCARE = 7,
    CONNECTIVITY = 10,
    COOKING = 12,
    LUXURY = 2,
    OFFICE = 10,
    OTHERS = 5

    def get_priority(self):
        return self.value


class DeviceType:
    def __init__(self, typeName: str):
        self.typeName = typeName
        self.devices = []

    def add_device(self, device: Device):
        self.devices.append(device)

    def remove_device(self, device: Device):
        if device in self.devices:
            self.devices.remove(device)

    def get_devices(self):
        return self.devices

    def turn_off_all_devices(self):
        for device in self.devices:
            device.set_turned_on(False)

    def turn_on_all_devices(self):
        for device in self.devices:
            device.set_turned_on(True)

    def get_device_by_name(self, name: str):
        name_lower = name.lower()
        return next((device for device in self.devices if name_lower in device.get_device_name().lower()), None)

    def get_device_by_id(self, device_id: int):
        return next((device for device in self.devices if device.get_device_id() == device_id), None)


#%%
from enum import Enum


class DeviceLocationEnum(Enum):
    LIVINGROOM = "Living Room"
    BEDROOM = "Bedroom"
    BEDROOM2 = "Bedroom 2"
    BEDROOM3 = "Bedroom 3"
    BEDROOM4 = "Bedroom 4"
    GARDEN = "Garden"
    OFFICE = "Office"
    ENTRANCE = "Entrance"
    KITCHEN = "Kitchen"
    BATHROOM = "Bathroom"
    BATHROOM2 = "Bathroom 2"
    BATHROOM3 = "Bathroom 3"
    OTHERS = "Others"


class DeviceLocation:
    def __init__(self, location: str):
        self.location = location
        self.devices = []
        self.people = 0
        self.temperature = 0.0

    def add_device(self, device: Device):

        self.devices.append(device)

    def remove_device(self, device: Device):

        if device in self.devices:
            self.devices.remove(device)

    def get_devices(self):

        return self.devices

    def get_people(self):
        return self.people

    def set_people(self, people: int):
        self.people = people

    def add_people(self, people: int):
        self.people += people

    def remove_people(self, people: int):
        self.people = max(0, self.people - people)

    def turn_off_all_devices(self):

        for device in self.devices:
            device.set_turned_on(False)

    def turn_on_all_devices(self):

        for device in self.devices:
            device.set_turned_on(True)

    def get_temperature(self):
        return self.temperature

    def set_temperature(self, temperature: float):
        self.temperature = temperature

    def get_device_by_name(self, name: str):

        name_lower = name.lower()
        return next((device for device in self.devices if name_lower in device.get_device_name().lower()), None)

    def get_device_by_id(self, device_id: int):

        return next((device for device in self.devices if device.get_device_id() == device_id), None)

    def __str__(self):
        return f"Location: {self.location}"
#%% md
# ### 4. Logging system
# 
# *   **Log Monitoring:** Displays system logs for transparency and debugging, including:
#     *   Info logs
#     *   Warning logs
#     *   Severe logs
#     *   Power logs
#     *   Battery logs
#%%
import logging
from functools import total_ordering


class LogTask:
    LEVEL_LIST = [
        logging.ERROR,
        logging.CRITICAL,
        logging.WARNING,
        logging.INFO
    ]

    def __init__(self, log_level, message):
        self.logLevel = log_level
        self.message = message

    def getLogLevel(self):
        return self.logLwevel

    def getMessage(self):
        return self.message

    def setLogLevel(self, logLevel):
        self.logLevel = logLevel

    def setMessage(self, message):
        self.message = message

#%% md
# #Exceptions
# 
#%%
class RuleParsingException(Exception):

    def __init__(self, message: str = "Rule parsing error", cause: Exception | None = None):
        super().__init__(message)
        self.cause = cause

    def __str__(self) -> str:
        return f"RuleParsingException: {super().__str__()}"
#%% md
# ### SmartHome.py Overview
# 
# **Integrating code**
# - Acts as the primary controller, integrating all device and data structure functionalities  
# - Manages device objects for efficient monitoring and control  
# - Enforces power consumption thresholds to optimize energy usage  
# - Maintains, checks, and updates battery levels across connected devices  
# 
# **Logging**
# - Logs key events, enhancing transparency and debugging  
# 
# **Priority Management**
# - Coordinates with the Priority Queue to handle high-priority device tasks  
# - Leverages the Linked List to manage and execute automation rules in a defined order  
# - Ensures continuous, coordinated operation among devices, rules, and system events
#%%
import logging
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures


class SmartHome:

    def __init__(self, threshold: float, ideal_temp: int, simulate: bool):

        self.tickCount = 0
        self.threshold = threshold
        self.idealTemp = ideal_temp
        self.simulate = simulate
        self.powerConsumption = 1.0
        self.mode = "Normal"
        self.date = time.time()
        self.lock = threading.Lock()
        self.random = random.Random()

        self.groupMap: dict[str, DeviceGroup] = {}
        self.typeMap: dict[str, DeviceType] = {}
        self.locationMap: dict[str, DeviceLocation] = {}

        self.poweredOnDevices: list[Device] = []
        self.poweredOffDevices: list[Device] = []

        self.deviceQueue: PriorityQueue[Task[Device, int]] = PriorityQueue()
        self.powerReducibleDevices = PriorityQueue()
        self.turnBackOnDevices = PriorityQueue()

        self.loggingList = LinkedList()
        self.powerConsumptionLogList: LinkedList[LogTask] = LinkedList()
        self.deviceBatteryLogList = LinkedList()

        self.ruleList = LinkedList()

        self.infoTasks: list[str] = []
        self.warningTasks: list[str] = []
        self.severeTasks: list[str] = []
        self.powerConsumptionTasks: list[str] = []
        self.deviceBatteryTasks: list[str] = []
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.powerConsumptionlogger = logging.getLogger("PowerConsumptionLog")
        self.logger = logging.getLogger(__name__)
        self.deviceBatteryLogger = logging.getLogger("DeviceBatteryLog")

        # Thread control
        self.tick_thread = None
        self.logging_thread = None
        self.rule_thread = None

        self.tick_running = False
        self.logging_running = False
        self.rule_running = False

        self.initializeLogger()  # Initialize loggers once
        self._initialize()
        self._initializeScheduler()

    def _initialize(self):

        for deviceGroup in DeviceGroupEnum:
            self.groupMap[deviceGroup.name] = DeviceGroup(deviceGroup.name)

        for deviceType in DeviceTypeEnum:
            self.typeMap[deviceType.name] = DeviceType(deviceType.name)

        for location in DeviceLocationEnum:
            devLocation = DeviceLocation(location.name)
            self.locationMap[location.name] = devLocation
            devLocation.temperature = self.random.randint(10, 45)

    # ========================================================================
    # Device Management
    # ========================================================================

    def _addToGroupAndType(self, deviced: Device):

        self.groupMap[deviced.get_device_group().name].add_device(deviced)
        self.typeMap[deviced.get_device_type().name].add_device(deviced)
        self.locationMap[deviced.get_location().name].add_device(deviced)

    def createDevice(
            self,
            deviceName: str,
            deviceType: DeviceTypeEnum,
            deviceGroup: DeviceGroupEnum,
            location: DeviceLocationEnum,
            isTurnedOn: bool = False,
            batteryLevel: float = 0.0,
            powerConsumption: float = 0.0,
            maxBatteryCapacity: int = 0,
            powerLevel: int = 1,
    ) -> Device:
        return Device(
            device_id=len(self.getDevices()) + 1,  #Simple ID assignment
            device_name=deviceName,
            device_type=deviceType,
            location=location,
            device_group=deviceGroup,
            is_turned_on=isTurnedOn,
            battery_level=batteryLevel,
            base_power_consumption=powerConsumption,
            max_battery_capacity=maxBatteryCapacity,
            current_battery_capacity=maxBatteryCapacity,
            power_level=powerLevel,
            is_on_battery=False,
            turned_on_time=int(time.time()) if isTurnedOn else 0,
            is_interacted=False,
        )

    def addDevice(self, device: Device):

        if device.is_turned_on():
            self.poweredOnDevices.append(device)
            device.set_turned_on_time(time.time())

            if device.get_device_type().get_priority()[0] == float("inf"):
                return
            location = self.locationMap[device.get_location().name]

            self.deviceQueue.enqueue(
                Task(device, device.get_device_type().get_priority()[
                    0] + device.get_device_group().get_priority() + location.people * 10)
            )

            if device.get_power_level() != 0:
                if device.get_device_type().get_priority()[0] == float("inf"):
                    return
                location = self.locationMap[device.get_location().name]

                self.powerReducibleDevices.enqueue(
                    Task(
                        device,
                        device.get_device_type().get_priority()[0]
                        + device.get_device_group().get_priority()
                        + (location.people * 10),
                    )
                )
        else:
            self.poweredOffDevices.append(device)
        self._addToGroupAndType(device)

    def turnOnDevice(self, device: Device):

        device.set_turned_on(True)

        if device not in self.poweredOnDevices:
            self.poweredOnDevices.append(device)
            device.set_turned_on_time(time.time())

        if device in self.poweredOffDevices:
            self.poweredOffDevices.remove(device)
        if device.get_device_type().priority == float("inf"):
            return
        location = self.locationMap[device.get_location().name]

        self.deviceQueue.put(
            Task(
                device,
                device.get_device_type().priority
                + device.get_device_group().priority
                + (location.people * 10),
            )
        )
        if device.get_power_level() != 0:
            if device.get_device_type().priority == float("inf"):
                return
            location = self.locationMap[device.get_location().name]

        self.powerReducibleDevices.put(
            Task(
                device,
                device.get_device_type().priority
                + device.get_device_group().priority
                + (location.people * 10),
            )
        )

    def turnOffDevice(self, device: Device):

        device.set_turned_on(False)
        if device not in self.poweredOffDevices:
            self.poweredOffDevices.append(device)

        if device in self.poweredOnDevices:
            self.poweredOnDevices.remove(device)

        self.deviceQueue.queue = [task for task in self.deviceQueue.queue if task.task != device]
        self.powerReducibleDevices.queue = [task for task in self.powerReducibleDevices.queue if task.task != device]

    def removeDevice(self, device: Device):

        if device in self.poweredOnDevices:
            self.poweredOnDevices.remove(device)
        if device in self.poweredOffDevices:
            self.poweredOffDevices.remove(device)
        self.groupMap[device.get_device_group().name].remove_device(device)
        self.typeMap[device.get_device_type().name].remove_device(device)
        self.locationMap[device.get_location().name].remove_device(device)

    def getDeviceByName(self, name: str) -> Device | None:

        for device in self.poweredOnDevices:
            if device.get_device_name().lower() == name.lower():
                return device
        for device in self.poweredOffDevices:
            if device.get_device_name().lower() == name.lower():
                return device
        return None

    def getDeviceByID(self, deviceId: int) -> Device | None:

        for device in self.poweredOnDevices:
            if device.get_device_id() == deviceId:
                return device
        for device in self.poweredOffDevices:
            if device.get_device_id() == deviceId:
                return device
        return None

    def turnOffDevicesByGroup(self, groupName: str):

        for device in self.groupMap[groupName].devices:
            self.turnOffDevice(device)

    def turnOnDevicesByGroup(self, groupName: str):

        for device in self.groupMap[groupName].devices:
            self.turnOnDevice(device)

    def turnOffDevicesByType(self, typeName: str):

        for device in self.typeMap[typeName].devices:
            self.turnOffDevice(device)

    def turnOnDevicesByType(self, typeName: str):

        for device in self.typeMap[typeName].devices:
            self.turnOnDevice(device)

    def turnOffDevicesByLocation(self, locationName: str):

        for device in self.locationMap[locationName].devices:
            self.turnOffDevice(device)

    def turnOnDevicesByLocation(self, locationName: str):

        for device in self.locationMap[locationName].devices:
            self.turnOnDevice(device)

    def turnOffAllDevices(self):

        for device in list(self.poweredOnDevices):
            self.turnOffDevice(device)

    def turnOnAllDevices(self):

        for device in list(self.poweredOffDevices):
            self.turnOnDevice(device)

    def getDevice(self, identifier: str | int) -> Device | None:

        if isinstance(identifier, int):
            return self.getDeviceByID(identifier)
        elif isinstance(identifier, str):
            return self.getDeviceByName(identifier)
        else:
            return None

    def addPerson(self, location: DeviceLocationEnum):

        if isinstance(location, DeviceLocationEnum):
            locationObj = self.locationMap[location.name]
        else:
            locationObj = location

        locationObj.add_people(1)
        for device in locationObj.devices:
            if device.is_turned_on():
                for i, task in enumerate(self.deviceQueue.queue):
                    if task.task == device:
                        new_priority = task.priority + 10
                        self.deviceQueue.queue[i] = Task(device, new_priority)
                        break
                self.deviceQueue.queue.sort()  # Re-sort after updating priority

    def removePerson(self, location: DeviceLocationEnum):

        if isinstance(location, DeviceLocationEnum):
            locationObj = self.locationMap[location.name]
        else:
            locationObj = location

        if locationObj.people == 0:
            return

        locationObj.remove_people(1)

        for device in locationObj.devices:
            if device.is_turned_on():
                for i, task in enumerate(self.deviceQueue.queue):
                    if task.task == device:
                        new_priority = task.priority - 10
                        self.deviceQueue.queue[i] = Task(device, new_priority)
                        break
        self.deviceQueue.queue.sort()

    # ========================================================================
    # Tick and Scheduling
    # ========================================================================

    def _initializeScheduler(self):

        self.scheduler = ThreadPoolExecutor(max_workers=3)
        self.startTick()
        self.logger.info("Tick started")
        self.startLogging()
        self.logger.info("Logging started")
        self.startRuleExecution()

    def startTick(self):
        if not self.tick_running:
            self.tick_running = True
            self.tick_thread = self.scheduler.submit(self._runTickPeriodically)

    def _runTickPeriodically(self):
        while self.tick_running:
            start_time = time.time()
            self.tick()
            end_time = time.time()
            execution_time = end_time - start_time
            sleep_time = max(0, 1 - execution_time)
            time.sleep(sleep_time)

    def stopTick(self):
        if self.tick_running:
            self.tick_running = False
            if self.tick_thread:
                self.tick_thread.cancel()
                self.tick_thread = None

    def tick(self):
        try:
            self.tickTask()
        except Exception as e:
            self.logger.error(f"Error during tick execution: {e}")
            self.logger.exception(e)

    def checkPowerConsumption(self):

        currPowerConsumption = self.calculateCurrentPowerConsumption()

        if currPowerConsumption > self.threshold:
            reducePowerTask = self.powerReducibleDevices.dequeue()
            if reducePowerTask is not None:
                device = reducePowerTask.task

                if (
                        currPowerConsumption
                        - (device.get_base_power_consumption() * (device.get_power_level() - 1))
                        > self.threshold
                ):
                    self.powerReducibleDevices.enqueue(reducePowerTask)
                    removeTask = self.deviceQueue.dequeue()
                    if removeTask is not None:
                        removeDevice = removeTask.task

                        self.logger.info(
                            f"Reducing power consumption by turning off {device.get_device_name()}"
                        )

                        self.turnOffDevice(removeDevice)
                        self.turnBackOnDevices.enqueue(
                            Task(device, -removeTask.priority)
                        )
                else:
                    device.set_power_level(1)

        else:
            turnBackOnTask = self.turnBackOnDevices.dequeue()
            if turnBackOnTask is not None:
                turnBackOnDevice = turnBackOnTask.task
                if (currPowerConsumption + (
                        turnBackOnDevice.get_base_power_consumption() * turnBackOnDevice.get_power_level()) > self.threshold):
                    self.logger.info(
                        f"Not turning back on {turnBackOnTask.task.get_device_name()}"
                    )
                    turnBackOnTask.priority = turnBackOnTask.priority + 3
                    self.turnBackOnDevices.enqueue(turnBackOnTask)
                    return
                self.logger.info(
                    f"Turning back on {turnBackOnTask.task.get_device_name()}"
                )

                self.turnOnDevice(turnBackOnDevice)

    def tickTask(self):

        self.tickCount += 1
        if self.tickCount % 2 == 0:
            try:
                if self.simulate:
                    self.simulateDeviceChange()
                self.realisticPowerConsumption()
            except Exception as e:
                self.logger.error(f"Error during deviceChange execution: {e}")
                self.logger.exception(e)
        try:
            self.logPowerConsumption()
            self.reduceBatteryTick()
            self.checkEachDevice()
            self.checkEachLocation()
            self.checkPowerConsumption()
        except Exception as e:
            self.logger.error(f"Error during tickTask execution: {e}")
            self.logger.exception(e)

    def startRuleExecution(self):
        if not self.rule_running:
            self.rule_running = True
            self.rule_thread = self.scheduler.submit(self._runExecuteRulesPeriodically)

    def _runExecuteRulesPeriodically(self):
        while self.rule_running:
            start_time = time.time()
            self.executeRules()
            end_time = time.time()
            execution_time = end_time - start_time
            sleep_time = max(0, 1 - execution_time)
            time.sleep(sleep_time)

    def executeRules(self):

        rule = self.ruleList.peekAndRemove()
        while rule is not None:
            self.executeRule(rule)
            rule = self.ruleList.peekAndRemove()

    def stopRuleExecution(self):
        if self.rule_running:
            self.rule_running = False
            if self.rule_thread:
                self.rule_thread.cancel()
                self.rule_thread = None

    # ========================================================================
    # Logging
    # ========================================================================

    def initializeLogger(self):

        infoFileHandler = None
        warningFileHandler = None
        severeFileHandler = None
        powerConsumptionFileHandler = None
        deviceBatteryFileHandler = None

        try:
            self.powerConsumptionlogger.setLevel(logging.INFO)
            powerConsumptionFileHandler = logging.FileHandler("PowerConsumption.log")
            powerConsumptionFileHandler.setLevel(logging.INFO)
            powerConsumptionFileHandler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))

            infoFileHandler = logging.FileHandler("Info.log")
            infoFileHandler.setLevel(logging.INFO)
            infoFileHandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            # infoFileHandler.addFilter(lambda record: record.levelno == logging.INFO) # Removed Lambda filters

            warningFileHandler = logging.FileHandler("Warning.log")
            warningFileHandler.setLevel(logging.WARNING)
            warningFileHandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            # warningFileHandler.addFilter(lambda record: record.levelno == logging.WARNING)

            severeFileHandler = logging.FileHandler("Severe.log")
            severeFileHandler.setLevel(logging.CRITICAL)
            severeFileHandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            # severeFileHandler.addFilter(lambda record: record.levelno == logging.CRITICAL)

            self.deviceBatteryLogger.setLevel(logging.INFO)
            deviceBatteryFileHandler = logging.FileHandler("DeviceBattery.log")
            deviceBatteryFileHandler.setLevel(logging.INFO)
            deviceBatteryFileHandler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))

            self.logger.addHandler(infoFileHandler)
            self.logger.addHandler(warningFileHandler)
            self.logger.addHandler(severeFileHandler)
            self.powerConsumptionlogger.addHandler(powerConsumptionFileHandler)
            self.deviceBatteryLogger.addHandler(deviceBatteryFileHandler)

            # Prevent duplicate logging
            self.powerConsumptionlogger.propagate = False
            self.logger.propagate = False
            self.deviceBatteryLogger.propagate = False

        except Exception as e:
            print(e)

    def startLogging(self):
        if not self.logging_running:
            self.logging_running = True
            self.logging_thread = self.scheduler.submit(self._runLogPeriodically)

    def _runLogPeriodically(self):
        while self.logging_running:
            start_time = time.time()
            self.log()
            end_time = time.time()
            execution_time = end_time - start_time
            sleep_time = max(0, 2 - execution_time)
            time.sleep(sleep_time)

    def log(self):

        task = self.loggingList.peekAndRemove()
        powerTask = self.powerConsumptionLogList.peekAndRemove()
        batteryTask = self.deviceBatteryLogList.peekAndRemove()

        while task is not None:
            self.logger.log(task.logLevel, task.message)
            task = self.loggingList.peekAndRemove()

        while powerTask is not None:
            self.powerConsumptionlogger.log(powerTask.logLevel, powerTask.message)
            powerTask = self.powerConsumptionLogList.peekAndRemove()

        while batteryTask is not None:
            self.deviceBatteryLogger.log(batteryTask.logLevel, batteryTask.message)
            batteryTask = self.deviceBatteryLogList.peekAndRemove()

    def addLog(self, logLevel, message):

        if logLevel == logging.INFO:
            self.infoTasks.append(message)

        elif logLevel == logging.WARNING:
            self.warningTasks.append(message)

        elif logLevel == logging.CRITICAL:
            self.severeTasks.append(message)
        self.loggingList.add_end(LogTask(logLevel, message))

    def addPowerLog(self, logLevel, message):

        self.powerConsumptionLogList.add_end(LogTask(logLevel, message))
        self.powerConsumptionTasks.append(message)
        if logLevel != logging.INFO:
            self.addLog(logLevel, message)

    def addBatteryLog(self, logLevel, message):

        self.deviceBatteryLogList.add_end(LogTask(logLevel, message))
        self.deviceBatteryTasks.append(message)
        if logLevel != logging.INFO:
            self.addLog(logLevel, message)

    def stopLogging(self):
        if self.logging_running:
            self.logging_running = False
            if self.logging_thread:
                self.logging_thread.cancel()
                self.logging_thread = None

    # ========================================================================
    # Power Management
    # ========================================================================

    def calculateCurrentBasePowerConsumption(self) -> float:

        return sum(device.get_base_power_consumption() for device in self.poweredOnDevices)

    def calculateCurrentPowerConsumption(self) -> float:

        return sum(
            device.get_base_power_consumption() * (device.get_power_level() if device.get_power_level() > 0 else 1)
            for device in self.poweredOnDevices
        )

    def logPowerConsumption(self):

        self.powerConsumption = self.calculateCurrentPowerConsumption()

        if self.powerConsumption > self.threshold * 1.5:
            message = f"Power consumption is {self.powerConsumption}W, which is {(self.powerConsumption - self.threshold) / self.threshold * 100:.2f} percent above the threshold"
            self.addPowerLog(logging.ERROR, message)  # Use logging.ERROR for SEVERE
        elif self.powerConsumption > self.threshold:
            message = f"Power consumption is {self.powerConsumption}W, which is {(self.powerConsumption - self.threshold) / self.threshold * 100:.2f} percent above the threshold"
            self.addPowerLog(logging.WARNING, message)
        else:
            message = f"Power consumption - {self.powerConsumption}W, {self.powerConsumption / self.threshold * 100:.2f} percent of threshold"
            self.addPowerLog(logging.INFO, message)

    def getPowerConsumption(self) -> float:

        return self.powerConsumption

    def realisticPowerConsumption(self):

        for device in self.poweredOnDevices:
            if self.random.random() >= 0.9:
                device.set_base_power_consumption(
                    device.get_base_power_consumption() + device.get_base_power_consumption() * self.random.uniform(0.3,
                                                                                                                    0.5))
            elif self.random.random() <= 0.1:
                device.set_base_power_consumption(
                    device.get_base_power_consumption() - device.get_base_power_consumption() * self.random.uniform(0.3,
                                                                                                                    0.5))

    def reduceBatteryTick(self):
        for device in self.poweredOnDevices:
            if device.get_current_battery_capacity() > 0 and device.is_on_battery_power():  # Corrected condition
                toLog = self.reduceBatteryLevel(device)
                if device.get_battery_level() < 20:
                    self.addBatteryLog(
                        logging.WARNING, f"Battery level of {device.get_device_name()} is below 20 percent!"
                    )
                elif device.get_battery_level() < 10:
                    self.addBatteryLog(
                        logging.CRITICAL, f"Battery level of {device.get_device_name()} is below 10 percent!"
                    )
                elif not toLog:
                    self.addBatteryLog(
                        logging.INFO, f"Battery level of {device.get_device_name()} is now {device.get_battery_level()}"
                    )

                if device.get_battery_level() <= 0:
                    self.addBatteryLog(
                        logging.ERROR, f"Battery of {device.get_device_name()} has run out! Plug it in!"
                    )
                    self.turnOffDevice(device)

    def reduceBatteryLevel(self, device: Device) -> bool:

        currentBattery = int(device.get_battery_level())
        device.set_current_battery_capacity(
            device.get_current_battery_capacity() - device.get_base_power_consumption() * device.get_power_level())
        device.set_battery_level(int(device.get_current_battery_capacity() / device.get_battery_capacity() * 100))
        return int(device.get_battery_level()) == currentBattery

    # ========================================================================
    # Rule Management
    # ========================================================================

    # ========================================================================
    # Location and Temperature Management
    # ========================================================================

    def addLocation(self, location: str):

        if location in self.locationMap:
            self.addLog(
                logging.WARNING, f"Location already exists, user tried to add {location} again"
            )
            return
        self.locationMap[location] = DeviceLocation(location)

    def checkEachDevice(self):
        pass

    def checkEachLocation(self):

        for location in self.locationMap.values():
            # if (simulate) {
            # double randomDouble = random.nextDouble();
            # if (randomDouble >= 0.9) {
            # System.out.println("Adding person to " + location);
            # addPerson(location);
            # } else if (randomDouble <= 0.1) {
            # System.out.println("Removing person from " + location);
            # if (location.getPeople() > 0) removePerson(location);
            # }
            # }
            if location.temperature > 40:
                self.addLog(logging.CRITICAL, f"Temperature in {location} is above 40 degrees!")
            elif location.temperature > 35:
                self.addLog(logging.WARNING, f"Temperature in {location} is above 35 degrees!")
            elif location.temperature < 15:
                self.addLog(logging.WARNING, f"Temperature in {location} is below 15 degrees!")
            elif location.temperature < 10:
                self.addLog(logging.CRITICAL, f"Temperature in {location} is below 10 degrees!")

            # if (location.temperature != ideal_temp) {
            # Device airConditioner = location.getDeviceByName("AirConditioner");
            # if (airConditioner != null) {
            # addRule(parseRule("turn " + airConditioner.getDeviceID() + " on"));
            # addRule(parseRule("set " + airConditioner.getDeviceID() + "1"));
            # }
            # }

    # def tempCheck(self, airConditioner: AirConditioner, location: DeviceLocation):

    #     pass

    # ========================================================================
    # Device State Checks and Simulations
    # ========================================================================

    # def checkEachDevice(self):

    #         for device in self.poweredOnDevices:
    #             if device.basePowerConsumption > 100:
    #                 self.addLog(
    #                     logging.SEVERE, f"Power consumption of {device.deviceName} is above 100W!"
    #                 )
    #             elif device.basePowerConsumption > 50:
    #                 self.addLog(
    #                     logging.WARNING, f"Power consumption of {device.deviceName} is above 50W!"
    #                 )
    #             elif device.basePowerConsumption < 10:
    #                 self.addLog(
    #                     logging.INFO, f"Power consumption of {device.deviceName} is below 10W!"
    #                 )

    def simulateDeviceChange(self):

        toTurnOff = []
        toTurnOn = []

        for device in self.poweredOnDevices:
            if not isinstance(device, Device):
                continue
            randomDouble = self.random.random()
            if randomDouble >= 0.6:
                toTurnOff.append(device)

            elif device.get_power_level() != 0:
                device.get_power_level() = self.random.randint(1, 6)

        for device in self.poweredOffDevices:
            if not isinstance(device, Device):
                continue

            if self.random.random() >= 0.6:
                toTurnOn.append(device)

        for device in toTurnOff:
            self.turnOffDevice(device)
        for device in toTurnOn:
            self.turnOnDevice(device)

    def accidentallyturnedoncheck(self):

        pass

    def roommemberscheck(self):

        pass

    def changeMode(self):
        pass

    # ========================================================================
    # Utility and Helper Methods
    # ========================================================================

    def isNumeric(self, str: str) -> bool:

        try:
            float(str)
            return True
        except ValueError:
            return False

    def getDevicesByGroup(self, groupName: str) -> list[Device]:

        return self.groupMap[groupName].devices

    def getDeviceGroups(self) -> dict[str, DeviceGroup]:

        return self.groupMap

    def getDeviceTypes(self) -> dict[str, DeviceType]:

        return self.typeMap

    def getDeviceLocations(self) -> dict[str, DeviceLocation]:

        return self.locationMap

    def getDevicesByType(self, typeName: str) -> list[Device]:

        return self.typeMap[typeName].devices

    def getDevicesByLocation(self, locationName: str) -> list[Device]:

        return self.locationMap[locationName].devices

    def checkTokenForDevice(self, token: str) -> Device:

        if self.isNumeric(token):
            device = self.getDevice(int(token))
        else:
            device = self.getDevice(token)

        if device is None:
            raise RuleParsingException("Device not found")
        return device

    def checkTokenSize(self, tokens: list[str], size: int):

        if len(tokens) != size:
            raise RuleParsingException("Invalid number of arguments for curr_rule")

    def checkTokenOnOff(self, token: str) -> bool:

        if token.lower() == "on":
            return True
        if token.lower() == "off":
            return False
        raise RuleParsingException("Invalid on/off token")

    def setThreshold(self, threshold: float):

        self.threshold = threshold

    def setIdealTemp(self, idealTemp: int):

        self.idealTemp = idealTemp

    def setSimulate(self, simulate: bool):

        self.simulate = simulate

    def getThreshold(self) -> float:

        return self.threshold

    def getIdealTemp(self) -> int:

        return self.idealTemp

    def isSimulate(self) -> bool:

        return self.simulate

    def getPoweredOnDevices(self) -> list[Device]:

        return self.poweredOnDevices

    def getPoweredOffDevices(self) -> list[Device]:

        return self.poweredOffDevices

    def getDevices(self) -> list[Device]:

        devices = []
        devices.extend(self.poweredOnDevices)
        devices.extend(self.poweredOffDevices)
        return devices

    def getLocation(self, location: str) -> DeviceLocation:

        return self.locationMap[location]

    def getGroup(self, group: str) -> DeviceGroup:

        return self.groupMap[group]

    def getType(self, type: str) -> DeviceType:

        return self.typeMap[type]

    def getPowerConsumptionTasks(self) -> list[str]:

        return self.powerConsumptionTasks

    def getDeviceBatteryTasks(self) -> list[str]:

        return self.deviceBatteryTasks

    def getInfoTasks(self) -> list[str]:

        return self.infoTasks

    def getWarningTasks(self) -> list[str]:

        return self.warningTasks

    def getSevereTasks(self) -> list[str]:

        return self.severeTasks

    def clearInfoTasks(self):

        self.infoTasks.clear()

    def clearWarningTasks(self):

        self.warningTasks.clear()

    def clearSevereTasks(self):

        self.severeTasks.clear()

    def clearPowerConsumptionTasks(self):

        self.powerConsumptionTasks.clear()

    def clearDeviceBatteryTasks(self):

        self.deviceBatteryTasks.clear()

    def getDeviceBatteryLogList(self) -> LinkedList:

        return self.deviceBatteryLogList

    def getPowerConsumptionLogList(self) -> LinkedList:

        return self.powerConsumptionLogList

    def getLoggingList(self) -> LinkedList:

        return self.loggingList

    def getRuleList(self) -> LinkedList:

        return self.ruleList

    def clearDeviceBatteryLogList(self):

        self.deviceBatteryLogList.clear()

    def getDeviceQueue(self) -> PriorityQueue:

        return self.deviceQueue

    def getPowerReducibleDevices(self) -> PriorityQueue:

        return self.powerReducibleDevices

    def getTurnBackOnDevices(self) -> PriorityQueue:

        return self.turnBackOnDevices

    # ========================================================================
    #Testing
    # ========================================================================


import json


def deep_inspect(obj):
    try:
        return json.dumps(obj, indent=4, default=str)
    except TypeError:
        return str(obj)


testHome = SmartHome(10, 25, True)
print(deep_inspect(testHome.getDeviceGroups()))
import inspect


def full_inspect(obj):
    for name, data in inspect.getmembers(obj):
        if not name.startswith("__"):
            print(f"{name}: {data}")


full_inspect(testHome)

testHome.addDevice(
    testHome.createDevice("Lamp", DeviceTypeEnum.DECORATIVE, DeviceGroupEnum.LIGHTS, DeviceLocationEnum.LIVINGROOM,
                          True, 100, 1, 100, 1))
testHome.addDevice(
    testHome.createDevice("Fan", DeviceTypeEnum.DECORATIVE, DeviceGroupEnum.LIGHTS, DeviceLocationEnum.LIVINGROOM, True,
                          100, 2, 100, 1))
testHome.addDevice(
    testHome.createDevice("AC", DeviceTypeEnum.DECORATIVE, DeviceGroupEnum.LIGHTS, DeviceLocationEnum.LIVINGROOM, True,
                          100, 3, 100, 1))

#%% md
# ## User Interface
# 
# The user interface provides a user-friendly way to interact with the smart home system:
# 
# *   **User-Friendly Access:**  A visual interface for easy interaction.
# *   **Device Status Display:** Shows the real-time status of devices (on/off, power level, battery level).
# *   **Device Control:** Allows users to manually control devices (e.g., toggle on/off).
# *   **Log Monitoring:** 
#%%

#%% md
# ## Bugs & Future Plans
# 
# ### Project Timeline
# 
# *   **Week 1:** Implement curr_rule execution and test code
# *   **Week 2:** Connect with frontend using Flask
# *   **Week 3:** Identify and fix any bugs
# 
# 
# ### Known Bugs
# 
# *   **Device Removal:** Occasionally, device removal might be off by one element.
# *   **Improper Logging** Logger logs much more than needed
# *   **Sorting and Reversing:** Optimize the efficiency of sorting and reversing operations (presumably within the `LinkedList` or `Priority Queue`).
#%%
