from ..datastructures import linkedlist
from ..datastructures import priorityqueue
from ..enums import DeviceGroup
from ..enums import Devicelocation
from ..devices import device

import logging
import enum
import time
import random
import threading



class SmartHome:

    groupMap = {}
    typeMap = {}
    locationMap = {}
    poweredOnDevices = []
    poweredOffDevices = []
    infoTasks = []
    warningTasks = []
    severeTasks = []
    powerConsumptionTasks = []
    deviceBatteryTasks = []

    def __init__(self, threshold: int, idealTemp: int, simulate: bool):
        self.threshold = threshold
        self.idealTemp = idealTemp
        self.simulate = simulate
        self.powerConsumption = 1
        self.mode = "Normal"
        self.date = time.time()
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)


