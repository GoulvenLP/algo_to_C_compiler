from .Type import Type


class ArrayType(Type):

    def __init__(self, id, size):
        self.id = id
        self.size = size

    def getId(self):
        return self.id

    def getSize(self):
        return self.size