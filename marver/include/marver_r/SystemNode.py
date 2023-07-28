import Node
from include.marver_r.Topic import Topic

class SystemNode(Node):
    def __init__(self, name: str = None, type: str = None, path: str = None, launchName: str = None,
                 packageName: str = None, topics: [Topic] = []):
        super(SystemNode, self).__init__(name, type, path, launchName, packageName, topics)
