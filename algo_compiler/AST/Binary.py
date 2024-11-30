from tkobject.TkObject import TkObject
from .AstNode import AstNode

class Binary(AstNode):

    def __init__(self, op: TkObject):
        self.op = op
        self.lh = None
        self.rh = None

    def addLh(self, bin) -> None:
        self.lh = bin

    def addRh(self, bin) -> None:
        self.rh = bin

    def getOp(self) -> TkObject:
        return self.op

    def getLh(self):
        return self.lh

    def getRh(self):
        return self.rh
