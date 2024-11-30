from .DisplayStrategy import DisplayStrategy

class Visitor(DisplayStrategy):

    def getLastChar(self) -> str:
        pass

    def getCode(self) -> str:
        pass

    def appendToCode(self, code) -> None:
        pass

    def appendPrettily(self, code) -> None:
        pass

    def appendOneCharEarlier(self, code) -> None:
        pass

    def displayCode(self):
        pass

    def getCurrentIndentation(self) -> str:
        pass

    def indent(self) -> str:
        pass

    def dedent(self) -> str:
        pass

    def newLine(self):
        pass
    def visitScalarType(self, scalarType):
        print(scalarType.getKind().getValue())

    def visitArrayType(self, arrayType):
        arrayType.getId().accept(self)
        arrayType.getSize().accept(self)

    def visitArrayAccess(self, arrayAccess):
        arrayAccess.getIdentifier().accept(self)
        arrayAccess.getIndex().accept(self)

    def visitAssign(self, assign):
        assign.getLhs().accept(self)
        assign.getRhs().accept(self)

    def visitBinary(self, binary):
        binary.getLh().accept(self)
        binary.getRh().accept(self)

    def visitBody(self, body):
        for declaration in body.getDeclarations():
            declaration.accept(self)
        for statement in body.getStatements():
            statement.accept(self)

    def visitDeclaration(self, declaration):
        declaration.getType().accept(self)
        declaration.getIdentifier().accept(self)
        if (declaration.getSize() != None):
            declaration.getSize().accept(self)

    def visitDoWhile(self, doWhile):
        doWhile.getBody().accept(self)
        doWhile.getCondition().accept(self)

    def visitIf(self, if_):
        if_.getCondition().accept(self)
        if_.getBody().accept(self)
        if if_.getOtherCondition() != None:
            if_.getOtherCondition().accept(self)
        if if_.getElse() != None:
            if_.getElse().accept(self)

    def visitElse(self, else_):
        else_.getBody().accept(self)

    def visitElseIf(self, elseIf):
        elseIf.getCondition().accept(self)
        elseIf.getBody().accept(self)

    def visitFor(self, for_):
        for_.getRef().accept(self)
        for_.getInit().accept(self)
        for_.getLimit().accept(self)
        for stm in for_.getStatements():
            stm.accept(self)

    def visitFunctionCall(self, functionCall):
        functionCall.getName().accept(self)
        if len(functionCall.getArgs()) > 0:
            for arg in functionCall.getArgs():
                arg.accept(self)

    def visitFunction(self, function):
        function.getName().accept(self)
        for arg in function.getArgs():
            arg.accept(self)
        function.getReturnedType().accept(self)
        function.getBody().accept(self)
        function.getReturnStatement().accept(self)

    def visitReturn(self, returns):
        returns.getTok().accept(self)

    def visitIdentifier(self, identifier):
        print(identifier.getIdentifier().getValue())

    def visitProgram(self, program):
        for func in program.getFunctions():
            func.accept(self)
        for decl in program.getDeclarations():
            decl.accept(self)
        for stm in program.getStatements():
            stm.accept(self)

    def visitUnary(self, unary):
        opp = False
        if (unary.getOpposed() != None):
            opp = True
            print(unary.getOpposed().getValue())
        if (unary.getOperator() != None):
            print(unary.getOperator().getValue())
        unary.getPrimary().accept(self)
        if (opp):
            print(')')

    def visitWhile(self, while_):
        while_.getCondition().accept(self)
        while_.getBody().accept(self)

    def visitIntLiteral(self, intLit):
        print(intLit.getToken().getValue())

    def visitFloatLiteral(self, floatLit):
        print(floatLit.getToken().getValue())

    def visitCharLiteral(self, charLit):
        print(charLit.getToken().getValue())

    def visitBooleanLiteral(self, boolLit):
        print(boolLit.getToken().getValue())

    def visitStringLiteral(self, stringLit):
        print(stringLit.getToken().getValue())

    def visitReturn(self, returns):
        print(returns.getTok().getValue())
        returns.getExpr().accept(self)
    def visitParenth(self, parenth):
        print('(')
        parenth.getExpr().accept(self)
        print(')')