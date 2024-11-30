from .AstNode import AstNode

class SingleTokenNode(AstNode):
    def __init__(self, tok):
        self.tok = tok

    def getToken(self):
        return self.tok