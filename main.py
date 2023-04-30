"""
Colin Martires
CS333 Testing and DevOps
Final Project
Date: 4/29/2023

Project used:
CS 457 Database Management Systems
Programming Assignment 1: Metadata Management
Date: 2/13/2023
"""

import os
import shutil
from Functions import DB_Functions
from TokenParser import TokenParser

def main():

    functions = DB_Functions()
    parser = TokenParser()

    home_dir = os.getcwd()
    curr_db = None
    
    try:
        # execute loop until user decides to exit program
        while(True):

            # if database is in use, display with input line
            if curr_db:
                userInput = input(f"{curr_db}> ")
            else:
                userInput = input(f"> ")

            tokens = parser.getTokens(userInput)
            num_tokens = parser.getNumArgs(userInput)
            
            # if userInput contains 1 command
            if num_tokens == 1:
                # ".EXIT" command
                if tokens[0].upper() == ".EXIT":
                    print("Closing Program")
                    return
                else:
                    print(functions.invalidCommand())

            # if userInput contains 2 commands
            elif num_tokens == 2:
                # "USE <db>" command
                if tokens[0] == "USE":
                    curr_db = functions.useDB(tokens, home_dir)
                elif tokens[0].upper() == "SHOW":
                    # "SHOW DBS" command
                    if tokens[1].upper() == "DBS":
                        functions.showDBs(home_dir)
                    # "SHOW TABLES" command
                    elif tokens[1].upper() == "TABLES":
                        functions.showTables()
                    else:
                        print(functions.invalidCommand())
                else:
                    print(functions.invalidCommand())

             # if userInput contains 3 commands 
            elif num_tokens == 3:
                # "CREATE DATABASE" command
                if tokens[0] == "CREATE":
                    if tokens[1] == "DATABASE":
                        functions.createDB(tokens, home_dir)
                    else:
                        print(functions.invalidCommand())
                elif tokens[0] == "DROP":
                    # "DROP DATABASE" command
                    if tokens[1] == "DATABASE":
                        dropped_db = functions.dropDB(tokens, home_dir)
                        if dropped_db == curr_db:
                            os.chdir(home_dir)
                            curr_db = None
                    # "DROP TABLE" command
                    elif tokens[1] == "TABLE":
                        functions.dropTable(tokens)
                    else:
                        print(functions.invalidCommand())
                else:
                    print(functions.invalidCommand())
                    
            # if userInput contains at least 4 commands
            elif num_tokens >= 4:
                # "CREATE TABLE" command
                if tokens[0] == "CREATE" and tokens[1] == "TABLE":
                    parsed_input = parser.getTokensCreateTable(userInput)
                    functions.createTable(parsed_input)
                # "SELECT" command
                elif tokens[0] == "SELECT" and tokens[2] == "FROM":
                    functions.select(tokens)
                # "ALTER TABLE" command
                elif tokens[0] == "ALTER" and tokens[1] == "TABLE":
                    functions.alterTable(tokens)
                else:
                    print(functions.invalidCommand())

            # userInput was an invalid command
            else:
                print(functions.invalidCommand())
    
    # handle keyboard interrupt 
    except KeyboardInterrupt:
        print("\nExiting Program")


if __name__ == "__main__":
    main()