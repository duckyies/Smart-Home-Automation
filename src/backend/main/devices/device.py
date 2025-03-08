from datetime import datetime
import time

class Device:
    def __init__(self, device_id, device_name, device_type, location, device_group, battery_level, max_battery_capacity, current_battery_capacity, is_on_battery, is_turned_on, base_power_consumption, power_level, turned_on_time, is_interacted):
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

    def get_device_type(self) -> str:
        return self.__device_type

    def set_device_type(self, type_: str):
        self.__device_type = type_

    def get_location(self) -> str:
        return self.__location

    def set_location(self, location: str):
        self.__location = location

    def get_device_group(self) -> str:
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
