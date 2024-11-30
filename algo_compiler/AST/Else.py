from tkobject.TkObject import TkObject
from .Body import Body
from .AstNode import AstNode

class Else(AstNode):

    def __init__(self, tok: TkObject, body: Body) -> None:
        self.body = body
        self.tok = tok

    def getBody(self) ->  Body:
        return self.body

    def getTok(self):
        return self.tok