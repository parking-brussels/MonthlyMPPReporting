import pyodbc
from pyodbc import Cursor, Connection, Row

import Identity


class SQLConnection:
    cursor: Cursor
    conn: Connection
    row: Row

    def __init__(self):
        self.target = {
            "pb_sql": {
                "Driver": "ODBC Driver 17 for SQL Server",
                "Server": "sv009",
                "Uid": "***",
                "Pwd": "{***}"  # needs to be specified
            }
        }
        Identity.config_access(self.target)
        try:
            self.conn = pyodbc.connect(
                'Driver={Driver}; Server={Server}; Database={Database}; UID={Uid}; PWD={Pwd}'.format(
                    Driver=self.target["pb_sql"]["Driver"],
                    Server=self.target["pb_sql"]["Server"],
                    Database="Analytics",
                    Uid=self.target["pb_sql"]["Uid"],
                    Pwd=self.target["pb_sql"]["Pwd"]
                )
            )

        except pyodbc.DatabaseError:
            raise Exception("Connection error")

    def Execute(self, query, param=None):
        try:
            self.cursor = self.conn.cursor()
            if param is None:
                self.cursor = self.cursor.execute(query)
            else:
                self.cursor = self.cursor.execute(query, param)

        except pyodbc.DatabaseError as e:
            print(e)
            raise Exception("Query execution error")

    def Next(self):
        try:
            row = self.cursor.fetchone()
            return row

        except pyodbc.DatabaseError:
            print("Fetch data from SQL server error")
            return None

    def ReturnAll(self):
        return self.cursor.fetchall()
