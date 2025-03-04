from enum import Enum
from main.devices.device import Device

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
