from .AstNode import AstNode

class FunctionCall(AstNode):

    def __init__(self, name):
        self.name = name
        self.arguments = []

    def setName(self, name):
        self.name = name

    def addArg(self, arg):
        self.arguments.append(arg)

    def getName(self):
        return self.name

    def getArgs(self):
        return self.arguments