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

    def get_priority(self):
        return self.value


class Device:
    def __init__(self, device_id, device_name):
        self.device_id = device_id
        self.device_name = device_name
        self.turned_on = False

    def set_turned_on(self, state):
        self.turned_on = state

    def get_device_name(self):
        return self.device_name

    def get_device_id(self):
        return self.device_id


class DeviceGroup:
    def __init__(self, group_name):
        self.group_name = group_name
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def remove_device(self, device):
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

    def get_device_by_name(self, name):
        name_lower = name.lower()
        return next((device for device in self.devices if name_lower in device.get_device_name().lower()), None)

    def get_device_by_id(self, device_id):
        return next((device for device in self.devices if device.get_device_id() == device_id), None)

    def get_group_name(self):
        return self.group_name
    


device1 = Device(1, "Smart Light")
device2 = Device(2, "Ceiling Fan")
device3 = Device(3, "Security Alarm")

group = DeviceGroup("Living Room")


group.add_device(device1)
group.add_device(device2)
group.add_device(device3)
print("Devices after adding:", [d.get_device_name() for d in group.get_devices()])


group.remove_device(device2)
print([d.get_device_name() for d in group.get_devices()])

found_device = group.get_device_by_name("smart light")
print("Found device by name:", found_device.get_device_name() if found_device else "Not found")

found_device = group.get_device_by_id(3)
print("Found device by ID 3:", found_device.get_device_name() if found_device else "Not found")

group.turn_on_all_devices()
print("Device states after turning on:", {d.get_device_name(): d.turned_on for d in group.get_devices()})

group.turn_off_all_devices()
print("Device states after turning off:", {d.get_device_name(): d.turned_on for d in group.get_devices()})

print("Priority of lights group:", DeviceGroupEnum.LIGHTS.get_priority())

