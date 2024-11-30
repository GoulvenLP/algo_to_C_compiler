from abc import abstractmethod


class DisplayStrategy:

    class JavaConverter:

        @abstractmethod
        def getLastChar(self) -> str:
            pass

        @abstractmethod
        def getCode(self) -> str:
            pass

        @abstractmethod
        def appendToCode(self, code) -> None:
            pass

        @abstractmethod
        def appendPrettily(self, code) -> None:
            pass

        @abstractmethod
        def appendOneCharEarlier(self, code) -> None:
            pass

        @abstractmethod
        def displayCode(self):
            pass

        @abstractmethod
        def getCurrentIndentation(self) -> str:
            pass

        @abstractmethod
        def indent(self) -> str:
            pass

        @abstractmethod
        def dedent(self) -> str:
            pass

        @abstractmethod
        def newLine(self):
            pass

        @abstractmethod
        def visitScalarType(self, scalarType):
            pass

        @abstractmethod
        def visitArrayType(self, arrayType):
            pass

        @abstractmethod
        def visitArrayAccess(self, arrayAccess):
            pass

        @abstractmethod
        def visitAssign(self, assign):
            pass

        @abstractmethod
        def visitBinary(self, binary):
            pass

        @abstractmethod
        def visitBody(self, body):
            pass

        @abstractmethod
        def visitDeclaration(self, declaration):
            pass

        @abstractmethod
        def visitFor(self, for_):
            pass

        @abstractmethod
        def visitWhile(self, while_):
            pass

        @abstractmethod
        def visitDoWhile(self, doWhile):
            pass

        @abstractmethod
        def visitIf(self, if_):
            pass

        @abstractmethod
        def visitElseIf(self, elseIf):
            pass

        @abstractmethod
        def visitElse(self, else_):
            pass

        @abstractmethod
        def visitFactor(self, factor):
            pass

        @abstractmethod
        def visitFunctionCall(self, functionCall):
            pass

        @abstractmethod
        def visitFunction(self, function):
            pass

        @abstractmethod
        def visitIdentifier(self, identifier):
            pass

        @abstractmethod
        def visitProgram(self, program):
            pass

        @abstractmethod
        def visitUnary(self, unary):
            pass

        @abstractmethod
        def visitIntLiteral(self, intLit):
            pass

        @abstractmethod
        def visitFloatLiteral(self, floatLit):
            pass

        @abstractmethod
        def visitCharLiteral(self, charLit):
            pass

        @abstractmethod
        def visitBooleanLiteral(self, boolLit):
            pass

        @abstractmethod
        def visitStringLiteral(self, stringLit):
            pass

        @abstractmethod
        def visitReturn(self, returns):
            pass

        @abstractmethod
        def visitParenth(self, parenth):
            pass