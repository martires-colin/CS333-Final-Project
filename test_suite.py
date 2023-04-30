# Colin Martires
# CS333 Testing and DevOps
# Final Project
# 4/29/2023

import unittest
import shutil
import os
from Functions import DB_Functions
from TokenParser import TokenParser

# DB Functions Module Unit Tests
class TestDB_Functions(unittest.TestCase):
    
    def setUp(self):
        self.functions = DB_Functions()

    def tearDown(self):
        os.chdir(".")
        if os.path.exists(os.getcwd() + "/test_dir"):
            try:
                shutil.rmtree(os.getcwd() + "/test_dir")
            except OSError as oserr:
                print(oserr)

    def test_invalidCommand_returns_correct_message(self):
        self.assertEqual(self.functions.invalidCommand(), "[ERROR] Invalid Command")

    def test_createDB_successfully_creates_DB(self):
        test_tokens = ["CREATE", "DATABASE", "test_db;"]
        test_dir = os.getcwd() + "/test_dir"
        self.assertTrue(self.functions.createDB(test_tokens, test_dir))

    def test_new_DB_in_correct_directory(self):
        test_tokens = ["CREATE", "DATABASE", "test_db;"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens, test_dir)
        self.assertTrue(os.path.exists(os.getcwd() + "/test_dir/test_db"))

    def test_createDB_doesnt_create_duplicate_DB(self):
        test_tokens = ["CREATE", "DATABASE", "test_db;"]
        test_dir = os.getcwd() + "/test_dir"
        self.assertTrue(self.functions.createDB(test_tokens, test_dir))
        self.assertFalse(self.functions.createDB(test_tokens, test_dir))

    def test_createDB_catches_invalid_command(self):
        test_tokens = ["CREATE", "DATABASE", "test_db"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens, test_dir)
        self.assertFalse(os.path.exists(os.getcwd() + "/test_dir/test_db"))
        self.assertEqual(self.functions.createDB(test_tokens, test_dir), "ERROR")

    def test_dropDB_successfully_deletes_DB(self):
        test_tokens = ["DROP", "DATABASE", "test_db;"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens, test_dir)
        self.assertEqual(self.functions.dropDB(test_tokens, test_dir), "test_db")

    def test_folder_was_successfully_deleted(self):
        test_tokens = ["DROP", "DATABASE", "test_db;"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens, test_dir)
        self.functions.dropDB(test_tokens, test_dir)
        self.assertFalse(os.path.exists(os.getcwd() + "/test_dir/test_db"))

    def test_dropDB_returns_correct_error_message(self):
        test_tokens = ["DROP", "DATABASE", "test_db;"]
        test_dir = os.getcwd() + "/test_dir"
        self.assertEqual(self.functions.dropDB(test_tokens, test_dir), "[ERROR] Database test_db does not exist!")

    def test_dropDB_catches_invalid_command(self):
        test_tokens = ["DROP", "DATABASE", "test_db"]
        test_dir = os.getcwd() + "/test_dir"
        self.assertEqual(self.functions.dropDB(test_tokens, test_dir), "ERROR")

    def test_useDB_changes_to_correct_working_directory(self):
        cur_cwd = os.getcwd()
        test_dir = cur_cwd + "/test_dir"
        test_tokens = ["CREATE", "DATABASE", "test_db;"]
        self.functions.createDB(test_tokens, test_dir)
        test_tokens = ["USE", "test_db;"]
        self.assertEqual(self.functions.useDB(test_tokens, test_dir), "test_db")
        os.chdir(cur_cwd)

    def test_useDB_returns_correct_error_message(self):
        cur_cwd = os.getcwd()
        test_dir = cur_cwd + "/test_dir"
        test_tokens = ["CREATE", "DATABASE", "test_db;"]
        test_tokens = ["USE", "test_db;"]
        self.assertEqual(self.functions.useDB(test_tokens, test_dir), "[ERROR] Database test_db does not exist!")
        os.chdir(cur_cwd)
        
    def test_useDB_catches_invalid_command(self):
        cur_cwd = os.getcwd()
        test_dir = cur_cwd + "/test_dir"
        test_tokens = ["CREATE", "DATABASE", "test_db;"]
        self.functions.createDB(test_tokens, test_dir)
        test_tokens = ["USE", "test_db"]
        self.assertEqual(self.functions.useDB(test_tokens, test_dir), "ERROR")
        os.chdir(cur_cwd)

    def test_createTable_successfully_creates_Table(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.assertTrue(self.functions.createTable(test_tokens_createTable))
        os.chdir(cur_cwd)

    def test_createTable_contents(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        f = open(test_dir + "/test_db/tbl_1", "r")
        self.assertEqual(f.readline(), "a1 int | a2 varchar(20)")
        f.close()
        os.chdir(cur_cwd)

    def test_new_table_in_correct_DB(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.assertTrue(os.path.exists("tbl_1"))
        os.chdir(cur_cwd)

    def test_createTable_doesnt_create_duplicate_DB(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.assertFalse(self.functions.createTable(test_tokens_createTable))
        os.chdir(cur_cwd)

    def test_createTable_catches_invalid_command(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20))"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.assertEqual(self.functions.createTable(test_tokens_createTable), "ERROR")
        os.chdir(cur_cwd)

    def test_dropTable_successfully_deletes_Table(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        test_tokens_dropTable = ["DROP", "TABLE", "tbl_1;"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.assertTrue(self.functions.dropTable(test_tokens_dropTable))
        os.chdir(cur_cwd)

    def test_file_was_successfully_deleted(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        test_tokens_dropTable = ["DROP", "TABLE", "tbl_1;"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.functions.dropTable(test_tokens_dropTable)
        self.assertFalse(os.path.exists("tbl_1"))
        os.chdir(cur_cwd)

    def test_dropTable_returns_correct_error_message(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        test_tokens_dropTable = ["DROP", "TABLE", "tbl_1;"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.functions.dropTable(test_tokens_dropTable)
        self.assertEqual(self.functions.dropTable(test_tokens_dropTable), "[ERROR] Table tbl_1 does not exist!")
        os.chdir(cur_cwd)

    def test_dropTable_catches_invalid_command(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        test_tokens_dropTable = ["DROP", "TABLE", "tbl_1"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.assertEqual(self.functions.dropTable(test_tokens_dropTable), "ERROR")
        os.chdir(cur_cwd)

    def test_select_can_open_valid_table(self):
        cur_cwd = os.getcwd()
        test_dir = os.getcwd() + "/test_dir"
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        test_tokens_select = ["SELECT", "*", "FROM", "tbl_1;"]
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.assertTrue(self.functions.select(test_tokens_select))
        os.chdir(cur_cwd)

    def test_select_returns_correct_error_message(self):
        cur_cwd = os.getcwd()
        test_dir = os.getcwd() + "/test_dir"
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        test_tokens_select = ["SELECT", "*", "FROM", "tbl_2;"]
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.assertEqual(self.functions.select(test_tokens_select), "[ERROR] Table tbl_2 does not exist!")
        os.chdir(cur_cwd)

    def test_select_catches_invalid_command(self):
        cur_cwd = os.getcwd()
        test_dir = os.getcwd() + "/test_dir"
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        test_tokens_select = ["SELECT", "*", "FROM", "tbl_1"]
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.assertEqual(self.functions.select(test_tokens_select), "ERROR")
        os.chdir(cur_cwd)

    def test_alterTable_accepts_existing_table(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        test_tokens_alterTable = ["ALTER", "TABLE", "tbl_1", "ADD", "a3", "float;"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.assertTrue(self.functions.alterTable(test_tokens_alterTable))
        os.chdir(cur_cwd)

    def test_alterTable_contents(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        test_tokens_alterTable = ["ALTER", "TABLE", "tbl_1", "ADD", "a3", "float;"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.functions.alterTable(test_tokens_alterTable)
        f = open(test_dir + "/test_db/tbl_1", "r")
        self.assertEqual(f.readline(), "a1 int | a2 varchar(20) | a3 float")
        f.close()
        os.chdir(cur_cwd)

    def test_alterTable_returns_correct_error_message(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_alterTable = ["ALTER", "TABLE", "tbl_1", "ADD", "a3", "float;"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.assertEqual(self.functions.alterTable(test_tokens_alterTable), "[ERROR] Table tbl_1 does not exist!")
        os.chdir(cur_cwd)

    def test_alterTable_catches_invalid_command(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = ["CREATE", "DATABASE", "test_db;"]
        test_tokens_useDB = ["USE", "test_db;"]
        test_tokens_createTable = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        test_tokens_alterTable = ["ALTER", "TABLE", "tbl_1", "ADD", "a3", "float"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.assertEqual(self.functions.alterTable(test_tokens_alterTable), "ERROR")
        os.chdir(cur_cwd)

# Token Parser Module Unit Tests
class TestTokenParser(unittest.TestCase):

    def setUp(self):
        self.parser = TokenParser()
        self.test_user_cmd = "Test Command Arg1 Arg2;"
        self.test_invalid_user_cmd = "Test Command Arg1 Arg2"

    def test_getTokens_tokenizes_input(self):
        target_tokens = ["Test", "Command", "Arg1", "Arg2;"]
        self.assertEqual(self.parser.getTokens(self.test_user_cmd), target_tokens)

    def test_getTokensCreateTable_tokenizes_input(self):
        target_tokens = ["CREATE", "TABLE", "tbl_1", "(a1 int, a2 varchar(20));"]
        self.assertEqual(self.parser.getTokensCreateTable("CREATE TABLE tbl_1 (a1 int, a2 varchar(20));"), target_tokens)

    def test_getNumArgs_returns_integer(self):
        self.assertIsInstance(self.parser.getNumArgs(self.test_user_cmd), int)

    def test_getNumArgs_returns_correct_arg_count(self):
        self.assertEqual(self.parser.getNumArgs(self.test_user_cmd), 4)

    def test_isValidCommand_returns_true_if_cmd_valid(self):
        self.assertTrue(self.parser.isValidCommand(self.test_user_cmd))

    def test_isValidCommand_returns_false_if_cmd_invalid(self):
        self.assertFalse(self.parser.isValidCommand(self.test_invalid_user_cmd))

# DB_Function and Token Parser Integration Tests
class TestDB_FunctionsAndTokenParser(unittest.TestCase):
    
    def setUp(self):
        self.functions = DB_Functions()
        self.parser = TokenParser()

    def tearDown(self):
        os.chdir(".")
        if os.path.exists(os.getcwd() + "/test_dir"):
            try:
                shutil.rmtree(os.getcwd() + "/test_dir")
            except OSError as oserr:
                print(oserr)

    def test_tokens_for_createDB(self):
        user_input = "CREATE DATABASE db_1;"
        tokens = self.parser.getTokens(user_input)
        test_dir = os.getcwd() + "/test_dir"
        self.assertTrue(self.functions.createDB(tokens, test_dir))

    def test_tokens_for_dropDB(self):
        user_input_createDB = "CREATE DATABASE db_1;"
        user_input_dropDB = "DROP DATABASE db_1;"
        tokens_createDB = self.parser.getTokens(user_input_createDB)
        tokens_dropDB = self.parser.getTokens(user_input_dropDB)
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(tokens_createDB, test_dir)
        self.assertEqual(self.functions.dropDB(tokens_dropDB, test_dir), "db_1")

    def test_tokens_for_useDB(self):
        cur_cwd = os.getcwd()
        user_input_createDB = "CREATE DATABASE db_1;"
        user_input_dropDB = "DROP DATABASE db_1;"
        user_input_useDB = "USE db_1;"
        tokens_createDB = self.parser.getTokens(user_input_createDB)
        tokens_dropDB = self.parser.getTokens(user_input_dropDB)
        tokens_useDB = self.parser.getTokens(user_input_useDB)
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(tokens_createDB, test_dir)
        self.assertEqual(self.functions.useDB(tokens_useDB, test_dir), "db_1")
        os.chdir(cur_cwd)

    def test_tokens_for_createTable(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = self.parser.getTokens("CREATE DATABASE db_1;")
        test_tokens_useDB = self.parser.getTokens("USE db_1;")
        test_tokens_createTable = self.parser.getTokensCreateTable("CREATE TABLE tbl_1 (a1 int, a2 varchar(20));")
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.assertTrue(self.functions.createTable(test_tokens_createTable))
        os.chdir(cur_cwd)

    def test_tokens_for_dropTable(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = self.parser.getTokens("CREATE DATABASE test_db;")
        test_tokens_useDB = self.parser.getTokens("USE test_db;")
        test_tokens_createTable = self.parser.getTokensCreateTable("CREATE TABLE tbl_1 (a1 int, a2 varchar(20));")
        test_tokens_dropTable = ["DROP", "TABLE", "tbl_1;"]
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.assertTrue(self.functions.dropTable(test_tokens_dropTable))
        os.chdir(cur_cwd)

    def test_tokens_for_select(self):
        cur_cwd = os.getcwd()
        test_dir = os.getcwd() + "/test_dir"
        test_tokens_createDB = self.parser.getTokens("CREATE DATABASE test_db;")
        test_tokens_useDB = self.parser.getTokens("USE test_db;")
        test_tokens_createTable = self.parser.getTokensCreateTable("CREATE TABLE tbl_1 (a1 int, a2 varchar(20));")
        test_tokens_select = self.parser.getTokens("SELECT * FROM tbl_1;")
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.assertTrue(self.functions.select(test_tokens_select))
        os.chdir(cur_cwd)

    def test_tokens_for_alterTable(self):
        cur_cwd = os.getcwd()
        test_tokens_createDB = self.parser.getTokens("CREATE DATABASE test_db;")
        test_tokens_useDB = self.parser.getTokens("USE test_db;")
        test_tokens_createTable = self.parser.getTokensCreateTable("CREATE TABLE tbl_1 (a1 int, a2 varchar(20));")
        test_tokens_alterTable = self.parser.getTokens("ALTER TABLE tbl_1 ADD a3 float;")
        test_dir = os.getcwd() + "/test_dir"
        self.functions.createDB(test_tokens_createDB, test_dir)
        self.functions.useDB(test_tokens_useDB, test_dir)
        self.functions.createTable(test_tokens_createTable)
        self.assertTrue(self.functions.alterTable(test_tokens_alterTable))
        os.chdir(cur_cwd)

if __name__ == "__main__":
    unittest.main()