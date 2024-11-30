from tkobject.TkObject import TkObject
from .AstNode import AstNode
class Function(AstNode):

    def __init__(self, name):
        self.name = name #it is an identifier
        self.args = [] # list of arguments. an argument is made of a Binary object that contains a type and an identifier
        self.body = None
        self.returned_type = None   # type returned in the function
        self.return_statement = None    # value of the returned statement

    def getName(self):
        return self.name
    def addArg(self, arg) -> None:
        """ a parameter is a Declaration object containing a type and an identifier """
        self.args.append(arg)

    def addBody(self, body) -> None:
        self.body = body

    def setReturnedType(self, ret): #specifies if the function returns anything
        self.returned_type = ret

    def setReturnStatement(self, ret) -> None:
        self.return_statement = ret

    def getArgs(self):
        return self.args

    def getRetType(self):
        return self.returned_type

    def getBody(self):
        return self.body

    def getReturnStatement(self):
        return self.return_statement

    def getReturnedType(self):
        return self.returned_type