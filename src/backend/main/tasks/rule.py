class Rule:
    def __init__(self, deviceId, flipState, turnOn, turnOff, setPowerLevel, powerLevel, groupName, turnGroupOff, turnGroupOn, typeName, turnTypeOff, turnTypeOn, locationName, turnLocationOff, turnLocationOn):
        self.__deviceId = deviceId
        self.__flipState = flipState
        self.__turnOn = turnOn
        self.__turnOff = turnOff
        self.__setPowerLevel = setPowerLevel
        self.__powerLevel = powerLevel
        self.__groupName = groupName
        self.__turnGroupOff = turnGroupOff
        self.__turnGroupOn = turnGroupOn
        self.__typeName = typeName
        self.__turnTypeOff = turnTypeOff
        self.__turnTypeOn = turnTypeOn
        self.__locationName = locationName
        self.__turnLocationOff = turnLocationOff
        self.__turnLocationOn = turnLocationOn

    def get_deviceId(self):
        return self.__deviceId

    def set_deviceId(self, deviceId):
        self.__deviceId = deviceId

    def get_flipState(self):
        return self.__flipState

    def set_flipState(self, flipState):
        self.__flipState = flipState

    def get_turnOn(self):
        return self.__turnOn

    def set_turnOn(self, turnOn):
        self.__turnOn = turnOn

    def get_turnOff(self):
        return self.__turnOff

    def set_turnOff(self, turnOff):
        self.__turnOff = turnOff

    def get_setPowerLevel(self):
        return self.__setPowerLevel

    def set_setPowerLevel(self, setPowerLevel):
        self.__setPowerLevel = setPowerLevel

    def get_powerLevel(self):
        return self.__powerLevel

    def set_powerLevel(self, powerLevel):
        self.__powerLevel = powerLevel

    def get_groupName(self):
        return self.__groupName

    def set_groupName(self, groupName):
        self.__groupName = groupName

    def get_turnGroupOff(self):
        return self.__turnGroupOff

    def set_turnGroupOff(self, turnGroupOff):
        self.__turnGroupOff = turnGroupOff

    def get_turnGroupOn(self):
        return self.__turnGroupOn

    def set_turnGroupOn(self, turnGroupOn):
        self.__turnGroupOn = turnGroupOn

    def get_typeName(self):
        return self.__typeName

    def set_typeName(self, typeName):
        self.__typeName = typeName

    def get_turnTypeOff(self):
        return self.__turnTypeOff

    def set_turnTypeOff(self, turnTypeOff):
        self.__turnTypeOff = turnTypeOff

    def get_turnTypeOn(self):
        return self.__turnTypeOn

    def set_turnTypeOn(self, turnTypeOn):
        self.__turnTypeOn = turnTypeOn

    def get_locationName(self):
        return self.__locationName

    def set_locationName(self, locationName):
        self.__locationName = locationName

    def get_turnLocationOff(self):
        return self.__turnLocationOff

    def set_turnLocationOff(self, turnLocationOff):
        self.__turnLocationOff = turnLocationOff

    def get_turnLocationOn(self):
        return self.__turnLocationOn

    def set_turnLocationOn(self, turnLocationOn):
        self.__turnLocationOn = turnLocationOn
        