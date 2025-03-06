from ..enums import Devicelocation
from ..enums import DeviceGroup
from ..devices import device
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

    def add_device(self, device: device.Device):
        self.devices.append(device)

    def remove_device(self, device: device.Device):
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
    