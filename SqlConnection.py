import pyodbc
import Identity
from pandas import read_sql, DataFrame
from pyodbc import Cursor, Connection, Row


class SQLConnection:
    data: DataFrame
    conn: Connection
    row: int

    def __init__(self):
        self.row = -1
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
        self.row = 0
        try:
            if param is None:
                self.data = read_sql(query, self.conn)
            else:
                self.data = read_sql(query, self.conn, params=param)

        except pyodbc.DatabaseError as e:
            print(e)
            raise Exception("Query execution error")

    def Next(self):
        rowData = self.data.iloc[self.row]
        self.row += 1
        return rowData

    def ReturnAll(self):
        return self.data

    def Reset(self):
        self.row = 0
