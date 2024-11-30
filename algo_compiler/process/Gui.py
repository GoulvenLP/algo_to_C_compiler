import time
from colorama import Fore, Style
from Main import Main
from AST.Strategies import Strategies # enum
from errors.ParserError import ParserError


class GUI():

    def __init__(self):
        self.endpoint = Main()
    def hall(self):
        """ Displays the loading screen """
        print(Fore.YELLOW + "===============ALGO COMPILER===============" + Fore.RESET)
        print("             " + Fore.LIGHTWHITE_EX + "by Goulven Le Pennec, May 2024")

    def hallChoice(self):
        """ Displays the possible choices related to the launch of a new file """
        print(Fore.BLUE + "[1]" + Fore.RESET + " Load a file      " + Fore.BLUE + "[2]" + Fore.RESET + " Leave")

    def wrongInput(self):
        """ Displays an error message """
        print(Fore.RED + "Your input is not valid. Please try again" + Fore.RESET)

    def loadFile(self):
        """ Loads a file. If the file does not exist, displays an error message """
        filename = input("Enter your filename (By default all files are stored in " + Fore.GREEN + "'submittedFiles/'" + Fore.RESET + ") : ")
        filename = "../submittedFiles/" + filename
        try:
            self.endpoint.loadFile(filename)
        except FileNotFoundError:
            print(Fore.RED + filename + "' could not be found. Verify its path and that you typed its name correctly" +
                  Fore.RESET)
            self.hallChoice()
            try:
                self.loadFile()
            except ParserError as pe2:
                print(Fore.RED + str(pe2) + Fore.RESET)
        except Exception as exc:
            print(Fore.RED + str(exc) + Fore.RESET)
            self.hallChoice()
            try:
                self.loadFile()
            except ParserError as pe2:
                print(Fore.RED + str(pe2) + Fore.RESET)

    def makeChoice(self):
        """ Displays a message to tell the user how to use the GUI with the number choices"""
        print("Enter the " + Fore.BLUE + "key" + Fore.RESET + " number corresponding to your choice:")

    def availableStrategies(self):
        """ Displays the available strategies (different modes) """
        print( Fore.BLUE + "[1]" + Fore.RESET + " Pretty printer       " + Fore.BLUE + "[2]" + Fore.RESET +
               " C language conversion       " + Fore.BLUE + "[3]" + Fore.RESET + " Leave")

    def availableFunctionalities(self):
        """ Displays the available functionalities """
        print ( Fore.BLUE + "[1]" + Fore.RESET + " Display code         " + Fore.BLUE + "[2]" + Fore.RESET +
                " Save code       " + Fore.BLUE + "[3]" + Fore.RESET + " Change mode\n" +
                Fore.BLUE + "[4]" + Fore.RESET + " Load another file        " + Fore.BLUE + "[5]" + Fore.RESET + " Leave")

    def leave(self):
        """ Definitely leaves the application """
        print(Fore.YELLOW + "See you next time!" + Fore.RESET)
        time.sleep(1)

    def setStrategy(self, strat: Strategies):
        """ Sets a strategy """
        self.endpoint.setStrategy(strat)

    def loadIntro(self) -> int:
        """
            displays the program, returns an integer corresponding to the key number chosen by the user. By default the
             choice to leave is assigned to 0 (zero)
        """
        isValid = False
        while (not isValid):  # loop until a valid choice is made
            choice = input()
            if (choice.isdigit()):  # input is a digit
                choice = int(choice)
                if (choice >= 1 and choice <= 2):  # valid choice
                    isValid = True
                else:
                    self.wrongInput()
            else:
                self.wrongInput()
        if (choice == 1): # load file
            self.loadFile()
        else: # leave
            choice = 0
            self.leave()
        return choice

    def execute(self):
        self.endpoint.execute()
    def loadModes(self) -> int:
        """
            Loads the differents modes of the program, returns an integer corresponding to the choice made.
            the choice to leave is reassigned to 0 so that in the whole program, 0 means leaving.
        """
        isValid = False # decision variable
        while (not isValid):
            print("How do you want to treat your data?")
            self.availableStrategies()
            choice = input()
            if (choice.isdigit()): # input is a digit
                choice = int(choice)
                if (choice >=1 and choice <=3): # digit is a valid digit
                    isValid = True
                else:
                    gui.wrongInput()
            else:
                gui.wrongInput()
        if (choice == 1): # pretty printer
            self.setStrategy(Strategies.PRETTYPRINTER)
            self.execute()
            print(Fore.MAGENTA + "Pretty Printer enabled" + Fore.RESET)
        elif (choice == 2): # convert to c
            self.setStrategy(Strategies.CCONVERTER)
            self.execute()
            print(Fore.MAGENTA + "C converter enabled" + Fore.RESET)
        elif (choice == 3): # leave
            choice = 0  # leaving code is 0 by convention
            self.leave()
        return choice

    def loadFunctionality(self) -> int:
        """
            displays the possible functionalities of the program with four choices, returns the number of the key
            associated with the valid choice made. The key number related to the chosen functionality is returned.
            The number associated to leaving the app is assigned to zero (0).
        """
        isValid = False  # decision variable
        while (not isValid):
            gui.availableFunctionalities()
            choice = input()
            if (choice.isdigit()):  # input is a digit
                choice = int(choice)
                if (choice >= 1 and choice <= 5):  # digit is a valid digit
                    isValid = True
                else:
                    self.wrongInput()
            else:
                self.wrongInput()
        if (choice == 1): # display code
            print(Fore.CYAN + "----------------------------------------------------------------------------" + Fore.RESET)
            self.endpoint.display()
            print(Fore.CYAN + "----------------------------------------------------------------------------" + Fore.RESET)
        elif (choice == 2): # save
            destFile = input("Please enter your destination file (by default the destination folder is " +
                             Fore.GREEN + "'createdFiles/'" + Fore.RESET + ") : ")
            (self.endpoint.save(destFile))
        elif (choice == 3): # change mode
            choice = self.loadModes()
        elif (choice == 4):  # load another file
            choice = self.loadFile()
            if (choice != 0):
                choice = self.loadModes()
        elif (choice == 5): # leave
            choice = 0 # leaving code is 0 by convention
            self.leave()
        return choice


if __name__ == "__main__":
    gui = GUI()
    gui.hall()
    gui.hallChoice()
    gui.makeChoice()

    nextStep = gui.loadIntro() #loadfile
    if (nextStep != 0):
        nextStep = gui.loadModes() #chose strategy
    if (nextStep != 0):
        while (nextStep != 0): # == leave
            nextStep = gui.loadFunctionality()



