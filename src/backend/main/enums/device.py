from datetime import datetime
from pydantic import BaseModel
import time

class Device(BaseModel):
    device_id: int
    device_name: str
    device_type: str
    location: str
    device_group: str
    battery_level: float = 100.0 
    max_battery_capacity: int = 100
    current_battery_capacity: float = 100.0
    is_on_battery: bool = False
    is_turned_on: bool = False
    base_power_consumption: float = 0.0
    power_level: int = 0
    turned_on_time: int = 0
    is_interacted: bool = False

    def flip_interaction_state(self):
        self.is_interacted = not self.is_interacted

    def get_minutes_since_turned_on(self):
        if self.turned_on_time:
            return int((int(time.time()) - self.turned_on_time) // 60)
        return 0

    def set_turned_on(self, status: bool):
        self.is_turned_on = status

    def set_battery_level(self, level: float):
        self.battery_level = level

    def set_base_power_consumption(self, consumption: float):
        self.base_power_consumption = consumption

    def set_battery_capacity(self, capacity: int):
        self.max_battery_capacity = capacity

    def get_battery_capacity(self) -> int:
        return self.max_battery_capacity

    def get_device_id(self) -> int:
        return self.device_id

    def get_device_name(self) -> str:
        return self.device_name

    def set_device_name(self, name: str):
        self.device_name = name

    def get_device_type(self) -> str:
        return self.device_type

    def set_device_type(self, type_: str):
        self.device_type = type_

    def get_location(self) -> str:
        return self.location

    def set_location(self, location: str):
        self.location = location

    def get_device_group(self) -> str:
        return self.device_group

    def set_device_group(self, group: str):
        self.device_group = group

    def get_power_level(self) -> int:
        return self.power_level

    def set_power_level(self, level: int):
        self.power_level = level

    def is_on_battery_power(self) -> bool:
        return self.is_on_battery

    def set_on_battery(self, status: bool):
        self.is_on_battery = status

    def get_current_battery_capacity(self) -> float:
        return self.current_battery_capacity

    def set_current_battery_capacity(self, capacity: float):
        self.current_battery_capacity = capacity

    def set_turned_on_time(self, time: int):
        self.turned_on_time = time

    def get_turned_on_time(self) -> int:
        return self.turned_on_time

    def __str__(self):
        return (f"Device ID: {self.device_id}\n"
                f"Device Name: {self.device_name}\n"
                f"Device Type: {self.device_type}\n"
                f"Device Group: {self.device_group}\n"
                f"Location: {self.location}\n"
                f"Power Status: {'On' if self.is_turned_on else 'Off'}\n"
                f"Battery Level: {self.battery_level}\n"
                f"Power Consumption: {self.base_power_consumption} W\n"
                f"Power Level: {self.power_level}\n")
    


#Test cases

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


print(f"Battery Level after update: {device1.get_current_battery_capacity()}")
print(f"Power Level after update: {device1.get_power_level()}")
print(f"Interaction State: {device1.is_interacted}")
print(f"Minutes since turned on: {device1.get_minutes_since_turned_on()} min")
