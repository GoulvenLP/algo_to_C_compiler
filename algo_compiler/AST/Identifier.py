from .SingleTokenNode import SingleTokenNode

class Identifier(SingleTokenNode):

    def __init__(self, identifier):
        self.identifier = identifier
    def getIdentifier(self):
        return self.identifier
