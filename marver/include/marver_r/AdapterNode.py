import Node
from include.marver_r.Topic import Topic


class AdapterNode(Node):
    def __init__(self, name: str = None, type: str = None, path: str = None, launchName: str = None,
                 packageName: str = None, topics: [Topic] = None):
        Node.__init__(self, name, type, path, launchName, packageName, topics)
