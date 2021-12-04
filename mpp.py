# Class presenting MPP
import SqlConnection

DBConn = SqlConnection.SQLConnection()


class MPPList:
    global DBConn

    def __init__(self):

        DBConn.Execute("SELECT name FROM masterdata.mpp")
        self.list = []
        df = DBConn.ReturnAll()
        for mppName in df['name']:
            self.list.append(MPP(mppName))


class MPP:
    global DBConn

    def __init__(self, name):
        self.name = name
        self.info = self.ReadInformationFromDataBase()

    def ReadInformationFromDataBase(self):
        DBConn.Execute("Select * from masterdata.mpp where name like ?", {self.name})
        return DBConn.Next()

    def GetName(self):
        return self.info['name']

    def GetEmail(self):
        return self.info['contact_email']

    def GetLanguage(self):
        return self.info['Langue']

    def GetFileName(self):
        return self.info['Report_file']

    def GetTransactions(self, month):
        DBConn.Execute("EXEC staging.Monthly_Report_MPP @MPP=?, @Date=?", (self.info.flowbird_name, month))
        return DBConn.ReturnAll()
