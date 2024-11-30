from tkobject.TkObject import TkObject
from .AstNode import AstNode

class For(AstNode):

    def __init__(self, tkObject):
        self.tkObject = tkObject
        self.ref = None
        self.init = None
        self.limit = None
        self.statements = []

    def addConfiguration(self, ref, init, limit) -> None:
        self.ref = ref
        self.init = init
        self.limit = limit

    def addRef(self, ident) -> None:
        self.ref = ident

    def addInit(self, init) -> None:
        self.init = init

    def addLimit(self, limit) -> None:
        self.limit = limit

    def addBody(self, statement) -> None:
        self.statements.append(statement)

    def getTkObject(self):
        return self.tkObject

    def getRef(self):
        return self.ref

    def getInit(self):
        return self.init

    def getLimit(self):
        return self.limit

    def getStatements(self):
        return self.statements