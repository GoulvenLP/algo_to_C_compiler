from tkobject.TkObject import TkObject
from .Body import Body
from .AstNode import AstNode

class If(AstNode):

    def __init__(self, tkObject):
        self.tkObject = tkObject
        self.condition = None
        self.body = None
        self.otherCondition = None
        self.else_ = None

    def addCondition(self, condition) -> None:
        self.condition = condition

    def addBody(self, body: Body) -> None:
        self.body = body

    def addElse(self, else_):
        self.else_ = else_
    def addOtherCondition(self, otherCondition) -> None:
        self.otherCondition = otherCondition

    def getIf(self) -> TkObject:
        return self.tkObject

    def getCondition(self):
        return self.condition

    def getBody(self) -> Body:
        return self.body

    def getOtherCondition(self):
        return self.otherCondition


    def getElse(self):
        return self.else_