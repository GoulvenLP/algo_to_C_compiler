from .AstNode import AstNode

class Assign(AstNode):

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op


    def getLhs(self):
        return self.lhs

    def getRhs(self):
        return self.rhs

    def getOp(self):
        return self.op