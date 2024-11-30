from .AstNode import AstNode

class ArrayAccess(AstNode):

    def __init__(self, identifier, index):
        self.identifier = identifier
        self.index = index


    def getIdentifier(self):
        return self.identifier

    def getIndex(self):
        return self.index