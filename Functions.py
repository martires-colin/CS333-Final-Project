import os
import shutil

from TokenParser import TokenParser


class DB_Functions():

    def __init__(self):
        self.parser = TokenParser()

    # return "Invalid Command", may add "correct usage" text later
    def invalidCommand(self):
        return "[ERROR] Invalid Command"

    # CREATE DATABASE
    # create DB if not already created
    def createDB(self, tokens, home_dir):
        if not self.parser.isValidCommand(tokens[-1]):
            print(self.invalidCommand())
            return "ERROR"

        db = tokens[2][:-1]
        path = f'{home_dir}/{db}'

        if os.path.exists(path):
            print(f"[ERROR] Database {db} already exists!")
            return False
        else:
            os.makedirs(path)
            print(f'Created database: {db}')
            return True

    # DROP DATABASE
    # drop DB if it exists
    def dropDB(self, tokens, home_dir):
        if not self.parser.isValidCommand(tokens[-1]):
            print(self.invalidCommand())
            return "ERROR"

        db = tokens[2][:-1]
        path = f'{home_dir}/{db}'

        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                print(f'Dropped database: {db}')
                return db
            except OSError as e:
                print(f'[ERROR] {e.filename} - {e.strerror}')
        else:
            print(f"[ERROR] Database {db} does not exist!")
            return f"[ERROR] Database {db} does not exist!"

    # USE DB
    # point cwd to DB
    def useDB(self, tokens, home_dir):
        if not self.parser.isValidCommand(tokens[-1]):
            print(self.invalidCommand())
            return "ERROR"

        db = tokens[1][:-1]
        path = f'{home_dir}/{db}'

        if os.path.exists(path):
            os.chdir(path)
            print(f'Using {db}')
            return db
        else:
            print(f"[ERROR] Database {db} does not exist!")
            return f"[ERROR] Database {db} does not exist!"

    # SHOW DBS
    # show available databases
    def showDBs(self, home_dir):
        print(home_dir)
        results = os.listdir(home_dir)
        for res in results:
            # print(res)
            if os.path.isdir(os.path.join(home_dir, res)):
                print(res)

    # SHOW TABLES
    # show available tables
    def showTables(self):
        results = os.listdir(os.getcwd())
        for res in results:
            if os.path.isfile(res):
                print(res)

    # CREATE TABLE
    # create Table, if not already created, with specified input
    def createTable(self, tokens):
        if not self.parser.isValidCommand(tokens[-1]):
            print(self.invalidCommand())
            return "ERROR"
        
        table = tokens[2]
        args = tokens[3][1:-2]
        arg_tokens = args.replace(", ", " | ")

        path = f'{os.getcwd()}/{table}'

        if os.path.exists(path):
            print(f"[ERROR] Table {table} already exists!")
            return False
        else:
            with open(path, 'a') as fp:
                fp.write(arg_tokens)
            print(f'Created table: {table}')
            return True

    # DROP TABLE
    # drop table if it exists
    def dropTable(self, tokens):
        if not self.parser.isValidCommand(tokens[-1]):
            print(self.invalidCommand())
            return "ERROR"
        
        table = tokens[2][:-1]
        path = f'{os.getcwd()}/{table}'

        if os.path.exists(path):
            os.remove(path)
            print(f'Dropped table: {table}')
            return True
        else:
            print(f"[ERROR] Table {table} does not exist!")
            return f"[ERROR] Table {table} does not exist!"

    # SELECT FROM TABLE
    # print out contents of table
    def select(self, tokens):
        if not self.parser.isValidCommand(tokens[-1]):
            print(self.invalidCommand())
            return "ERROR"

        table = tokens[3][:-1]
        path = f'{os.getcwd()}/{table}'

        if os.path.exists(path):
            f = open(path, "r")
            for lines in f:
                print(lines)
            return True
        else:
            print(f"[ERROR] Table {table} does not exist!")
            return f"[ERROR] Table {table} does not exist!"

    # ALTER TABLE
    # modify table
    def alterTable(self, tokens):
        if not self.parser.isValidCommand(tokens[-1]):
            print(self.invalidCommand())
            return "ERROR"

        table = tokens[2]
        method = tokens[3]
        newEntry = f" | {tokens[4]} {tokens[5][:-1]}"
        path = f'{os.getcwd()}/{table}'

        if method == "ADD":
            if os.path.exists(path):
                with open(path, 'a') as fp:
                    fp.write(newEntry)
                print(f'Altering Table: {table}')
                return True
            else:
                print(f"[ERROR] Table {table} does not exist!")
                return f"[ERROR] Table {table} does not exist!"