import pyodbc
from pyodbc import SQL_KEYWORDS
import traceback
import random

class Handler:
    def __init__(self, server, database, username):
        self.server = server
        self.database = database
        self.username = username
        self.debug = False
        self.connection = None

    def connect(self):
        SERVER = self.server
        DATABASE = self.database
        USERNAME = self.username
        connection_string = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};Trusted_Connection=yes'
        self.connection = pyodbc.connect(connection_string)

    def get_data(self, table_name, columns = []):
        if self.connection == None or self.connection.closed:
            self.connect()

        try:
            query = '''
                    SELECT {}
                    FROM {}
                    '''.format(','.join(columns), 
                               table_name)
            cur = self.connection.cursor()
            cur.execute(query)
            result = cur.fetchall()

        except Exception as e:
            traceback.print_exception()
            print(f'Error during get_data {e}')

        if self.debug:
            print(query)
        
        self.connection.close()
        return result
    

    def get_random_data(self, table_name, columns = []):
        data = self.get_data(table_name, columns)
        random_data = random.choice(data)
        return random_data
    

    def get_data_conditioned(self, table_name, condition_column, condition, columns = []):
        if self.connection == None or self.connection.closed:
            self.connect()

        try:
            query = '''
                    SELECT {}
                    FROM {}
                    WHERE {} = {}
                    '''.format(','.join(columns),
                               table_name,
                               condition_column,
                               repr(condition))
            cur = self.connection.cursor()
            cur.execute(query)
            result = cur.fetchall()

        except Exception as e:
            traceback.print_exception()
            print(f'Error during get_data_conditioned {e}')

        if self.debug:
            print(query)

        self.connection.close()
        return result
    
    def insert_data(self, table_name, data_dict = {}):
        if self.connection == None or self.connection.closed:
            self.connect()

        try:
            query = '''
                    INSERT INTO {}({})
                    VALUES({})
                    '''.format(table_name,
                               ','.join(data_dict.keys()),
                               ','.join(map(repr, data_dict.values())))
            cur = self.connection.cursor()
            cur.execute(query)
            self.connection.commit()

        except Exception as e:
            traceback.print_exception()
            print(f'Error during insert_data {e}')

        if self.debug:
            print(query)

        self.connection.close()
        
    def update_data(self, table_name, column_a, column_value_a, column_b, column_value_b):
        if self.connection == None or self.connection.closed:
            self.connect()

        try:
            query = '''
                    UPDATE {}
                    SET {} = {}
                    WHERE {} = {}
                    '''.format(table_name,
                               column_a,
                               repr(column_value_a),
                               column_b,
                               repr(column_value_b))
            cur = self.connection.cursor()
            cur.execute(query)
            self.connection.commit()
        
        except Exception as e:
            traceback.print_exception()
            print(f'Error during update_data {e}')

        if self.debug:
            print(query)

        self.connection.close()


    def update_data_addition(self, table_name, column_a, column_value_a, column_b, column_value_b):
        if self.connection == None or self.connection.closed:
            self.connect()

        try:
            query = '''
                    UPDATE {}
                    SET {} += {}
                    WHERE {} = {}
                    '''.format(table_name, 
                               column_a,
                               repr(column_value_a),
                               column_b,
                               repr(column_value_b))
            cur = self.connection.cursor()
            cur.execute(query)
            self.connection.commit()

        except Exception as e:
            traceback.print_exception()
            print(f'Error during update_data_addition {e}')

        if self.debug:
            print(query)

        self.connection.close()

    def drop_data(self, table_name, column, column_value):
        if self.connection == None or self.connection.closed:
            self.connect()
        
        try:
            query = '''
                    DELETE FROM {}
                    WHERE {} = {}
                    '''.format(table_name,
                               column,
                               repr(column_value))
            cur = self.connection.cursor()
            cur.execute(query)
            self.connection.commit()

        except Exception as e:
            traceback.print_exception()
            print(f'Error during drop_data {e}')

        if self.debug:
            print(query)

        self.connection.close() 

    def answer_execute(self, answer):
        answer_checker = 0
        if self.connection == None or self.connection.closed:
            self.connect()
        try:
            cur = self.connection.cursor()
            cur.execute(answer)
            result = cur.fetchall()

        except Exception:
            answer_checker += 1
            pass
        if self.debug:
            print(answer)

        self.connection.close()

        if answer_checker == 0:
            return result

