from colorama import Fore, Style

class Saver:
    def __init__(self, someCode: str, dest: str):
        self.dest = dest
        self.concatDest = "../createdFiles/" + dest
        self.code = someCode

    def saveIntoFile(self):
        try:
            f = open(self.concatDest, "w")
            f.write(self.code)
            f.close

            print(Fore.MAGENTA + "The file \'" + self.dest + "\' was successfully created with some formatting!"
                  + Style.RESET_ALL)
        except:
            raise FileNotFoundError("The file \'" + self.dest + "\' could not be found")

