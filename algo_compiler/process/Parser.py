from tkobject.TkObject import TkObject
from errors.ParserError import ParserError
from errors.ReturnError import ReturnError
from AST.Program import Program
from AST.Function import Function
from AST.FunctionCall import FunctionCall
from AST.Binary import Binary
from AST.Body import Body
from AST.Declaration import Declaration
from AST.Unary import Unary
from AST.If import If
from AST.ElseIf import ElseIf
from AST.Else import Else
from AST.While import While
from AST.For import For
from AST.DoWhile import DoWhile
from AST.IntLiteral import IntLiteral
from AST.FloatLiteral import FloatLiteral
from AST.CharLiteral import CharLiteral
from AST.StringLiteral import StringLiteral
from AST.BooleanLiteral import BooleanLiteral
from AST.Identifier import Identifier
from AST.ScalarType import  ScalarType
from AST.ArrayAccess import ArrayAccess
from AST.Assign import Assign
from AST.ArrayType import ArrayType
from AST.Return import Return
from AST.Parenth import Parenth


class Parser:

    def __init__(self, tkObjectList):
        self.tkObjectList = tkObjectList

    def showNext(self, k) -> TkObject:
        """ returns the k-th object of the tkObject list, k being an indice. if k is superior to the biggest indice in the list, nothing is returned
            @param k: indice of the object the user wants to be returned
        """
        if (k >= len(self.tkObjectList)):
            raise Exception("The parser is trying to reach an index that is out of bounds: your token list may be shorter than expected")
        return self.tkObjectList[k]


    def accept_it(self) -> None:
        """ removes the first object of the tkObject list """
        self.tkObjectList.pop(0)


    def expect(self, tk_token) -> TkObject:
        """ verifies that the next TkObject's type (in the list) corresponds to the tk_object given as a parameter"""
        if self.tkObjectList[0].getType() == tk_token:
            return self.tkObjectList.pop(0)
        else:
            if (self.tkObjectList[0].getType() == 'tk_linebreak'):
                raise ParserError("Unexpected token: linebreak", self.showNext(0))
            else:
                raise ParserError("Unexpected token: '" + self.tkObjectList[0].getValue() + "'", self.tkObjectList[0])

    def parse_program(self) -> Program:
        self.parse_linebreaks()
        program = Program()
        # Function declarations
        while (len(self.tkObjectList) > 0 and self.showNext(0).getType() != "tk_typeInt" and self.showNext(0).getType() != "tk_typeFloat" and self.showNext(0).getType() != "tk_typeBoolean" and self.showNext(0).getType() != "tk_typeChar"):
            function = self.parse_function()
            program.addFunction(function)
            self.parse_linebreaks()
        # Use of main
        while (len(self.tkObjectList) > 0 and (self.showNext(0).getType() == "tk_typeInt" or self.showNext(0).getType() == "tk_typeFloat" or self.showNext(
                0).getType() == "tk_typeBoolean" or self.showNext(0).getType() == "tk_typeChar" or self.showNext(
            0).getType() == "tk_typeVoid")):
            declaration = self.parse_declaration()
            program.addDeclaration(declaration)
            self.parse_linebreaks()
        while (len(self.tkObjectList) > 0 and (self.showNext(0).getType() == "tk_identifier" or self.showNext(0).getType() == "tk_if" or self.showNext(
                0).getType() == "tk_for" or self.showNext(0).getType() == "tk_while" or self.showNext(
            0).getType() == "tk_do")):
            try:
                statement = self.parse_statement()
                program.addStatement(statement)
            except Exception as pe:
                raise ParserError(str(pe))
        return program

    def parse_function(self) -> Function:
        funcId = self.expect("tk_identifier")
        functionName = Identifier(funcId) # function name
        function = Function(functionName)
        returned_type = None
        return_something = False #specifies if a return statement has been found
        self.expect("tk_lParenth")
        if (self.showNext(0).getType() == "tk_typeInt" or self.showNext(0).getType() == "tk_typeFloat" or self.showNext(0).getType() == "tk_typeBoolean" or self.showNext(0).getType() == "tk_typeChar"):
            # argument
            type = self.parse_type()
            id = self.expect("tk_identifier")
            varName = Identifier(id)
            arg = Declaration(type, varName)
            function.addArg(arg)
            while (self.showNext(0).getType() == "tk_comma"): # more than one argument
                self.accept_it()
                type2 = self.parse_type()
                id3 = self.expect("tk_identifier")
                otherVarName = Identifier(id3)
                arg = Declaration(type2, otherVarName)
                function.addArg(arg)
        self.expect("tk_rParenth")
        self.expect("tk_colon")
        returned_type = self.parse_type() # returned type
        function.setReturnedType(returned_type)
        self.expect("tk_linebreak")
        self.expect("tk_beginFunction")
        self.expect("tk_linebreak")
        self.parse_linebreaks()
        # possible declarations in the middle of the function
        body = Body()
        while (self.showNext(0).getType() == "tk_typeInt" or self.showNext(0).getType() == "tk_typeFloat" or
               self.showNext(0).getType() == "tk_typeBoolean" or self.showNext(0).getType() == "tk_typeChar"):
            while (self.showNext(0).getType() == "tk_typeInt" or self.showNext(0).getType() == "tk_typeFloat" or
                   self.showNext(0).getType() == "tk_typeBoolean" or self.showNext(0).getType() == "tk_typeChar"):
                declaration = self.parse_declaration()
                body.addDeclaration(declaration)
            while (self.showNext(0).getType() == "tk_identifier" or self.showNext(0).getType() == "tk_if" or
                   self.showNext(0).getType() == "tk_for" or self.showNext(0).getType() == "tk_while" or
                   self.showNext(0).getType() == "tk_do"):
                statement = self.parse_statement()
                body.addStatement(statement)
        while (self.showNext(0).getType() == "tk_identifier" or self.showNext(0).getType() == "tk_if" or
               self.showNext(0).getType() == "tk_for" or self.showNext(0).getType() == "tk_while" or
               self.showNext(0).getType() == "tk_do"):
            statement = self.parse_statement()
            body.addStatement(statement)
        if (returned_type.getKind().getType() != "tk_typeVoid"): # verifies if the type of the function is void. If not void it must return something
            return_something = True
            try:
                ret = self.expect("tk_return")
                ret = Return(ret)
            except ParserError:
                raise ReturnError("This function has been declared as not void. Make sure it returns something",
                                  self.showNext(0))
            return_expr = self.parse_expression()
            ret.setExpr(return_expr)
            function.setReturnStatement(ret)
            self.expect("tk_linebreak")
            self.parse_linebreaks()

        if (self.showNext(0).getType() == "tk_return" and not return_something):
            ret = self.showNext(0)
            self.accept_it()
            ret = Return(ret)
            return_expr = self.parse_expression()
            ret.setExpr(return_expr)
            function.setReturnStatement(ret)
            self.expect("tk_linebreak")
            self.parse_linebreaks()
        self.expect("tk_end")
        function.addBody(body)

        return function


    def parse_linebreaks(self):
        while (len(self.tkObjectList) > 0 and self.showNext(0).getType() == "tk_linebreak"):
            self.accept_it()

    def parse_declaration(self):
        type = self.parse_type()
        id = self.expect("tk_identifier")
        identifier = Identifier(id)
        if (self.showNext(0).getType() == "tk_lBracket"):
            self.accept_it()
            sz = self.expect("tk_int")
            size = IntLiteral(sz)
            identifier = ArrayType(identifier, size)
            self.expect("tk_rBracket")
        decl = Declaration(type, identifier)
        if (self.showNext(0).getType() == "tk_assign"):
            op, assigned = self.parse_assign_on_declaration()
            decl = Assign(decl, op, assigned) #returned item is an assignment!

        self.expect("tk_linebreak")
        self.parse_linebreaks()

        return decl

    def parse_assign_on_declaration(self):
        op = self.expect("tk_assign")
        expression = self.parse_expression()
        return op, expression

    def parse_type(self):
        if (self.showNext(0).getType() == "tk_typeInt" or self.showNext(0).getType() == "tk_typeFloat" or
                self.showNext(0).getType() == "tk_typeChar" or self.showNext(0).getType() == "tk_typeBoolean" or
                self.showNext(0).getType() == "tk_typeVoid"):
            tok = self.showNext(0)
            self.accept_it()
            return ScalarType(tok)
        else:
            # syntax error
            wrongToken = self.showNext(0)
            raise ParserError("Expecting type int, float, bool or char, got " + wrongToken.getType(), wrongToken)

    def parse_statement(self):
        statement = None
        if (self.showNext(0).getType() == "tk_typeInt" or self.showNext(0).getType() == "tk_typeFloat" or
                self.showNext(0).getType() == "tk_typeBoolean" or self.showNext(0).getType() == "tk_typeChar"):
            statement = self.parse_declaration()
        elif(self.showNext(0).getType() == "tk_identifier"):
            statement = self.parse_assignment()
        elif (self.showNext(0).getType() == "tk_if"):
            statement = self.parse_if()
        elif (self.showNext(0).getType() == "tk_for"):
            statement = self.parse_for()
        elif (self.showNext(0).getType() == "tk_while"):
            statement = self.parse_while()
        elif (self.showNext(0).getType() == "tk_do"):
            statement = self.parse_doWhile()
        else:
            raise ParserError("Illegal statement: '" + self.showNext(0).getValue() + "' ", self.showNext(0))
        self.expect("tk_linebreak")
        self.parse_linebreaks()
        return statement

    def parse_assignment(self):
        id = self.expect("tk_identifier")
        lhs = Identifier(id)
        if (self.showNext(0).getType() == "tk_lBracket"): #array assignment
            self.accept_it()
            index = self.parse_expression()
            lhs = ArrayAccess(lhs, index)
            self.expect("tk_rBracket")

        op = self.expect("tk_assign")
        rhs = self.parse_expression()
        assignment = Assign(lhs, op, rhs)

        return assignment


    def parse_expression(self):
        binConj = None # a binary object to store "or"
        oriBin = None
        conjL = self.parse_conjunction()
        bin = False #specifies if there is a binary object or (or more)
        if (self.showNext(0).getType() == "tk_or"):
            binConj = Binary(self.showNext(0))
            oriBin = binConj #initialise the root
            self.accept_it()
            bin = True
            binConj.addLh(conjL)
            otherConj = self.parse_conjunction()

        while (self.showNext(0).getType() == "tk_or"):
            otherBinConj = Binary(self.showNext(0))
            self.accept_it()
            otherBinConj.addLh(otherConj)
            binConj.addRh(otherBinConj)
            binConj = otherBinConj
            otherConj = self.parse_conjunction()
        if (bin):
            binConj.addRh(otherConj)
        else:
            oriBin = conjL
        return oriBin

    def parse_conjunction(self):
        binEq = None # a binary object to store "and"
        oriBin = None
        eq = self.parse_equality()
        bin = False #specifies if there is a binary object or not
        if (self.showNext(0).getType() == "tk_and"):
            binEq = Binary(self.showNext(0))
            oriBin = binEq
            self.accept_it()
            bin = True
            binEq.addLh(eq)
            otherEq = self.parse_equality()

        while (self.showNext(0).getType() == "tk_and"):
            otherBinEq = Binary(self.showNext(0))
            self.accept_it()
            otherBinEq.addLh(otherEq)
            binEq.addRh(otherBinEq)
            binEq = otherBinEq
            otherEq = self.parse_equality()
        if (bin):
            binEq.addRh(otherEq)
        else:
            oriBin = eq
        return oriBin


    def parse_equality(self):
        e1 = self.parse_relation()
        if (self.showNext(0).getType() == "tk_equal" or self.showNext(0).getType() == "tk_different"):
            binary = Binary(self.showNext(0))
            self.accept_it()
            binary.addLh(e1)
            e2 = self.parse_relation()
            binary.addRh(e2)
            e1 = binary
        return e1

    def parse_relation(self):
        a1 = self.parse_addition()
        if (self.showNext(0).getType() == "tk_lt" or self.showNext(0).getType() == "tk_bt" or self.showNext(
                0).getType() == "tk_le" or self.showNext(0).getType() == "tk_be"):
            binAdd = Binary(self.showNext(0))
            self.accept_it()
            binAdd.addLh(a1)
            a2 = self.parse_addition()
            binAdd.addRh(a2)
            a1 = binAdd
        return a1

    def parse_addition(self):
        binTerm = None
        term = self.parse_term()
        oriBin = None
        bin = False
        if (self.showNext(0).getType() == "tk_plus" or self.showNext(0).getType() == "tk_minus"):
            binTerm = Binary(self.showNext(0))
            oriBin = binTerm
            self.accept_it()
            bin = True
            binTerm.addLh(term)
            otherTerm = self.parse_term()

        while (self.showNext(0).getType() == "tk_plus" or self.showNext(0).getType() == "tk_minus"):
            otherBinTerm = Binary(self.showNext(0))
            self.accept_it()
            otherTerm.addLh(otherTerm)
            binTerm.addRh(otherBinTerm)
            binTerm = otherBinTerm
            otherTerm = self.parse_term()
        if (bin):
            binTerm.addRh(otherTerm)
        else:
            oriBin = term
        return oriBin

    def parse_term(self):
        binFact = None
        fact = self.parse_factor()
        oriBin = None
        bin = False
        if (self.showNext(0).getType() == "tk_mul" or self.showNext(0).getType() == "tk_div" or
                self.showNext(0).getType() == "tk_modulo"):
            binFact = Binary(self.showNext(0))
            oriBin = binFact
            self.accept_it()
            bin = True
            binFact.addLh(fact)
            otherFact = self.parse_factor()

        while (self.showNext(0).getType() == "tk_mul" or self.showNext(0).getType() == "tk_div" or self.showNext(0).getType() == "tk_modulo"):
            otherBinFact = Binary(self.showNext(0))
            self.accept_it()
            otherBinFact.addLh(otherFact)
            binFact.addRh(otherBinFact)
            binFact = otherBinFact
            otherFact = self.parse_factor()
        if (bin):
            binFact.addRh(otherFact)
        else:
            oriBin = fact
        return oriBin

    def parse_factor(self):
        parenthNot = False
        unary = None
        e = None #primary
        isUnary = False
        if (self.showNext(0).getType() == "tk_not"): # NEGATION
            isUnary = True
            parenthNot = True
            un = self.expect("tk_not")
        elif (self.showNext(0).getType() == "tk_minus"):  # NEGATIVE
            isUnary = True
            un = self.expect("tk_minus")

        if (isUnary):   # prefix
            unary = Unary(un)
            if (unary.getTok().getType() == "tk_minus"): # concerns a literal: int or float
                if (self.showNext(0).getType() == "tk_int" or self.showNext(0).getType() == "tk_float" or self.showNext(0).getType() == "tk_identifier" or self.showNext(0).getType() == "tk_lParenth"):
                    e = self.parse_primary()
                    unary.setExpr(e)
                else:
                    raise SyntaxError("Wrong use of an unary operator", unary)
            elif (unary.getTok().getType() == "tk_not"): # concerns a literal: boolean
                if (self.showNext(0).getType() == "tk_boolean" or self.showNext(0).getType() == "tk_identifier" or self.showNext(0).getType() == "tk_lParenth"):
                    e = self.parse_primary()
                    unary.setExpr(e)
                else:
                    raise SyntaxError("Wrong use of an unary operator", unary)

        else:           # no prefix
            unary = self.parse_primary()

        if (parenthNot):
            self.expect("tk_rParenth")

        return unary

    def parse_primary(self):
        primary = None
        if (self.showNext(0).getType() == "tk_identifier"): #identifier
            # Identifier
            id = self.showNext(0)
            primary = Identifier(id)
            self.accept_it()
            if (self.showNext(0).getType() == "tk_lBracket"): #Array
                self.accept_it()
                expression = self.parse_expression()
                primary = ArrayAccess(primary, expression)
                self.expect("tk_rBracket")
            elif (self.showNext(0).getType() == "tk_lParenth"): #function
                self.accept_it()
                primary = FunctionCall(primary)
                if (self.showNext(0).getType() != "tk_rParenth"): #argument(s)
                    argument = self.parse_expression()
                    primary.addArg(argument)
                    while (self.showNext(0).getType() == "tk_comma"):
                        self.accept_it()
                        anotherArgument = self.parse_expression()
                        primary.addArg(anotherArgument)
                self.expect("tk_rParenth")

        elif (self.showNext(0).getType() == "tk_int" or self.showNext(0).getType() == "tk_float" or
              self.showNext(0).getType() == "tk_char" or self.showNext(0).getType() == "tk_string" or
              self.showNext(0).getType() == "tk_boolean"):
            # Literal
            if (self.showNext(0).getType() == "tk_int"):
                primary = IntLiteral(self.showNext(0))
            elif (self.showNext(0).getType() == "tk_float"):
                primary = FloatLiteral(self.showNext(0))
            elif (self.showNext(0).getType() == "tk_char"):
                primary = CharLiteral(self.showNext(0))
            elif (self.showNext(0).getType() == "tk_boolean"):
                primary = BooleanLiteral(self.showNext(0))
            elif (self.showNext(0).getType() == "tk_string"):
                primary = StringLiteral(self.showNext(0))

            self.accept_it()
        elif (self.showNext(0).getType() == "tk_lParenth"): # Parenthesis
            primary = self.parse_parenth()
        elif (self.showNext(0).getType() == "tk_add" or self.showNext(0).getType() == "tk_sub" or
              self.showNext(0).getType() == "tk_mul" or self.showNext(0).getType() == "tk_div"):
            op = self.showNext(0)
            self.accept_it()
            expr = self.parse_expression()
            primary = Unary(op, expr)
        else:
            if (self.showNext(0).getType() == 'tk_linebreak'):
                raise ParserError("Unexpected token: linebreak", self.showNext(0))
            else:
                raise ParserError("Unexpected token: " + self.showNext(0).getValue(), self.showNext(0))
        return primary

    def parse_parenth(self):
        self.expect("tk_lParenth")
        expression = self.parse_expression()
        expression = Parenth(expression)
        self.expect("tk_rParenth")
        return expression


    def parse_if(self):
        ifexpr = self.expect("tk_if")
        if_ = If(ifexpr)
        condition = self.parse_expression()
        self.expect("tk_linebreak")
        self.expect("tk_then")
        self.expect("tk_linebreak")
        self.parse_linebreaks()
        if_.addCondition(condition)
        body = Body()
        while (self.showNext(0).getType() == "tk_identifier" or self.showNext(0).getType() == "tk_if" or
               self.showNext(0).getType() == "tk_for" or self.showNext(0).getType() == "tk_while" or
               self.showNext(0).getType() == "tk_do"):
            try:
                statement = self.parse_statement()
                body.addStatement(statement)
            except ParserError as pe:
                raise ParserError(str(pe))
            while (self.showNext(0).getType() == "tk_else" and self.showNext(1).getType() == "tk_if"):  # else
                elseif = self.parse_else_if()
                if_.addOtherCondition(elseif)
            if (self.showNext(0).getType() == "tk_else"):
                else_ = self.parse_else()
                if_.addElse(else_)
        if_.addBody(body)
        self.expect("tk_end")
        self.expect("tk_if")

        return if_

    def parse_else_if(self):
        self.expect("tk_else")
        self.expect("tk_if")
        elseif = ElseIf(TkObject("tk_elseIf", "sinon si"))
        condition = self.parse_expression()
        elseif.addCondition(condition)
        self.expect("tk_linebreak")
        self.expect("tk_then")
        self.expect("tk_linebreak")
        self.parse_linebreaks()
        body = Body()
        while (self.showNext(0).getType() == "tk_identifier" or self.showNext(0).getType() == "tk_if" or
               self.showNext(0).getType() == "tk_for" or self.showNext(0).getType() == "tk_while" or
               self.showNext(0).getType() == "tk_do"):
            try:
                statement = self.parse_statement()
                body.addStatement(statement)
            except ParserError as pe:
                raise ParserError(str(pe))

        elseif.addBody(body)
        return elseif

    def parse_else(self):
        elseStatement = self.expect("tk_else")
        self.expect("tk_linebreak")
        body = Body()
        while (self.showNext(0).getType() == "tk_identifier" or self.showNext(0).getType() == "tk_if" or
               self.showNext(0).getType() == "tk_for" or self.showNext(0).getType() == "tk_while" or
               self.showNext(0).getType() == "tk_do"):
            try:
                statement = self.parse_statement()
                body.addStatement((statement))
            except ParserError as pe:
                raise ParserError(str(pe))
        else_ = Else(elseStatement, body)

        return else_


    def parse_for(self):
        forStatement = self.expect("tk_for")
        for_ = For(forStatement)
        ref = Identifier(self.expect("tk_identifier"))
        self.expect("tk_from")
        if (self.showNext(0).getType() == "tk_char" or self.showNext(0).getType() == "tk_int" or
                self.showNext(0).getType() == "tk_float" or self.showNext(0).getType() == "tk_string"):
            id = self.showNext(0)
            self.accept_it()
            if (id.getType() == "tk_char"):
               init = CharLiteral(id)
            elif (id.getType() == "tk_int"):
                init = IntLiteral(id)
            elif (id.getType() == "tk_float"):
                init = FloatLiteral(id)
            elif (id.getType() == "tk_string"):
                init = StringLiteral(id)
        self.expect("tk_to")
        limit = self.parse_expression()
        for_.addConfiguration(ref, init, limit)
        self.expect("tk_linebreak")
        self.expect("tk_do")
        self.expect("tk_linebreak")
        self.parse_linebreaks()
        body = Body()
        while (self.showNext(0).getType() == "tk_identifier" or self.showNext(
                0).getType() == "tk_if" or self.showNext(0).getType() == "tk_for" or self.showNext(
            0).getType() == "tk_while" or self.showNext(0).getType() == "tk_do"):
            try:
                statement = self.parse_statement()
                body.addStatement(statement)
            except ParserError as pe:
                raise ParserError(str(pe))
        self.expect("tk_end")
        self.expect("tk_for")
        for_.addBody(body)

        return for_

    def parse_while(self):
        whileStatement = self.expect("tk_while")
        while_ = While(whileStatement)
        condition = self.parse_expression()
        while_.setCondition(condition)
        self.expect("tk_linebreak")
        self.expect("tk_do")
        self.expect("tk_linebreak")
        self.parse_linebreaks()
        body = Body()
        while (self.showNext(0).getType() == "tk_identifier" or self.showNext(0).getType() == "tk_if" or
               self.showNext(0).getType() == "tk_for" or self.showNext(0).getType() == "tk_while" or
               self.showNext(0).getType() == "tk_do"):
            try:
                statement = self.parse_statement()
                body.addStatement(statement)
            except ParserError as pe:
                raise ParserError(str(pe))
        self.expect("tk_end")
        self.expect("tk_while")
        while_.setBody(body)

        return while_

    def parse_doWhile(self):
        doWhileStatement = self.expect("tk_do")
        doWhile = DoWhile(doWhileStatement)
        self.expect("tk_linebreak")
        body = Body()
        while (self.showNext(0).getType() == "tk_identifier" or self.showNext(0).getType() == "tk_if" or
               self.showNext(0).getType() == "tk_for" or self.showNext(0).getType() == "tk_do"):
            try:
                statement = self.parse_statement()
                body.addStatement(statement)
            except ParserError as pe:
                raise ParserError(str(pe))
        self.expect("tk_while")
        condition = self.parse_expression()
        doWhile.addBody(body)
        doWhile.addCondition(condition)

        return doWhile
