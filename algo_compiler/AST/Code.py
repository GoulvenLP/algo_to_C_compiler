from .Indentation import Indentation

class Code:

    def __init__(self):
        self.code = ""
        self.indentation = Indentation()

    def getCode(self) -> str:
        """ Returns the whole code as a string """
        return self.code

    def getLastChar(self) -> str:
        """ Returns the last char found int the current code """
        return self.code[len(self.code) - 1 :]
    def appendPrettily(self, code):
        """ Concatenates the code given as an argument to the current code. concatenates to this code one space right behind it"""
        self.code += code + " "

    def appendToCode(self, code):
        """ Concatenates the code given as an argument to the current code. """
        self.code += code

    def appendOneCharEarlier(self, code):
        """
            Concatenates the code given as an argument to the current code one character earlier IF the previous
            character is a blank space
        """
        if (len(self.code) == 0):
            raise RuntimeError("The current code is empty. No concatenation can be made at a previous index")
        if (self.code[len(self.code) -1] == " "):
            self.code = self.code[:len(self.code) - 1] + code
        else:
            self.appendToCode(code)

    def newLine(self):
        self.code += '\n'

    def display(self) -> None:
        print(self.code)

    def indent(self) -> str:
        return self.indentation.indent()

    def dedent(self) -> str:
        return self.indentation.dedent()

    def resetIndent(self) -> str:
        return self.indentation.resetIndent()

    def getCurrentIndentation(self) -> str:
        return self.indentation.getIndent()

