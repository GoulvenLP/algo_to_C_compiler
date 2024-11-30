from tkobject.TkObject import TkObject
from .AstNode import AstNode

class DoWhile(AstNode):

    def __init__(self, tkObject):
        self.tkObject = tkObject
        self.body = None
        self.condition = None

    def addCondition(self, condition) -> None:
        self.condition = condition

    def addBody(self, body):
        self.body = body

    def getCondition(self):
        return self.condition

    def getBody(self):
        return self.body

    def getTkObject(self):
        return self.tkObject
