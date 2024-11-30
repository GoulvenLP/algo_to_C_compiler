
class ReturnError(Exception):

    def __init__(self, msg, tok):
        msg += " line " + str(tok.getLine()) + " column " + str(tok.getColumn())
        super().__init__(msg)