from .AstNode import AstNode

class Return(AstNode):

    def __init__(self, tok):
        self.tok = tok
        self.expr = None

    def setExpr(self, expr):
        self.expr = expr

    def getTok(self):
        return self.tok

    def getExpr(self):
        return self.expr