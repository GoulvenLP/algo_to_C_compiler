
class ParserError(Exception):

    def __init__(self, message, tkObject):
        message += " line " + str(tkObject.getLine()) + " column " + str(tkObject.getColumn())
        super().__init__(message)