import Node
from include.marver_r.Topic import Topic


class ServiceNode(Node):
    def __init__(self, name: str = None, type: str = None, path: str = None, launchName: str = None,
                 packageName: str = None, topics: [Topic] = []):
        super(ServiceNode, self).__init__(name, type, path, launchName, packageName, topics)
