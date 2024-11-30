from .Function import Function
from .Declaration import Declaration
from .AstNode import AstNode

class Program(AstNode):

    def __init__(self):
        self.name = "Program"
        self.functions = []
        self.declarations = []
        self.statements = []

    def getName(self) -> str:
        return self.name

    def addFunction(self, function) -> None:
        self.functions.append(function)

    def addDeclaration(self, declaration) -> None:
        self.declarations.append(declaration)

    def addStatement(self, statement) -> None:
        self.statements.append(statement)

    def getFunctions(self) -> [Function]:
        return self.functions

    def getDeclarations(self) -> [Declaration]:
        return self.declarations

    def getStatements(self) -> [AstNode] :
        return self.statements