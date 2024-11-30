from tkobject.TkObject import TkObject
from .AstNode import AstNode

class Declaration(AstNode):

    def __init__(self, type: TkObject, identifier: TkObject):
        self.name = "Declaration"
        self.type = type
        self.identifier = identifier
        self.size = None

    def setSize(self, size) -> None:
        self.size = size

    def getType(self):
        return self.type

    def getIdentifier(self):
        return self.identifier

    def getSize(self):
        return self.size