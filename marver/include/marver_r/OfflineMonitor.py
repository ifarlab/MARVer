import Monitor
import Verifier
from include.marver_r.Topic import Topic
from include.marver_r.Node import Node


class OfflineMonitor(Monitor):
    def __init__(self, name: str = None, logFileName: str = None, silent: bool = None, oracle: Verifier = None,
                 nodes: [Node] = [], topics: [Topic] = []):
        super(OfflineMonitor, self).__init__(name, logFileName, silent, oracle, nodes, topics)

    def generate(self) -> bool:
        pass
