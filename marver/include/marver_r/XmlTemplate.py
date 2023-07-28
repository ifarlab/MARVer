
class XmlTemplate:
    def __init__(self, name, variables=[]):
        self.__name = name
        self.__nodes = []
        self.__localVariables = variables

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def addNode(self, node: str):
        self.__nodes.append(node)

    def getNodes(self) -> [str]:
        return self.__nodes

    def setVariables(self, variableList):
        self.__localVariables = variableList

    def getVariables(self):
        return self.__localVariables
