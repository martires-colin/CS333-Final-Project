import os
import shutil


class TokenParser():

    # split the user command into tokenized arguments
    def getTokens(self, user_cmd):
        return user_cmd.split(" ")

    # special parsing for createTable command
    def getTokensCreateTable(self, user_cmd):
        return user_cmd.split(" ", 3)

    # return number of args
    def getNumArgs(self, user_cmd):
        tokens = user_cmd.split(" ")
        return len(tokens)
        # return len(tokens) + 1

    # checks if command ends with ";"
    def isValidCommand(self, arg):
        return True if arg[-1] == ";" else False