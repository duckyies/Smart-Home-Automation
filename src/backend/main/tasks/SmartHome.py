from ..datastructures import linkedlist, priorityqueue
from ..devices import AirConditioner, Device
from ..enums import DeviceGroup, Devicelocation, DeviceType
from ..misc import RuleParsingException
from ..tasks import LogTask, Rule

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

        self.groupMap = {}
        self.typeMap = {}
        self.locationMap = {}

        self.poweredOnDevices = []
        self.poweredOffDevices = []

        self.deviceQueue = priorityqueue.PriorityQueue()
        self.powerReducibleDevices = priorityqueue.PriorityQueue()
        self.turnBackOnDevices = priorityqueue.PriorityQueue()

        self.loggingList = linkedlist.LinkedList()
        self.powerConsumptionLogList = linkedlist.LinkedList()
        self.deviceBatteryLogList = linkedlist.LinkedList()

        self.ruleList = linkedlist.LinkedList()

        self.infoTasks = []
        self.warningTasks = []
        self.severeTasks = []
        self.powerConsumptionTasks = []
        self.deviceBatteryTasks = []

        # Logger setup
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.powerConsumptionlogger = logging.getLogger("PowerConsumptionLog")
        self.logger = logging.getLogger(__name__)
        self.deviceBatteryLogger = logging.getLogger("DeviceBatteryLog")

        self._initialize()

        self.scheduler = ThreadPoolExecutor(max_workers=3)
        self.startTick()
        self.logger.info("Tick started")
        self.initializeLogger()
        self.startLogging()
        self.logger.info("Logging started")
        self.startRuleExecution()

    def _initialize(self):

        for deviceGroup in DeviceGroup.DeviceGroupEnum:
            self.groupMap[deviceGroup.name] = DeviceGroup.DeviceGroup(deviceGroup.name)

        for deviceType in DeviceType.DeviceTypeEnum:
            self.typeMap[deviceType.name] = DeviceType.DeviceType(deviceType.name)

        for location in Devicelocation.DeviceLocationEnum:
            devLocation = Devicelocation.DeviceLocation(location.name)
            self.locationMap[location.name] = devLocation
            devLocation.temperature = self.random.randint(10, 45)

    # ========================================================================
    # Device Management
    # ========================================================================

    def _addToGroupAndType(self, device: Device):

        self.groupMap[device.device_group.name].add_device(device)
        self.typeMap[device.device_type.name].add_device(device)
        self.locationMap[device.location.name].add_device(device)

    def createDevice(
        self,
        deviceName: str,
        deviceType: DeviceType.DeviceTypeEnum,
        deviceGroup: DeviceGroup.DeviceGroupEnum,
        location: Devicelocation.DeviceLocationEnum,
        isTurnedOn: bool = False,
        batteryLevel: float = 0.0,
        powerConsumption: float = 0.0,
        maxBatteryCapacity: int = 0,
        powerLevel: int = 1,
    ) -> Device:

        if deviceGroup.name.lower() == "airconditioners":
            return AirConditioner.AirConditioner(
                deviceName,
                deviceType,
                deviceGroup,
                location,
                isTurnedOn,
                batteryLevel,
                powerConsumption,
                maxBatteryCapacity,
                powerLevel,
                True,
            )
        return Device.Device(
            deviceName,
            deviceType,
            deviceGroup,
            location,
            isTurnedOn,
            batteryLevel,
            powerConsumption,
            maxBatteryCapacity,
            powerLevel,
        )

    def addDevice(self, device: Device):

        if (
            device.device_group.name.lower() == "airconditioners".lower()
            and not isinstance(device, AirConditioner.AirConditioner)
        ):
            device = AirConditioner.AirConditioner(
                device.deviceName,
                device.device_type,
                device.device_group,
                device.location,
                device.isTurnedOn,
                device.batteryLevel,
                device.basePowerConsumption,
                int(device.maxBatteryCapacity),
                device.powerLevel,
                True,
            )

        if device.isTurnedOn:
            self.poweredOnDevices.append(device)
            device.turnedOnTime = time.time()

            if device.device_type.priority == float("inf"):
                return
            location = self.locationMap[device.location.name]

            self.deviceQueue.enqueue(
                    priorityqueue.Task(
                    device,
                    device.device_type.priority
                    + device.device_group.priority
                    + (location.people * 10),
                )
            )

            if device.powerLevel != 0:
                if device.device_type.priority == float("inf"):
                    return
                location = self.locationMap[device.location.name]

                self.powerReducibleDevices.enqueue(
                    priorityqueue.Task(
                        device,
                        device.device_type.priority
                        + device.device_group.priority
                        + (location.people * 10),
                    )
                )
        else:
            self.poweredOffDevices.append(device)
        self._addToGroupAndType(device)

    def turnOnDevice(self, device: Device):

        device.isTurnedOn = True

        if device not in self.poweredOnDevices:
            self.poweredOnDevices.append(device)
            device.turnedOnTime = time.time()

        if device in self.poweredOffDevices:
            self.poweredOffDevices.remove(device)
        if device.device_type.priority == float("inf"):
            return
        location = self.locationMap[device.location.name]

        self.deviceQueue.enqueue(
            priorityqueue.Task(
                device,
                device.device_type.priority
                + device.device_group.priority
                + (location.people * 10),
            )
        )
        if device.powerLevel != 0:
            if device.device_type.priority == float("inf"):
                return
            location = self.locationMap[device.location.name]

        self.powerReducibleDevices.enqueue(
            priorityqueue.Task(
                device,
                device.device_type.priority
                + device.device_group.priority
                + (location.people * 10),
            )
        )

    def turnOffDevice(self, device: Device):

        device.isTurnedOn = False

        if device not in self.poweredOffDevices:
            self.poweredOffDevices.append(device)

        if device in self.poweredOnDevices:
            self.poweredOnDevices.remove(device)
        self.deviceQueue.remove_task(device)
        self.powerReducibleDevices.remove_task(device)

    def removeDevice(self, device: Device):

        if device in self.poweredOnDevices:
            self.poweredOnDevices.remove(device)
        if device in self.poweredOffDevices:
            self.poweredOffDevices.remove(device)
        self.groupMap[device.device_group.name].remove_device(device)
        self.typeMap[device.device_type.name].remove_device(device)
        self.locationMap[device.location.name].remove_device(device)

    def getDeviceByName(self, name: str) -> Device.Device | None:

        for device in self.poweredOnDevices:
            if device.deviceName.lower() == name.lower():
                return device
        for device in self.poweredOffDevices:
            if device.deviceName.lower() == name.lower():
                return device
        return None

    def getDeviceByID(self, deviceId: int) -> Device.Device | None:

        for device in self.poweredOnDevices:
            if device.deviceId == deviceId:
                return device
        for device in self.poweredOffDevices:
            if device.deviceId == deviceId:
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

    def getDevice(self, identifier: str | int) -> Device.Device | None:

        if isinstance(identifier, int):
            return self.getDeviceByID(identifier)
        elif isinstance(identifier, str):
            return self.getDeviceByName(identifier)
        else:
            return None

    def addPerson(self, location: Devicelocation.DeviceLocationEnum):

        if isinstance(location, Devicelocation.DeviceLocationEnum):
            locationObj = self.locationMap[location.name]
        else:
            locationObj = location

        locationObj.add_people(1)
        for device in locationObj.devices:
            if device.isTurnedOn:
                task = self.deviceQueue.get_task(device)
                self.deviceQueue.update_priority(task, task.priority + 10)

    def removePerson(self, location: Devicelocation.DeviceLocationEnum):

        if isinstance(location, Devicelocation.DeviceLocationEnum):
            locationObj = self.locationMap[location.name]
        else:
            locationObj = location

        if locationObj.people == 0:
            return

        locationObj.remove_people(1)

        for device in locationObj.devices:
            if device.isTurnedOn:
                task = self.deviceQueue.get_task(device)
                self.deviceQueue.update_priority(task, task.priority - 10)

    # ========================================================================
    # Tick and Scheduling
    # ========================================================================

    def initializeScheduler(self):

        self.scheduler = ThreadPoolExecutor(max_workers=3)
        self.startTick()
        self.logger.info("Tick started")
        self.initializeLogger()
        self.startLogging()
        self.logger.info("Logging started")
        self.startRuleExecution()

    def startTick(self):

        self.scheduler.submit(self._runTickPeriodically)

    def _runTickPeriodically(self):

        while True:
            start_time = time.time()
            self.tick()
            end_time = time.time()
            execution_time = end_time - start_time
            sleep_time = max(0, 1 - execution_time)
            time.sleep(sleep_time)

    def stopTick(self):

        self.scheduler.shutdown(wait=False)

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
            if reducePowerTask is None:
                self.logger.info("No devices to reduce power consumption")
                return
            device = reducePowerTask.task

            if (
                currPowerConsumption
                - (device.basePowerConsumption * (device.powerLevel - 1))
                > self.threshold
            ):
                self.powerReducibleDevices.enqueue(reducePowerTask)
                removeTask = self.deviceQueue.dequeue()
                if removeTask is None:
                    self.logger.info("No devices to turn off")
                    return
                removeDevice = removeTask.task

                self.logger.info(
                    f"Reducing power consumption by turning off {device.deviceName}"
                )

                # add rule
                # self.addRule(self.parseRule(f"turn {removeDevice.deviceId} off"))
                self.turnOffDevice(removeDevice)
                self.turnBackOnDevices.enqueue(
                    priorityqueue.Task(device, -removeTask.priority)
                )
            else:
                # add rule
                # self.addRule(self.parseRule(f"set {device.deviceId} 1"))
                device.powerLevel = 1
        else:
            turnBackOnTask = self.turnBackOnDevices.dequeue()
            if turnBackOnTask is not None:
                turnBackOnDevice = turnBackOnTask.task
                if (
                    currPowerConsumption
                    + (
                        turnBackOnDevice.basePowerConsumption
                        * turnBackOnDevice.powerLevel
                    )
                    > self.threshold
                ):
                    self.logger.info(
                        f"Not turning back on {turnBackOnTask.task.deviceName}"
                    )
                    turnBackOnTask.priority = turnBackOnTask.priority + 3
                    self.turnBackOnDevices.enqueue(turnBackOnTask)
                    return
                self.logger.info(
                    f"Turning back on {turnBackOnTask.task.deviceName}"
                )
                # add rule
                # self.addRule(
                #    self.parseRule(f"turn {turnBackOnTask.task.deviceId} on")
                # )
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

        try:
            self.scheduler.submit(self._runExecuteRulesPeriodically)
        except Exception as e:
            self.logger.error(f"Error during rule execution: {e}")
            self.logger.exception(e)

    def _runExecuteRulesPeriodically(self):

        while True:
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

    # ========================================================================
    # Logging
    # ========================================================================

    def initializeLogger(self):

        self.powerConsumptionlogger = logging.getLogger("PowerConsumptionLog")
        self.logger = logging.getLogger(__name__)
        self.deviceBatteryLogger = logging.getLogger("DeviceBatteryLog")

        infoFileHandler = None
        warningFileHandler = None
        severeFileHandler = None
        powerConsumptionFileHandler = None
        deviceBatteryFileHandler = None

        try:
            self.powerConsumptionlogger.setLevel(logging.ALL)
            powerConsumptionFileHandler = logging.FileHandler("PowerConsumption.log")
            powerConsumptionFileHandler.setLevel(logging.ALL)
            powerConsumptionFileHandler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))

            infoFileHandler = logging.FileHandler("Info.log")
            infoFileHandler.setLevel(logging.INFO)
            infoFileHandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            infoFileHandler.addFilter(lambda record: record.levelno == logging.INFO)

            warningFileHandler = logging.FileHandler("Warning.log")
            warningFileHandler.setLevel(logging.WARNING)
            warningFileHandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            warningFileHandler.addFilter(lambda record: record.levelno == logging.WARNING)

            severeFileHandler = logging.FileHandler("Severe.log")
            severeFileHandler.setLevel(logging.SEVERE)
            severeFileHandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            severeFileHandler.addFilter(lambda record: record.levelno == logging.SEVERE)

            self.deviceBatteryLogger.setLevel(logging.ALL)
            deviceBatteryFileHandler = logging.FileHandler("DeviceBattery.log")
            deviceBatteryFileHandler.setLevel(logging.ALL)
            deviceBatteryFileHandler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))

            self.logger.addHandler(infoFileHandler)
            self.logger.addHandler(warningFileHandler)
            self.logger.addHandler(severeFileHandler)
            self.powerConsumptionlogger.addHandler(powerConsumptionFileHandler)
            self.powerConsumptionlogger.propagate = False  # Using propagate instead of setUseParentHandlers
            self.logger.propagate = False
            self.deviceBatteryLogger.addHandler(deviceBatteryFileHandler)
            self.deviceBatteryLogger.propagate = False

        except Exception as e:
            print(e)

    def startLogging(self):

        self.logger.info("Logging started")
        try:
            self.scheduler.submit(self._runLogPeriodically)
        except Exception as e:
            self.logger.error(f"Error during logging: {e}")
            self.logger.exception(e)

    def _runLogPeriodically(self):

        while True:
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

        elif logLevel == logging.SEVERE:
            self.severeTasks.append(message)
        self.loggingList.addEnd(LogTask.LogTask(logLevel, message))

    def addPowerLog(self, logLevel, message):

        self.powerConsumptionLogList.addEnd(LogTask.LogTask(logLevel, message))
        self.powerConsumptionTasks.append(message)
        if logLevel != logging.INFO:
            self.addLog(logLevel, message)

    def addBatteryLog(self, logLevel, message):

        self.deviceBatteryLogList.addEnd(LogTask.LogTask(logLevel, message))
        self.deviceBatteryTasks.append(message)
        if logLevel != logging.INFO:
            self.addLog(logLevel, message)

    # ========================================================================
    # Power Management
    # ========================================================================

    def calculateCurrentBasePowerConsumption(self) -> float:

        return sum(device.basePowerConsumption for device in self.poweredOnDevices)

    def calculateCurrentPowerConsumption(self) -> float:

        return sum(
            device.basePowerConsumption * (device.powerLevel if device.powerLevel > 0 else 1)
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
                device.basePowerConsumption += device.basePowerConsumption * self.random.uniform(0.3, 0.5)
            elif self.random.random() <= 0.1:
                device.basePowerConsumption -= device.basePowerConsumption * self.random.uniform(0.3, 0.5)

    def reduceBatteryTick(self):

        for device in self.poweredOnDevices:
            # ikr ui is sooo dumb :3
            if device.maxBatteryCapacity > 0 and device.currentBatteryCapacity == 0:
                device.currentBatteryCapacity = device.batteryCapacity
                device.onBattery = True

            if device.onBattery:
                toLog = self.reduceBatteryLevel(device)
                if device.batteryLevel < 20:
                    self.addBatteryLog(
                        logging.WARNING, f"Battery level of {device.deviceName} is below 20 percent!"
                    )
                elif device.batteryLevel < 10:
                    self.addBatteryLog(
                        logging.SEVERE, f"Battery level of {device.deviceName} is below 10 percent!" 
                    )
                elif not toLog:
                    self.addBatteryLog(
                        logging.INFO, f"Battery level of {device.deviceName} is now {device.batteryLevel}"
                    )

                if device.batteryLevel <= 0:
                    self.addBatteryLog(
                        logging.ERROR, f"Battery of {device.deviceName} has run out! Plug it in!"
                    )
                    self.turnOffDevice(device)

    def reduceBatteryLevel(self, device: Device) -> bool:

        currentBattery = int(device.batteryLevel)
        device.currentBatteryCapacity -= device.basePowerConsumption * device.powerLevel
        device.batteryLevel = int(device.currentBatteryCapacity / device.maxBatteryCapacity * 100)
        return int(device.batteryLevel) == currentBattery

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
        self.locationMap[location] = Devicelocation.DeviceLocation(location)

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
                self.addLog(logging.SEVERE, f"Temperature in {location} is above 40 degrees!")
            elif location.temperature > 35:
                self.addLog(logging.WARNING, f"Temperature in {location} is above 35 degrees!")
            elif location.temperature < 15:
                self.addLog(logging.WARNING, f"Temperature in {location} is below 15 degrees!")
            elif location.temperature < 10:
                self.addLog(logging.SEVERE, f"Temperature in {location} is below 10 degrees!")


            # if (location.temperature != idealTemp) {
            # Device airConditioner = location.getDeviceByName("AirConditioner");
            # if (airConditioner != null) {
            # addRule(parseRule("turn " + airConditioner.getDeviceID() + " on"));
            # addRule(parseRule("set " + airConditioner.getDeviceID() + "1"));
            # }
            # }

    def tempCheck(self, airConditioner: AirConditioner, location: Devicelocation):

        pass

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

            elif device.powerLevel != 0:
                device.powerLevel = self.random.randint(1, 6)

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

    def getDevicesByGroup(self, groupName: str) -> list[Device.Device]:

        return self.groupMap[groupName].devices

    def getDeviceGroups(self) -> dict[str, DeviceGroup.DeviceGroup]:

        return self.groupMap

    def getDeviceTypes(self) -> dict[str, DeviceType.DeviceType]:

        return self.typeMap

    def getDeviceLocations(self) -> dict[str, Devicelocation.DeviceLocation]:

        return self.locationMap

    def getDevicesByType(self, typeName: str) -> list[Device.Device]:

        return self.typeMap[typeName].devices

    def getDevicesByLocation(self, locationName: str) -> list[Device.Device]:

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
            raise RuleParsingException("Invalid number of arguments for rule")

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

    def getPoweredOnDevices(self) -> list[Device.Device]:

        return self.poweredOnDevices

    def getPoweredOffDevices(self) -> list[Device.Device]:

        return self.poweredOffDevices

    def getDevices(self) -> list[Device.Device]:

        devices = []
        devices.extend(self.poweredOnDevices)
        devices.extend(self.poweredOffDevices)
        return devices

    def getLocation(self, location: str) -> Devicelocation:

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

    def getDeviceBatteryLogList(self) -> linkedlist.LinkedList:

        return self.deviceBatteryLogList

    def getPowerConsumptionLogList(self) -> linkedlist.LinkedList:

        return self.powerConsumptionLogList

    def getLoggingList(self) -> linkedlist.LinkedList:

        return self.loggingList

    def getRuleList(self) -> linkedlist.LinkedList:

        return self.ruleList

    def clearDeviceBatteryLogList(self):

        self.deviceBatteryLogList.clear()

    def getDeviceQueue(self) -> priorityqueue.PriorityQueue:

        return self.deviceQueue

    def getPowerReducibleDevices(self) -> priorityqueue.PriorityQueue:

        return self.powerReducibleDevices

    def getTurnBackOnDevices(self) -> priorityqueue.PriorityQueue:

        return self.turnBackOnDevices
    

    # ========================================================================
    #Testing
    # ========================================================================

