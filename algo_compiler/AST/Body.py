from .AstNode import AstNode
class Body(AstNode):

    def __init__(self):
        self.name = "Body"
        self.declarations = []
        self.statements = []

    def addDeclaration(self, declaration) -> None:
        self.declarations.append(declaration)

    def addStatement(self, statement) -> None:
        self.statements.append(statement)

    def getDeclarations(self):
        return self.declarations

    def getStatements(self):
        return self.statements