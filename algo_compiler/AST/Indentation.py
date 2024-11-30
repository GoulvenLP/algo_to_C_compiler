# manages the level of indentation

class Indentation:

    def __init__(self):
        self.level = 0
        self.ref = "    " #indentation : 4

    def indent(self) -> str:
        """ Increases the level of indentation by one level. Returns the text corresponding to the current level
        of indentation
        """
        self.level += 1
        return self.getIndent()

    def dedent(self) -> str:
        """ Decreases the level of indentation by one level. Returns the text corresponding to the current
        level of indentation
        """
        self.level -= 1
        if (self.level < 0):
            self.level = 0
        return self.getIndent()

    def getIndent(self) -> str:
        """ Converts the current level of indentation into the corresponding space text """
        idt = ""
        for i in range(0, self.level, 1):
            idt += self.ref
        return idt

    def resetIndent(self) -> str:
        """ Resets the level of indentation to zero. Returns a no spaced text """
        self.level = 0
        return self.getIndent()