from enum import Enum
from main.devices.device import Device

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
