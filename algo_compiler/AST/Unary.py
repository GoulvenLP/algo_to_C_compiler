from .AstNode import AstNode

class Unary(AstNode):

    def __init__(self,tok):
        self.tok = tok
        self.expr = None

    def setExpr(self, e):
        self.expr = e

    def getTok(self):
        return self.tok

    def getExpr(self):
        return self.expr

    # def setOperator(self, operator):
    #     self.operator = operator
    #
    # def setExpression(self, expr):
    #     self.primary = expr
    #
    # def setOpposed(self, tok):
    #     self.opposed = tkNot
    #
    # def getOperator(self):
    #     return self.operator
    #
    # def getOpposed(self):
    #     return self.opposed
    #
    # def getPrimary(self):
    #     return self.primary