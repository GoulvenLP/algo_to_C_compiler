from .Code import Code
from .DisplayStrategy import DisplayStrategy

class CConverter(DisplayStrategy):
    def __init__(self):
        self.code = Code()

    def getLastChar(self) -> str:
        """ Returns the last character found in the current code """
        return self.code.getLastChar()

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
        if (scalarType.getKind().getType() == "tk_typeVoid"):
            self.appendPrettily("void")
        if (scalarType.getKind().getType() == "tk_typeInt"):
            self.appendPrettily("int")
        elif(scalarType.getKind().getType() == "tk_typeFloat"):
            self.appendPrettily("float")
        elif(scalarType.getKind().getType() == "tk_typeChar"):
            self.appendPrettily("char")
        elif(scalarType.getKind().getType() == "tk_typeString"):
            self.appendPrettily("String")
        elif(scalarType.getKind().getType() == "tk_typeBoolean"):
            self.appendPrettily("int")

    def visitArrayType(self, arrayType):
        arrayType.getId().accept(self)
        self.appendOneCharEarlier('[')
        arrayType.getSize().accept(self)
        self.appendOneCharEarlier(']')
        self.appendToCode(' ')

    def visitArrayAccess(self, arrayAccess):
        arrayAccess.getIdentifier().accept(self)
        arrayAccess.getIndex().accept(self)

    def visitAssign(self, assign):
        assign.getLhs().accept(self)
        self.appendPrettily('=')
        assign.getRhs().accept(self)

    def visitBinary(self, binary):
        binary.getLh().accept(self)

        if (binary.getOp().getType() == "tk_and"):
            self.appendPrettily("&&")
        elif (binary.getOp().getType() == "tk_or" ):
            self.appendPrettily("||")
        elif (binary.getOp().getType() == "tk_equal"):
            self.appendPrettily("==")
        else:
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
                self.appendOneCharEarlier(';')
                self.newLine()

        for i in range(lenSttm):
            sttm[i].accept(self)
            if (self.getLastChar() != "}"):
                self.appendOneCharEarlier(';')
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
        self.appendPrettily("for(")
        for_.getRef().accept(self)
        self.appendPrettily("=")
        for_.getInit().accept(self)
        self.appendOneCharEarlier("; ")
        for_.getRef().accept(self)
        self.appendPrettily("<")
        for_.getLimit().accept(self)
        self.appendOneCharEarlier("; ")
        for_.getRef().accept(self)
        #TODO ANALYSE ITEMS TO DECIDE INCREMENTATION OR DECREMENTATION?
        self.appendOneCharEarlier("++ )")
        self.appendPrettily("{")
        self.indent()
        self.newLine()
        for stm in for_.getStatements():
            stm.accept(self)
        self.dedent()
        self.newLine()
        self.appendToCode("}")

    def visitWhile(self, while_):
        self.appendToCode('while')
        self.appendPrettily('(')
        while_.getCondition().accept(self)
        self.appendToCode(')')
        self.appendPrettily('{')
        self.indent()
        self.newLine()
        while_.getBody().accept(self)
        self.dedent()
        self.newLine()
        self.appendToCode('}')

    def visitDoWhile(self, doWhile):
        self.newLine()
        self.appendPrettily('do {')
        self.indent()
        self.newLine()
        doWhile.getBody().accept(self)
        self.dedent()
        self.newLine()
        self.appendPrettily('} while(')
        doWhile.getCondition().accept(self)
        self.appendToCode(')')

    def visitIf(self, if_):
        self.appendPrettily('if')
        self.appendPrettily('(')
        if_.getCondition().accept(self)
        self.appendToCode(')')
        self.appendToCode('{')
        self.indent()
        self.newLine()
        if_.getBody().accept(self)
        if if_.getOtherCondition() != None:
            if_.getOtherCondition().accept(self)
        if if_.getElse() != None:
            if_.getElse().accept(self)
        self.dedent()
        self.newLine()
        self.appendToCode('}')

    def visitElseIf(self, elseIf):
        self.dedent()
        self.newLine()
        self.appendPrettily('} else if (')
        elseIf.getCondition().accept(self)
        self.appendToCode(')')
        self.appendToCode("{")
        self.indent()
        self.newLine()
        elseIf.getBody().accept(self)

    def visitElse(self, else_):
        self.dedent()
        self.newLine()
        self.appendPrettily("} else {")
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
        function.getReturnedType().accept(self)
        function.getName().accept(self)
        self.appendOneCharEarlier('(')
        for arg in function.getArgs():
            arg.accept(self)
            if (arg != function.getArgs()[len(function.getArgs()) - 1]):  # display comas between args
                self.appendOneCharEarlier(", ")
        self.appendOneCharEarlier(')')
        self.appendToCode("{")
        self.indent()
        self.newLine()
        function.getBody().accept(self)
        self.newLine()
        if (function.getReturnStatement() != None):
            function.getReturnStatement().accept(self)
        self.dedent()
        self.newLine()
        self.appendToCode("}")
        self.newLine()

    def visitIdentifier(self, identifier):
        self.appendPrettily(identifier.getIdentifier().getValue())

    def visitProgram(self, program):
        self.appendToCode('#include <stdio.h>')
        self.newLine()
        self.appendToCode('#include <stdlib.h>')
        self.newLine()
        self.newLine()
        for func in program.getFunctions():
            func.accept(self)
            self.newLine()
        self.appendToCode("int main(int argc, char* argv[]) {")
        self.indent()
        self.newLine()

        lenSttm = len(program.getStatements())
        lenDecl = len(program.getDeclarations())
        decl = program.getDeclarations()
        sttm = program.getStatements()
        for i in range(lenDecl):
            decl[i].accept(self)
            if (((i < lenDecl - 1) and lenSttm == 0) or lenSttm > 0):
                self.appendOneCharEarlier(';')
                self.newLine()

        for i in range(lenSttm):
            sttm[i].accept(self)
            if (self.getLastChar() != "}"):
                self.appendOneCharEarlier(';')
            if (i < lenSttm - 1):
                self.newLine()

        self.newLine()
        self.appendToCode('return EXIT_SUCCESS;')
        self.dedent()
        # self.newLine()
        self.newLine()
        self.appendToCode('}')


    def visitUnary(self, unary):
        if (unary.getTok().getType() == "tk_not"):
            self.appendPrettily('!')
        elif (unary.getTok().getType() == "tk_minus"):
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
        if (boolLit.getToken().getValue() == 'vrai'):
            self.appendPrettily('0')
        elif (boolLit.getToken().getValue() == 'faux'):
            self.appendPrettily('1')

    def visitStringLiteral(self, stringLit):
        self.appendPrettily(stringLit.getToken().getValue())

    def visitReturn(self, returns):
        self.appendPrettily('return')
        returns.getExpr().accept(self)
        self.appendOneCharEarlier(';')
        self.newLine()

    def visitParenth(self, parenth):
        self.appendPrettily('(')
        parenth.getExpr().accept(self)
        self.appendPrettily(')')