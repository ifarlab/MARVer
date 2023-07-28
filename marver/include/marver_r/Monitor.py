from include.marver_r.Node import Node
from include.marver_r.Verifier import Verifier
from include.marver_r.Topic import Topic


class Monitor:
    def __init__(self, name: str = None, logFileName: str = None, silent: bool = False, warning: bool = False,
                 oracle: Verifier = None,
                 nodes: [Node] = []):
        self.__name = name
        self.__logFileName = logFileName
        self.__silent = silent
        self.__warning = warning
        self.__oracle = oracle
        self.__nodes = nodes

    def getName(self) -> str:
        return self.__name

    def setName(self, name: str):
        self.__name = name

    def getLogFileName(self) -> str:
        return self.__logFileName

    def setLogFileName(self, logFileName: str):
        self.__logFileName = logFileName

    def getSilent(self) -> bool:
        return self.__silent

    def getOracle(self) -> Verifier:
        return self.__oracle

    def setOracle(self, oracle: Verifier):
        self.__oracle = oracle

    def setSilent(self, silent: bool):
        self.__silent = silent

    def getWarning(self) -> bool:
        return self.__warning

    def setWarning(self, warning: bool):
        self.__warning = warning

    def getNodes(self) -> [Node]:
        return self.__nodes

    def setNodes(self, nodes: [Node] = []):
        self.__nodes.append(nodes)

    def appendNode(self, node: Node = Node()):
        self.__nodes.append(node)

    def removeNode(self, index):
        self.__nodes.pop(index)

    def getTopics(self) -> [Topic]:
        topicList = []
        for node in self.__nodes:
            topicList.extend(node.getTopics())
        return topicList
