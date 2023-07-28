from include.marver_r.Property import Property

class Verifier:
    def __init__(self, port: int = None, url: str = None, action: str = None,
                 properties: [Property] = []):
        self.__port = port
        self.__url = url
        self.__action = action
        self.__properties = properties

    def setPort(self, port: int):
        self.__port = port

    def getPort(self) -> int:
        return self.__port

    def setUrl(self, url: str):
        self.__url = url

    def getUrl(self) -> str:
        return self.__url

    def setAction(self, action: str):
        self.__action = action

    def getAction(self) -> str:
        return self.__action

    def setProperties(self, property: Property):
        self.__properties.append(property)

    def getProperties(self) -> [Property]:
        return self.__properties

    def getPropertyByName(self, name: str) -> Property:
        for property in self.__properties:
            if property.getName() == name:
                return property
        return None

    def getPropertiesByName(self, names: [str]) -> [Property]:
        temp = []
        for property in self.__properties:
            if property.getName() in names:
                temp.append(property)
        return temp

    def isExist(self, name: str) -> [bool, int]:
        for index in range(len(self.__properties)):
            if self.__properties[index].getName() == name:
                return [True, index]
        return [False, -1]

    def deletePropertyByName(self, name: str):
        for index in range(len(self.__properties)):
            if self.__properties[index].getName() == name:
                self.__properties.pop(index)
                return
