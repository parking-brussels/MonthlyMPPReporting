# Class presenting MPP
import calendar
from datetime import date

import SqlConnection

DBConn = SqlConnection.SQLConnection()



class MPPList:
    global DBConn


    def __init__(self, month: date):
        # last day of month
        lastday = month.replace(day=calendar.monthrange(month.year, month.month)[1])

        DBConn.Execute("SELECT distinct name FROM masterdata.mpp "
                       "WHERE (date_from < ? or date_from IS NULL) "
                       "AND (date_until > ? or date_until IS NULL) "
                       "AND PCC_code IS NOT NULL", (month, lastday))
        self.list = []
        df = DBConn.ReturnAll()
        for mppName in df['name']:
            self.list.append(MPP(mppName, month))



class MPP:
    global DBConn
    month: date = None
    lastDay: date = None


    def __init__(self, _name, _month: date):
        self.name = _name
        self.month = _month
        self.lastDay = _month.replace(day=calendar.monthrange(_month.year, _month.month)[1])
        self.info = self.ReadInformationFromDataBase()


    def ReadInformationFromDataBase(self):
        DBConn.Execute("Select * "
                       "from masterdata.mpp "
                       "where name like ? "
                       "and (date_until > ? or date_until is null)"
                       "and (date_from < ? or date_from is null)"
                       "and PCC_code IS NOT NULL", (self.name, self.month, self.lastDay))
        return DBConn.Next()


    def GetName(self):
        return self.info['name']


    def GetEmail(self):
        return self.info['contact_email']


    def GetLanguage(self):
        return self.info['Langue']


    def GetFileName(self):
        return self.info['Report_file']


    def GetTransactions(self):
        DBConn.Execute("EXEC staging.Monthly_Report_MPP @MPP=?, @Date=?", (self.info.flowbird_name, self.month))
        return DBConn.ReturnAll()
