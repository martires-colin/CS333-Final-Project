# CS333 Final Project
CS333 Testing and DevOps Final Project

## Technologies Used

* Testing Framework

    * Python unittest

* Source Control

    * GitHub

* Package Deployment

    * PyPi

* Automated Testing and Deployment

    * GitHub Actions

## CS457 Programming Assignment 1: Metadata Management

Author: Colin Martires

Date: 2/13/2023

## Prerequisites

* Python 3.10.6

* Modules used:

    * os
    * shutil

## Usage
* Run main.py

    `python3 main.py`

* To create a database

    `CREATE DATABASE <database name>;`

* To delete a database

    `DROP DATABASE <database name>;`

* To use a database

    `USE <database name>;`

* To create a table

    `CREATE TABLE <table name> <input parameters>;`

* To delete a table

    `DROP TABLE <table name>;`

* To select from a table

    `SELECT <query> FROM <table name>;`

* To modify a table

    `ALTER TABLE <table name> <ADD> <parameters>;`

* To exit the program

    `.EXIT`

## Function Descriptions

* `invalidCommand()`

    Prints an error if the user has entered a command that is not recognized by the system.
    I made this a separate function in case I wanted to include a "Correct Usage" guide to
    let the user know of the valid commands.

    ```
    def invalidCommand():
        print("[ERROR] Invalid Command")
    ```

* `isValidCommand(arg)`

    Takes a string as a paramenter. Returns true if that string ends with ";" and false otherwise.

    ```
    def isValidCommand(arg):
        return True if arg[-1] == ";" else False
    ```

* `createDB(tokens, home_dir)`

    Takes tokenized arguments from the user input as well as a string representing the user's home directory.
    The function first validates the command using `isValidCommand()`. It then creates a file path by
    concatenating the user's home directory path with the name of the new database.
    If the directory already exists, an error is printed to the screen.
    The home directory is used so the user can create a new database even if they are currently using one.

    ```
    def createDB(tokens, home_dir):
        if not isValidCommand(tokens[-1]):
            invalidCommand()
            return

        db = tokens[2][:-1]
        path = f'{home_dir}/{db}'

        if os.path.exists(path):
            print("[ERROR] Database already exists!")
        else:
            os.makedirs(path)
            print(f'Created database: {db}')
    ````

* `dropDB(tokens, home_dir)`
    
    Takes tokenized arguments from the user input as well as a string representing the user's home directory.
    The function first validates the command using `isValidCommand()`. It then checks if the specifed
    database exists as a folder. If the folder exists, then it is deleted using `shutil.rmtree()`. If the folder does
    not exist, an error is printed to the screen.

    ```
    def dropDB(tokens, home_dir):
        if not isValidCommand(tokens[-1]):
            invalidCommand()
            return

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
            print("[ERROR] Database does not exist!")
    ```

* `useDB(tokens, home_dir)`

    Takes tokenized arguments from the user input as well as a string representing the user's home directory.
    The function first validates the command using `isValidCommand()`. It then checks if the specified
    database exists as a folder. If the folder exists, the system changes its working directory using `os.chdir()`.

    ```
    def useDB(tokens, home_dir):
        if not isValidCommand(tokens[-1]):
            invalidCommand()
            return

        db = tokens[1][:-1]
        path = f'{home_dir}/{db}'

        if os.path.exists(path):
            os.chdir(path)
            print(f'Using {db}')
            return db
        else:
            print("[ERROR] Database does not exist!")
    ```

* `showDBs(home_dir)`
    
    Takes a string representing the user's home directory. The function prints all the folders (databases) that
    exist in the user's home directory using `os.listdir()`.

    ```
    def showDBs(home_dir):
        print(home_dir)
        results = os.listdir(home_dir)
        for res in results:
            # print(res)
            if os.path.isdir(os.path.join(home_dir, res)):
                print(res)
    ```

* `showTables()`

    The function prints all the files (tables) that exist within a certain directory (database).

    ```
    def showTables():
        results = os.listdir(os.getcwd())
        for res in results:
            if os.path.isfile(res):
                print(res)
    ```

* `createTable(tokens)`

    Takes tokenized arguments from the user input.
    The function first validates the command using `isValidCommand()`. It then checks if the table already exists
    in the database. If the file does not exist, it is created.

    ```
    def createTable(tokens):
        if not isValidCommand(tokens[-1]):
            invalidCommand()
            return
        
        table = tokens[2]
        args = tokens[3][1:-2]
        arg_tokens = args.replace(", ", " | ")

        path = f'{os.getcwd()}/{table}'

        if os.path.exists(path):
            print("[ERROR] Table already exists!")
        else:
            with open(path, 'a') as fp:
                fp.write(arg_tokens)
            print(f'Created table: {table}')
    ```

* `dropTable(token)`

    Takes tokenized arguments from the user input.
    The function first validates the command using `isValidCommand()`. It then checks if the table exists in the
    database. If the table exists, it is deleted using `os.remove()`.

    ```
    def dropTable(tokens):
        if not isValidCommand(tokens[-1]):
            invalidCommand()
            return
        
        table = tokens[2][:-1]
        path = f'{os.getcwd()}/{table}'

        if os.path.exists(path):
            os.remove(path)
            print(f'Dropped table: {table}')
        else:
            print("[ERROR] Table does not exist!")
    ```

* `select(tokens)`

    Takes tokenized arguments from the user input.
    The function first validates the command using `isValidCommand()`. It then checks if the table exists in the
    database. If the table exists, the contents of the file are printed to the screen.

    ```
    def select(tokens):
        if not isValidCommand(tokens[-1]):
            invalidCommand()
            return

        table = tokens[3][:-1]
        path = f'{os.getcwd()}/{table}'

        if os.path.exists(path):
            f = open(path, "r")
            for lines in f:
                print(lines)
        else:
            print("[ERROR] Table does not exist!")
    ```

* `alterTable(tokens)`

    Takes tokenized arguments from the user input.
    The function first validates the command using `isValidCommand()`. If the method is "ADD", the function will
    add the specifed parameters to the table indicated in the command.

    ```
    def alterTable(tokens):
        if not isValidCommand(tokens[-1]):
            invalidCommand()
            return

        table = tokens[2]
        method = tokens[3]
        newEntry = f" | {tokens[4]} {tokens[5][:-1]}"
        path = f'{os.getcwd()}/{table}'

        if method == "ADD":
            if os.path.exists(path):
                with open(path, 'a') as fp:
                    fp.write(newEntry)
                print(f'Altering Table: {table}')
            else:
                print("[ERROR] Table does not exist!")
    ```

* `main()`

    The main function processes the user's input and executes different functions based on the tokens recevied from parsing the input. The function also keeps track of the current database so the user can know which database they are accessing at a given time.

## Sample Output

```
> Created database: db_1
> [ERROR] Database db_1 already exists!
> Created database: db_2
> Dropped database: db_2
> [ERROR] Database db_2 does not exist!
> Created database: db_2
> Using db_1
db_1> Created table: tbl_1
db_1> [ERROR] Table tbl_1 already exists!
db_1> Dropped table: tbl_1
db_1> [ERROR] Table tbl_1 does not exist!
db_1> Created table: tbl_1
db_1> a1 int | a2 varchar(20)
db_1> Altering Table: tbl_1
db_1> a1 int | a2 varchar(20) | a3 float
db_1> Created table: tbl_2
db_1> a3 float | a4 char(20)
db_1> Using db_2
db_2> [ERROR] Table tbl_1 does not exist!
db_2> Created table: tbl_1
db_2> a3 float | a4 char(20)
db_2> Closing Program
```