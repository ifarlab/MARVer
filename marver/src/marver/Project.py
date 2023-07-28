class Project:
    def __init__(self):
        self.__rosPath = None
        self.__confFilePath = None
        self.__propertyFilePath = None
        self.__projectFilePath = None

    def getRosPath(self) -> str:
        return self.__rosPath

    def setRosPath(self, rosPath: str):
        self.__rosPath = rosPath

    def getConfFilePath(self) -> str:
        return self.__confFilePath

    def setConfFilePath(self, confFilePath: str):
        self.__confFilePath = confFilePath

    def getPropertyFilePath(self) -> str:
        return self.__propertyFilePath

    def setPropertyFilePath(self, propertyFilePath: str):
        self.__propertyFilePath = propertyFilePath

    def getProjectFilePath(self) -> str:
        return self.__projectFilePath

    def setProjectFilePath(self, projectFilePath: str):
        self.__projectFilePath = projectFilePath
