from ..datastructures import linkedlist, priorityqueue
from ..devices import AirConditioner, Device
from ..enums import DeviceGroup, Devicelocation, DeviceType
# from ..misc import RuleParsingException
# from ..tasks import LogTask, Rule, Task


import logging
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor




class SmartHome:

    def __init__(self, threshold: float, ideal_temp: int, simulate: bool):

        self.tick_count = 0
        self.threshold = threshold
        self.ideal_temp = ideal_temp
        self.simulate = simulate
        self.power_consumption = 1.0
        self.mode = "Normal"
        self.date = time.time()  
        self.lock = threading.Lock()
        self.random = random.Random()

        self.group_map = {} 
        self.type_map = {} 
        self.location_map = {}  

        self.powered_on_devices = []  
        self.powered_off_devices = [] 

        self.device_queue = priorityqueue()
        self.power_reducible_devices = priorityqueue()  
        self.turn_back_on_devices = priorityqueue()

        self.logging_list = linkedlist()
        self.power_consumption_log_list = linkedlist()
        self.device_battery_log_list = linkedlist()


        self.rule_list = linkedlist() 


        self.info_tasks = []
        self.warning_tasks = []
        self.severe_tasks = []
        self.power_consumption_tasks = [] 
        self.device_battery_tasks = []

        # Logger setup
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)
        self.power_consumption_logger = logging.getLogger("power_consumption")
        self.device_battery_logger = logging.getLogger("device_battery")

        self._initialize()

        self.scheduler = ThreadPoolExecutor(max_workers=3)
        self.start_tick()
        self.logger.info("Tick started")
        self.initialize_logger()
        self.start_logging()
        self.logger.info("Logging started")
        # self.start_rule_execution()   to be fixedddd


    def _initialize(self):

        for device_group in DeviceGroup.DeviceGroupEnum:
            self.group_map[device_group.name] = DeviceGroup.DeviceGroup(device_group.name)

        for device_type in DeviceType.DeviceTypeEnum:
            self.type_map[device_type.name] = DeviceType.DeviceType(device_type.name)

        for location in Devicelocation.DeviceLocationEnum:
            dev_location = Devicelocation.DeviceLocation(location.name)
            self.location_map[location.name] = dev_location
            dev_location.temperature = self.random.randint(10, 45)


    # ========================================================================
    # Device Management
    # ========================================================================

    def _add_to_group_and_type(self, device: Device):

        self.group_map[device.device_group.name].add_device(device)
        self.type_map[device.device_type.name].add_device(device)
        self.location_map[device.location.name].add_device(device)


    def create_device(
        self,
        device_name: str,
        device_type: DeviceType.DeviceTypeEnum,
        device_group: DeviceGroup.DeviceGroupEnum,
        location: Devicelocation.DeviceLocationEnum,
        is_turned_on: bool = False,
        battery_level: float = 0.0,
        power_consumption: float = 0.0,
        max_battery_capacity: int = 0,
        power_level: int = 1,
    ) -> Device:

        # if device_group.name.lower() == "AirConditioner".lower():
        #     return AirConditioner(
        #         device_name,
        #         device_type,
        #         device_group,
        #         location,
        #         is_turned_on,
        #         battery_level,
        #         power_consumption,
        #         max_battery_capacity,
        #         power_level,
        #         True,
        #     )

        return Device(
            device_name,
            device_type,
            device_group,
            location,
            is_turned_on,
            battery_level,
            power_consumption,
            max_battery_capacity,
            power_level,
        )


    def add_device(self, device: Device):
       
        if (
            device.device_group.name.lower() == "AirConditioners".lower()
            and not isinstance(device, AirConditioner)
        ):
            device = AirConditioner(
                device.device_name,
                device.device_type,
                device.device_group,
                device.location,
                device.is_turned_on,
                device.battery_level,
                device.base_power_consumption,
                int(device.max_battery_capacity),
                device.power_level,
                True,
            )

        if device.is_turned_on:
            self.powered_on_devices.append(device)
            device.turned_on_time = time.time()

            if device.device_type.priority == float("inf"):
                return
            location = self.location_map[device.location.name]

            self.device_queue.enqueue(
                Task(
                    device,
                    device.device_type.priority
                    + device.device_group.priority
                    + (location.people * 10),
                )
            )

            if device.power_level != 0:
                if device.device_type.priority == float("inf"):
                    return
                location = self.location_map[device.location.name]

                # self.power_reducible_devices.enqueue(
                #     Task(
                #         device,
                #         device.device_type.priority
                #         + device.device_group.priority
                #         + (location.people * 10),
                #     )
                # )
        else:
            self.powered_off_devices.append(device)
        self._add_to_group_and_type(device)


    def turn_on_device(self, device: Device):
       
        device.is_turned_on = True

        if device not in self.powered_on_devices:
            self.powered_on_devices.append(device)
            device.turned_on_time = time.time()

        if device in self.powered_off_devices:
            self.powered_off_devices.remove(device)
        if device.device_type.priority == float("inf"):
            return
        location = self.location_map[device.location.name]

        # self.device_queue.enqueue(
        #     Task(
        #         device,
        #         device.device_type.priority
        #         + device.device_group.priority
        #         + (location.people * 10),
        #     )
        #)
        if device.power_level != 0:
            if device.device_type.priority == float("inf"):
                return
            location = self.location_map[device.location.name]

            # self.power_reducible_devices.enqueue(
            #     Task(
            #         device,
            #         device.device_type.priority
            #         + device.device_group.priority
            #         + (location.people * 10),
            #     )
            # )


    def turn_off_device(self, device: Device):
        
        device.is_turned_on = False

        if device not in self.powered_off_devices:
            self.powered_off_devices.append(device)

        if device in self.powered_on_devices:
            self.powered_on_devices.remove(device)
        self.device_queue.remove_task(device)
        self.power_reducible_devices.remove_task(device)


    def remove_device(self, device: Device):
    
        if device in self.powered_on_devices:
            self.powered_on_devices.remove(device)
        if device in self.powered_off_devices:
            self.powered_off_devices.remove(device)
        self.group_map[device.device_group.name].remove_device(device)
        self.type_map[device.device_type.name].remove_device(device)
        self.location_map[device.location.name].remove_device(device)


    def get_device_by_name(self, name: str) -> Device | None:
       
        for device in self.powered_on_devices:
            if device.device_name.lower() == name.lower():
                return device
        for device in self.powered_off_devices:
            if device.device_name.lower() == name.lower():
                return device
        return None


    def get_device_by_id(self, device_id: int) -> Device | None:
       
        for device in self.powered_on_devices:
            if device.device_id == device_id:
                return device
        for device in self.powered_off_devices:
            if device.device_id == device_id:
                return device
        return None


    def turn_off_devices_by_group(self, group_name: str):
        
        for device in self.group_map[group_name].devices:
            self.turn_off_device(device)


    def turn_on_devices_by_group(self, group_name: str):
       
        for device in self.group_map[group_name].devices:
            self.turn_on_device(device)


    def turn_off_devices_by_type(self, type_name: str):
       
        for device in self.type_map[type_name].devices:
            self.turn_off_device(device)


    def turn_on_devices_by_type(self, type_name: str):
       
        for device in self.type_map[type_name].devices:
            self.turn_on_device(device)


    def turn_off_devices_by_location(self, location_name: str):
        
        for device in self.location_map[location_name].devices:
            self.turn_off_device(device)


    def turn_on_devices_by_location(self, location_name: str):

        for device in self.location_map[location_name].devices:
            self.turn_on_device(device)


    def turn_off_all_devices(self):

        for device in list(self.powered_on_devices): 
            self.turn_off_device(device)


    def turn_on_all_devices(self):

        for device in list(self.powered_off_devices):
            self.turn_on_device(device)


    def get_device(self, identifier: str | int) -> Device | None:
    
        if isinstance(identifier, int):
            return self.get_device_by_id(identifier)
        elif isinstance(identifier, str):
            return self.get_device_by_name(identifier)
        else:
            return None


    def add_person(self, location: Devicelocation.DeviceLocationEnum ):

        if isinstance(location, Devicelocation.DeviceLocationEnum):
            location_obj = self.location_map[location.name]
        else:
            location_obj = location

        location_obj.add_people(1)
        for device in location_obj.devices:
            if device.is_turned_on:
                task = self.device_queue.get_task(device)
                self.device_queue.update_priority(task, task.priority + 10)


    def remove_person(
        self, location: Devicelocation.DeviceLocationEnum
    ):

        if isinstance(location, Devicelocation.DeviceLocationEnum):
            location_obj = self.location_map[location.name]
        else:
            location_obj = location

        if location_obj.people == 0:
            return

        location_obj.remove_people(1)

        for device in location_obj.devices:
            if device.is_turned_on:
                task = self.device_queue.get_task(device)
                self.device_queue.update_priority(task, task.priority - 10)


    # ========================================================================
    # Tick and Scheduling
    # ========================================================================

    def initialize_scheduler(self):

        self.scheduler = ThreadPoolExecutor(max_workers=3)  # Simulate ScheduledExecutorService
        self.start_tick()
        self.logger.info("Tick started")
        self.initialize_logger()  # Ensure logger is initialized before logging starts
        self.start_logging()
        self.logger.info("Logging started")
        # self.start_rule_execution()  # Rule execution not yet translated


    def start_tick(self):
        self.scheduler.submit(self._run_tick_periodically)


    def _run_tick_periodically(self):

        while True:
            start_time = time.time()
            self.tick()
            end_time = time.time()
            execution_time = end_time - start_time
            sleep_time = max(0, 1 - execution_time)  # Ensure sleep_time is not negative
            time.sleep(sleep_time)


    def stop_tick(self):

        self.scheduler.shutdown(wait=False)


    def tick(self):

        try:
            self.tick_task()
        except Exception as e:
            self.logger.error(f"Error during tick execution: {e}")
            self.logger.exception(e)


    def check_power_consumption(self):

        curr_power_consumption = self.calculate_current_power_consumption()

        if curr_power_consumption > self.threshold:
            reduce_power_task = self.power_reducible_devices.dequeue()
            if reduce_power_task is None:
                self.logger.info("No devices to reduce power consumption")
                return
            device = reduce_power_task.task

            if (
                curr_power_consumption
                - (device.base_power_consumption * (device.power_level - 1))
                > self.threshold
            ):
                self.power_reducible_devices.enqueue(reduce_power_task)
                remove_task = self.device_queue.dequeue()
                if remove_task is None:
                    self.logger.info("No devices to turn off")
                    return
                remove_device = remove_task.task

                self.logger.info(
                    f"Reducing power consumption by turning off {device.device_name}"
                )

                #add rule
                #self.add_rule(self.parse_rule(f"turn {remove_device.device_id} off"))
                self.turn_off_device(remove_device)
                self.turn_back_on_devices.enqueue(
                    Task(device, -remove_task.priority)
                )
            else:
                #add rule
                #self.add_rule(self.parse_rule(f"set {device.device_id} 1"))
                device.power_level = 1
        else:
            turn_back_on_task = self.turn_back_on_devices.dequeue()
            if turn_back_on_task is not None:
                turn_back_on_device = turn_back_on_task.task
                if (
                    curr_power_consumption
                    + (
                        turn_back_on_device.base_power_consumption
                        * turn_back_on_device.power_level
                    )
                    > self.threshold
                ):
                    self.logger.info(
                        f"Not turning back on {turn_back_on_task.task.device_name}"
                    )
                    turn_back_on_task.priority = turn_back_on_task.priority + 3
                    self.turn_back_on_devices.enqueue(turn_back_on_task)
                    return
                self.logger.info(
                    f"Turning back on {turn_back_on_task.task.device_name}"
                )
                #add rule
                #self.add_rule(
                #    self.parse_rule(f"turn {turn_back_on_task.task.device_id} on")
                #)
                self.turn_on_device(turn_back_on_device)



    def tick_task(self):

        self.tick_count += 1
        if self.tick_count % 2 == 0:
            try:
                if self.simulate:
                    #self.simulate_device_change()
                    pass
                #self.realistic_power_consumption()
                pass
            except Exception as e:
                self.logger.error(f"Error during deviceChange execution: {e}")
                self.logger.exception(e)
        try:
            self.log_power_consumption()
            #self.reduce_battery_tick()
            #self.check_each_device()
            #self.check_each_location()
            self.check_power_consumption()
        except Exception as e:
            self.logger.error(f"Error during tickTask execution: {e}")
            self.logger.exception(e)

    # ========================================================================
    # Logging
    # ========================================================================

    def initialize_logger(self):

        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.power_consumption_logger.setLevel(logging.INFO)
        power_handler = logging.FileHandler("power_consumption.log")
        power_formatter = logging.Formatter("%(asctime)s - %(message)s")
        power_handler.setFormatter(power_formatter)
        self.power_consumption_logger.addHandler(power_handler)

        self.device_battery_logger.setLevel(logging.INFO)
        battery_handler = logging.FileHandler("device_battery.log")
        battery_formatter = logging.Formatter("%(asctime)s - %(message)s")
        battery_handler.setFormatter(battery_formatter)
        self.device_battery_logger.addHandler(battery_handler)


    def start_logging(self):

        self.scheduler.submit(self._run_logging_periodically)

    def _run_logging_periodically(self):

        while True:
            start_time = time.time()
            self.log_info_tasks()
            self.log_warning_tasks()
            self.log_severe_tasks()
            self.log_power_consumption()
            self.log_device_battery()
            end_time = time.time()
            execution_time = end_time - start_time
            sleep_time = max(0, 10 - execution_time)  
            time.sleep(sleep_time)


    def log_info_tasks(self):

        for task in self.info_tasks:
            self.logger.info(task)
        self.info_tasks.clear()


    def log_warning_tasks(self):

        for task in self.warning_tasks:
            self.logger.warning(task)
        self.warning_tasks.clear()


    def log_severe_tasks(self):

        for task in self.severe_tasks:
            self.logger.error(task) 
        self.severe_tasks.clear()


    def log_power_consumption(self):

        power_consumption = self.calculate_current_power_consumption()
        self.power_consumption_logger.info(
            f"Current power consumption: {power_consumption}"
        )
        self.power_consumption_tasks.clear()


    def log_device_battery(self):

        for device in self.powered_on_devices:
            self.device_battery_logger.info(
                f"Device {device.device_name} battery level: {device.battery_level}"
            )
        self.device_battery_tasks.clear()


    # ========================================================================
    # Power Consumption
    # ========================================================================

    def calculate_current_power_consumption(self) -> float:
       
        total_consumption = 0.0
        for device in self.powered_on_devices:
            total_consumption += device.base_power_consumption * device.power_level
        return total_consumption


    def initialize_logger(self):

        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


        self.power_consumption_logger.setLevel(logging.INFO)
        power_handler = logging.FileHandler("power_consumption.log")
        power_formatter = logging.Formatter("%(asctime)s - %(message)s")
        power_handler.setFormatter(power_formatter)
        self.power_consumption_logger.addHandler(power_handler)


        self.device_battery_logger.setLevel(logging.INFO)
        battery_handler = logging.FileHandler("device_battery.log")
        battery_formatter = logging.Formatter("%(asctime)s - %(message)s")
        battery_handler.setFormatter(battery_handler)
        self.device_battery_logger.addHandler(battery_handler)