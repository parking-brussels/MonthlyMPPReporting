# Class presenting MPP
import pyodbc as pyodbc
import Identity


class mpp:
    def __init__(self,name):
        self.name = name
        self.ReadInformationFromDataBase()

    def ReadInformationFromDataBase(self):
        target = Identity.config_access("pb_sql")
        conn = pyodbc.connect(
            'Driver={Driver}; Server={Server}; Database={Database}; UID={Uid}; PWD={Pwd}'.format(
                Driver = "ODBC Driver 17 for SQL Server",
                Server = "sv009",
                Database = "Analytics",
                Uid=target["Uid"],
                Pwd=target["Pwd"]
            )
        )
