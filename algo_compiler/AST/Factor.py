from .AstNode import AstNode


class Factor(AstNode):

    def __init__(self, tkObject):
        self.tkObject = tkObject
        self.not_ = None
        self.unary = None
        self.primary = None

    def setNot(self, not_):
        self.not_ = not_

    def setUnary(self, unary):
        self.unary = unary

    def setPrimary(self, primary):
        self.primary = primary

    def getNot(self):
        return self.not_

    def getUnary(self):
        return self.unary

    def getPrimary(self):
        return self.primary