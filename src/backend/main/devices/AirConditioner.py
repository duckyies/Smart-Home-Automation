import Device
import time

class AirConditioner(Device):
    def __init__(self, device_name, device_type, device_group, location, is_turned_on, battery_level, power_consumption, max_battery_capacity, power_level, mode):
        super().__init__(device_name, device_type, device_group, location, is_turned_on, battery_level, power_consumption, max_battery_capacity, power_level)
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





