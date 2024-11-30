
class TkObject:

    def __init__(self, TK_TYPE, TK_VALUE):
        self.TK_TYPE = TK_TYPE
        self.TK_VALUE = TK_VALUE


    def addCoordinates(self, line, column):
        self.line = line
        self.column = column

    def getLine(self):
        return self.line

    def getColumn(self):
        return self.column

    def getType(self):
        return self.TK_TYPE

    def getValue(self):
        return self.TK_VALUE

    def __str__(self):
        return self.TK_TYPE + ': ' + self.TK_VALUE + ' [' + self.line + ', ' + self.column + ']'