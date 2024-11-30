from AST.Context import Context
from Analyser import Analyser
from Parser import Parser
from AST.Strategies import Strategies #enumeration
from AST.Visitor import Visitor
from Saver import Saver
from errors.ParserError import ParserError

class Main:

    def __init__(self):
        self.context = Context()
        self.astTree = None

    def loadFile(self, filename):
        try:
            analyser = Analyser(filename)
            analyser.lexer()
            analyser.removeSpaces()
            list = analyser.getTkObjectList()
            p = Parser(list)
            self.astTree = p.parse_program()
        except FileNotFoundError:
            raise FileNotFoundError(f"file {filename} not found")
        except ParserError as pe:
            raise Exception(str(pe))

    def setStrategy(self, strategy: Strategies):
        self.context.setStrategy(strategy)

    def getStrategy(self):
        return self.context.getStrategy()

    def execute(self):
        self.context.execute(self.astTree)

    def save(self, dest):
        if (type(self.getStrategy()) == Visitor):
            print("The pattern Visitor has not been implemented for any save.")
        else:
            save = Saver(self.context.getCode(), dest)
            save.saveIntoFile()

    def display(self):
        if (type(self.getStrategy()) == Visitor):
            self.context.execute()
        else:
            self.context.displayCode()


# if __name__ == "__main__":
#     filename = '../testfiles/error6.txt' #CHOIX DU FICHIER À LIRE
#     program = Main()
#     try:
#         program.loadFile(filename)
#     except ParserError as exc:
#         print(str(exc))
#     # program.setStrategy(Strategies.VISITOR)
#     # program.execute()
#     #
#     # # ------------ PRETTY PRINTER ------------
#     # program.setStrategy(Strategies.PRETTYPRINTER)
#     program.execute()
#     program.display()
#     # program.save("save8_pretty.txt")
#
#     # # ------------ C CONVERTER ------------
#     # program.setStrategy(Strategies.CCONVERTER)
#     # program.execute()
#     # program.display()
#     #program.save("save8_C.c")
