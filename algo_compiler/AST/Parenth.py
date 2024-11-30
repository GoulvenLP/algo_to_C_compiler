from .AstNode import AstNode

class Parenth(AstNode):

    def __init__(self, e):
        self.expr = e

    def getExpr(self):
        return self.expr