from tkobject.TkObject import TkObject
from .Body import Body
from .AstNode import AstNode

class ElseIf(AstNode):

    def __init__(self, tkObject: TkObject):
        self.tkObject = tkObject
        self.condition = None
        self.body = None

    def addCondition(self, condition) -> None:
        self.condition =condition

    def addBody(self, body: Body) -> None:
        self.body = body

    def getTkObject(self) -> TkObject:
        return self.tkObject

    def getCondition(self):
        return self.condition

    def getBody(self) -> Body:
        return self.body
