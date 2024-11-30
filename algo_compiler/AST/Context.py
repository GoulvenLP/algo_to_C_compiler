from .Visitor import Visitor
from .PrettyPrinter import PrettyPrinter
from .CConverter import CConverter
from .DisplayStrategy import DisplayStrategy
from .Strategies import Strategies #enumeration

class Context:

    strategy: DisplayStrategy

    def __init__(self):
        # Default strategy: PrettyPrinter
        self.strategy = PrettyPrinter()

    def setStrategy(self, strategy: Strategies):
        """
            Sets the current strategy. Takes as a parameter an enumeration, representing one of the available
            strategies.
        """
        if (strategy == Strategies.VISITOR):
            self.strategy = Visitor()
        elif (strategy == Strategies.PRETTYPRINTER):
            self.strategy = PrettyPrinter()
        elif (strategy == Strategies.CCONVERTER):
            self.strategy = CConverter()

    def getStrategy(self):
        return self.strategy

    def execute(self, asTree):
        self.strategy.visitProgram(asTree)

    def displayCode(self):
        self.strategy.displayCode()

    def getCode(self):
        return self.strategy.getCode()
