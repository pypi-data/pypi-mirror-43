###########################
# PyMySQL wrapper class
#
# Example:
# db = MySQL({
#     "user" : "root",
#     "name" : "dbname",
#     "host" : "databasehost.com",
#     "pass" : "password"
# })
#
# print(db.config)
# >>> {
# >>>    "user" : "root",
# >>>    "name" : "dbname",
# >>>    "host" : "databasehost.com",
# >>>    "pass" : "password"
# >>> }
#
# print(db.test_connection())
# >>> Connected!
#
# print(db.query("SELECT * FROM my_table"))
# >>> ...array of rows...
###########################

import pymysql
import sys

class MySQL:

    def __init__(self, config):
        self.config = config

    def connect(self):
        return pymysql.connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['pass'],
            db=self.config['name'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def test_connection(self):
        try:
            connected = pymysql.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['pass'],
                db=self.config['name'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            connected.close()
            return "Connected!"
        except Exception as e:
            e = str(e)
            return e

    def prepare_query(self, string):
        string = pymysql.escape_string(str(string))
        return string

    def query(self, sql):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            result = cursor.execute(sql)
            if "SELECT".lower() in sql.lower() and "FROM".lower() in sql.lower():
                result = cursor.fetchall()
            else:
                result = cursor.lastrowid
            connection.close()
            return result
        except Exception as e:
            f = list(sys._current_frames().values())[-1]
            file = f.f_back.f_globals['__file__']
            linenumber = f.f_back.f_lineno
            function_name = f.f_back.f_code.co_name
            error_object = {
                "error" : {
                    "code" : "SqlError",
                    "message" : str(e),
                    "details" : {
                        "file" : file,
                        "line" : linenumber,
                        "sql" : sql,
                        "function_name" : function_name
                    }
                }
            }
            print(str(e))
            print("SQL: " + sql)
            return error_object
