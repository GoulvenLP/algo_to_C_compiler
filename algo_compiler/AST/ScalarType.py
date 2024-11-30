from .Type import Type

class ScalarType(Type):

    def __init__(self, kind):
        self.kind = kind

    def getKind(self):
        return self.kind

    def setKind(self, kind):
        self.kind = kind