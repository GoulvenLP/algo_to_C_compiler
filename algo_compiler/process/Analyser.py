import sys
import os
parentPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('../')
from tkobject.TkObject import TkObject
from colorama import Fore, Style
import re
from errors.ParserError import ParserError
from errors.ReturnError import ReturnError

class Analyser:

    def __init__(self, filename):
        self.filename = filename
        self.tkObjectList = []
        self.referenceList = []

        self.loadReferenceList()


    def loadReferenceList(self) -> None:
        """
            Adds all tokens to the reference list. The reference list contains all the required tokens to recognize
            the 'legal' code
        """
        self.referenceList.append(TkObject('tk_plus', r'^\+'))
        self.referenceList.append(TkObject('tk_minus', '-'))
        self.referenceList.append(TkObject('tk_then', r'^alors'))
        self.referenceList.append(TkObject('tk_from', r'^de '))
        self.referenceList.append(TkObject('tk_to', '^à'))
        self.referenceList.append(TkObject('tk_mul', r'^\*'))
        self.referenceList.append(TkObject('tk_div', r'^/'))
        self.referenceList.append(TkObject('tk_modulo', r'^%'))
        self.referenceList.append(TkObject('tk_lBracket', r'^\['))
        self.referenceList.append(TkObject('tk_rBracket', r'^\]'))
        self.referenceList.append(TkObject('tk_or', r'^ou'))
        self.referenceList.append(TkObject('tk_and', r'^et'))
        self.referenceList.append(TkObject('tk_lParenth', r'^\('))
        self.referenceList.append(TkObject('tk_rParenth', r'^\)'))
        self.referenceList.append(TkObject('tk_linebreak', r'\n'))
        self.referenceList.append(TkObject('tk_assign', r'^<-'))
        self.referenceList.append(TkObject('tk_le', r'^<='))
        self.referenceList.append(TkObject('tk_lt', r'^<'))
        self.referenceList.append(TkObject('tk_be', r'^>='))
        self.referenceList.append(TkObject('tk_bt', r'^>'))
        self.referenceList.append(TkObject('tk_different', r'^!='))
        self.referenceList.append(TkObject('tk_equal', r'^='))
        self.referenceList.append(TkObject('tk_space', r'[\s\t]+'))
        self.referenceList.append(TkObject('tk_beginFunction', r'd[eé]but'))
        self.referenceList.append(TkObject('tk_return', r'^retourner'))
        self.referenceList.append(TkObject('tk_else', r'^sinon'))
        self.referenceList.append(TkObject('tk_not', r'^non\('))
        self.referenceList.append(TkObject('tk_if', r'^si'))
        self.referenceList.append(TkObject('tk_elseIf', r'^sinon si'))
        self.referenceList.append(TkObject('tk_while', r'^tant que'))
        self.referenceList.append(TkObject('tk_do', r'^faire'))
        self.referenceList.append(TkObject('tk_for', r'^pour'))
        self.referenceList.append(TkObject('tk_end', r'^fin'))
        self.referenceList.append(TkObject('tk_typeInt', r'^entier'))
        self.referenceList.append(TkObject('tk_typeFloat', r'^flottant'))
        self.referenceList.append(TkObject('tk_typeChar', r'^car'))
        self.referenceList.append(TkObject('tk_typeBoolean', r'^booléen'))
        self.referenceList.append(TkObject('tk_typeVoid', r'^rien'))
        self.referenceList.append(TkObject('tk_float', r'[0-9]+\.[0-9]*'))
        self.referenceList.append(TkObject('tk_int', r'[0-9]+'))
        self.referenceList.append(TkObject('tk_boolean', r'vrai|faux'))
        self.referenceList.append(TkObject('tk_char', r'\'[a-zA-Z0-9]\''))
        self.referenceList.append(TkObject('tk_string', r'\"[a-zA-Z0-9\',;:! \#\*]*\"'))
        self.referenceList.append(TkObject('tk_comma', r'^,'))
        self.referenceList.append(TkObject('tk_colon', r'^:'))
        self.referenceList.append(TkObject('tk_identifier', r'[a-zA-Z0-9_]+'))


    def extractContent(self) -> str:
        """ Extracts the whole content of a file and returns the result as a single String """
        try:
            f = open(self.filename, "r")
            fileContent = f.readlines()
            gatheredContent = ''
            for line in fileContent:
                gatheredContent += line
            f.close()
            return gatheredContent
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {self.filename} was not found")
        except ParserError as pe:
            raise Exception(str(pe))
        except ReturnError as re:
            raise Exception(str(re))



    def removeSpaces(self) -> None:
        """ Parses the tkObjectList and removes any space into it by creating a new list TkObject list without
            any spaces and assigning it to the tkObjectList
        """
        updatedList = []
        for tkObj in self.tkObjectList:
            if tkObj.getType() != 'tk_space':
                updatedList.append(tkObj)
        self.tkObjectList = updatedList


    def lexer(self) -> None:
        readContent = self.extractContent() # load the content to parse
        numLine = 1
        numColumn = 1
        exit = False
        while (not exit): # loop until the whole content of readContent is parsed
            found = False
            indice = 0
            for item in self.referenceList: # goal: compare all the declared TkObjects to the string to parse, to classify each item.
                indice += 1
                isMatching = re.match(item.getValue(), readContent)
                if (isMatching): # matching token found
                    tkObject = TkObject(item.getType(), isMatching.group()) #create an object with the matching pattern
                    tkObject.addCoordinates(numLine, numColumn)
                    self.tkObjectList.append(tkObject)
                    if (item.getType() == 'tk_linebreak'): # special update if linebreak: increment line, reset column
                        numLine += 1
                        numColumn = 1
                    else: # standard update: set the new coordinates on the line
                        numColumn += len(isMatching.group())
                    found = True # a pattern matched: signal it
                    break # leave the for loop so that the 'readContent' string is updated

            if(found): # when a pattern matches: remove the found pattern from the sequence to treat
                readContent = readContent[ len(isMatching.group()):]
            else:
                raise Exception("A lexem was not recognized line " + str(numLine) + " after column " + str(numColumn))

            if (len(readContent) == 0): # once the whole text to parse got parsed, the function can come to an end
                exit = True
        print(Fore.CYAN + "File successfully parsed" + Style.RESET_ALL) # display a message to confirm the success of the parsing

    def getTkObjectList(self):
        """ Gets the whole list of TkObjects made from the text"""
        return self.tkObjectList
