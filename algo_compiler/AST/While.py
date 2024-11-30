from tkobject.TkObject import TkObject
from .AstNode import AstNode

class While(AstNode):

    def __init__(self, tkObject):
        self.tok = tkObject
        self.condition = None
        self.body = None

    def setCondition(self, condition) -> None:
        self.condition = condition

    def setBody(self, body):
        self.body = body

    def getTok(self):
        return self.tok

    def getCondition(self):
        return self.condition

    def getBody(self):
        return self.body