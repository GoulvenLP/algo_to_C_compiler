from .Code import Code
from .DisplayStrategy import DisplayStrategy

class PrettyPrinter(DisplayStrategy):
    def __init__(self):
        self.code = Code()

    def getLastChar(self) -> str:
        pass

    def getCode(self) -> str:
        """ Returns the whole code as a string """
        return self.code.getCode()

    def appendToCode(self, code) -> None:
        """ Concatenates code to the current code """
        self.code.appendToCode(code)

    def appendPrettily(self, code) -> None:
        """ Concatenates code to the current code with a blank space between both codes """
        self.code.appendPrettily(code)

    def appendOneCharEarlier(self, code) -> None:
        """ Places the code given as an argument one character earlier in the previous code """
        self.code.appendOneCharEarlier(code)

    def displayCode(self):
        """ Displays the code in the pretty printer-way"""
        self.code.display()

    def getCurrentIndentation(self) -> str:
        """ Returns the current indentation as blank text """
        return self.code.getCurrentIndentation()

    def indent(self) -> str:
        """ Increases the level of indentation and returns the corresponding blank space generated"""
        return self.code.indent()

    def dedent(self) -> str:
        """ Reduces the level of indentation by one and returns the corresponding blank space generated """
        return self.code.dedent()

    def newLine(self):
        """ Jumps a new line and applies the current level of indentation to the next line """
        self.code.newLine()
        self.appendToCode(self.getCurrentIndentation())

    def visitScalarType(self, scalarType):
        self.appendPrettily(scalarType.getKind().getValue())

    def visitArrayType(self, arrayType):
        arrayType.getId().accept(self)
        self.appendOneCharEarlier('[')
        arrayType.getSize().accept(self)
        self.appendOneCharEarlier(']')
        self.appendToCode(' ')

    def visitArrayAccess(self, arrayAccess):
        arrayAccess.getIdentifier().accept(self)
        self.appendOneCharEarlier('[')
        arrayAccess.getIndex().accept(self)
        self.appendOneCharEarlier(']')
        self.appendToCode(' ')

    def visitAssign(self, assign):
        assign.getLhs().accept(self)
        self.appendPrettily(assign.getOp().getValue())
        assign.getRhs().accept(self)

    def visitBinary(self, binary):
        binary.getLh().accept(self)
        self.appendPrettily(binary.getOp().getValue())
        binary.getRh().accept(self)


    def visitBody(self, body):
        lenSttm = len(body.getStatements())
        lenDecl = len(body.getDeclarations())
        decl = body.getDeclarations()
        sttm = body.getStatements()
        for i in range(lenDecl):
            decl[i].accept(self)
            if (((i < lenDecl - 1) and lenSttm == 0) or lenSttm > 0):
                self.newLine()

        for i in range(lenSttm):
            sttm[i].accept(self)
            if (i < lenSttm - 1):
                self.newLine()


    def visitDeclaration(self, declaration):
        self.indent()
        declaration.getType().accept(self)
        declaration.getIdentifier().accept(self)
        if (declaration.getSize() != None):
            declaration.getSize().accept(self)
        self.dedent()

    def visitFor(self, for_):
        self.newLine()
        self.appendPrettily("pour")
        for_.getRef().accept(self)
        self.appendPrettily("de")
        for_.getInit().accept(self)
        self.appendPrettily("à")
        for_.getLimit().accept(self)
        self.indent()
        self.newLine()
        self.appendPrettily("faire")
        self.newLine()
        for stm in for_.getStatements():
            stm.accept(self)
        self.dedent()
        self.newLine()
        self.appendPrettily("fin pour")

    def visitWhile(self, while_):
        self.appendPrettily(while_.getTok().getValue())
        while_.getCondition().accept(self)
        self.indent()
        self.newLine()
        self.appendPrettily('faire')
        self.newLine()
        while_.getBody().accept(self)
        self.dedent()
        self.newLine()
        self.appendToCode("fin tant que")

    def visitDoWhile(self, doWhile):
        self.newLine()
        self.appendPrettily(doWhile.getTkObject().getValue())
        self.indent()
        self.newLine()
        doWhile.getBody().accept(self)
        self.dedent()
        self.newLine()
        self.appendPrettily("tant que")
        doWhile.getCondition().accept(self)

    def visitIf(self, if_):
        self.newLine()
        self.appendPrettily(if_.getIf().getValue())
        if_.getCondition().accept(self)
        self.indent()
        self.newLine()
        self.appendToCode("alors")
        self.newLine()
        if_.getBody().accept(self)
        if if_.getOtherCondition() != None:
            if_.getOtherCondition().accept(self)
        if if_.getElse() != None:
            if_.getElse().accept(self)
        self.dedent()
        self.newLine()
        self.appendToCode("fin si")
        #self.newLine()

    def visitElseIf(self, elseIf):
        self.dedent()
        self.newLine()
        self.appendPrettily(elseIf.getTkObject().getValue())
        elseIf.getCondition().accept(self)
        self.indent()
        self.newLine()
        self.appendToCode("alors")
        self.newLine()
        elseIf.getBody().accept(self)

    def visitElse(self, else_):
        self.dedent()
        self.newLine()
        self.appendPrettily(else_.getTok().getValue())
        self.indent()
        self.newLine()
        else_.getBody().accept(self)


    def visitFunctionCall(self, functionCall):
        functionCall.getName().accept(self)
        self.appendOneCharEarlier('(')
        if len(functionCall.getArgs()) > 0:
            for arg in functionCall.getArgs():
                arg.accept(self)
                if (arg != functionCall.getArgs()[len(functionCall.getArgs()) - 1]): #display comas between args
                    self.appendOneCharEarlier(", ")
        self.appendOneCharEarlier(')')

    def visitFunction(self, function):
        function.getName().accept(self)
        self.appendOneCharEarlier('(')
        for arg in function.getArgs():
            arg.accept(self)
            if (arg != function.getArgs()[len(function.getArgs()) - 1]):  # display comas between args
                self.appendOneCharEarlier(", ")
        self.appendOneCharEarlier('): ')
        function.getReturnedType().accept(self)
        self.indent()
        self.newLine()
        self.appendToCode("début")
        self.newLine()
        function.getBody().accept(self)
        self.newLine()
        if (function.getReturnStatement() != None):
            function.getReturnStatement().accept(self)
        self.appendToCode("fin")
        self.dedent()
        self.newLine()

    def visitIdentifier(self, identifier):
        self.appendPrettily(identifier.getIdentifier().getValue())

    def visitProgram(self, program):
        for func in program.getFunctions():
            func.accept(self)
            self.newLine()
        for decl in program.getDeclarations():
            decl.accept(self)
            self.newLine()
        for stm in program.getStatements():
            stm.accept(self)
            self.newLine()

    def visitUnary(self, unary):
        self.appendPrettily(unary.getTok().getValue())
        unary.getExpr().accept(self)
        if (unary.getTok().getType() == "tk_not"):
            self.appendPrettily(')')


    def visitIntLiteral(self, intLit):
        self.appendPrettily(intLit.getToken().getValue())

    def visitFloatLiteral(self, floatLit):
        self.appendPrettily(floatLit.getToken().getValue())

    def visitCharLiteral(self, charLit):
        self.appendPrettily(charLit.getToken().getValue())

    def visitBooleanLiteral(self, boolLit):
        self.appendPrettily(boolLit.getToken().getValue())

    def visitStringLiteral(self, stringLit):
        self.appendPrettily(stringLit.getToken().getValue())

    def visitReturn(self, returns):
        self.appendPrettily(returns.getTok().getValue())
        returns.getExpr().accept(self)
        self.newLine()

    def visitParenth(self, parenth):
        self.appendPrettily('(')
        parenth.getExpr().accept(self)
        self.appendPrettily(')')