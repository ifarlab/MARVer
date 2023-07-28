from include.marver_r.Verifier import Verifier
from include.marver_r.Property import Property


class RMLOracle(Verifier):
    def __init__(self, port: int = None, url: str = None, action: str = None, properties: [Property] = []):
        super(RMLOracle, self).__init__(port, url, action, properties)
