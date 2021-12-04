# Class to read and write Excel files
import datetime

import xlsxwriter
from xlsxwriter import worksheet
import pandas

from mpp import MPP


class ExcelFile:
    # First day of previous month
    # Calculated as beginning of this month minus 1 day, and take first day of that month)
    Month = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1)

    # Open Excel
    def __init__(self, mpp: MPP):
        self.mpp = mpp
        self.sheet = None
        self.filename = 'C:\\Users\\kcox\\Downloads\\MPP invoices\\' \
                        + self.Month.strftime("%Y%m") \
                        + self.mpp.GetFileName()
        self.wb = xlsxwriter.Workbook(self.filename)

    # Add sheet for month (default last month)
    def AddWorkSheet(self, date=Month):
        self.sheet = self.wb.add_worksheet(date.strftime("%B %Y"))
        return self.sheet

    # Add data to sheet and format sheet
    def AddData(self):
        sheet: worksheet = self.sheet

        # Add new sheet to add the Transactions
        if sheet is None:
            sheet = self.AddWorkSheet()

        # Get data and put into sheet
        df: pandas.DataFrame = self.mpp.GetTransactions(month=self.Month)

        # Format table
        self.FormatTable(sheet)

        tableName = sheet.name.replace(" ", "_")

        (rows, cols) = df.shape
        if '4411' == self.mpp.name:
            cols = 12
        else:
            cols = 6

        data = df.to_dict('split')['data']
        headers = []
        for col in df.columns:
            if 'Location' == col or 'Client' == col or 'Provider' == col:
                headers.append({'header': col})
            elif 'Month' == col:
                headers.append({'header': col,
                                'total_string': 'Totals'})
            elif 'Number_of_transactions' == col: # 177px
                headers.append({'header': col,
                                'total_function': 'sum'})
            elif 'Diff% PRDB/4411' == col:
                headers.append({'header': col})
            else:
                headers.append({'header': col,
                                'total_function': 'sum'})

        sheet.add_table(0, 0, rows, cols - 1,
                        {
                            'name': tableName,
                            'data': data,
                            'columns': headers,
                            'style': 'Table Style Light 9',
                            'total_row': True
                        })

        # Save te file
        self.wb.close()

    # Add table to document and format columns
    def FormatTable(self, sheet: worksheet):
        currency_format = self.wb.add_format({'num_format': '#,##0.00 €;-#,##0.00 €'})
        percentage_format = self.wb.add_format({'num_format': '0%'})
        number_format = self.wb.add_format({'num_format': '0'})

        # format columns
        sheet.set_column('A:D', 12, number_format)
        sheet.set_column('E:E', 12, currency_format)
        sheet.set_column('F:F', 25, number_format)
        sheet.set_column('G:K', 12, currency_format)
        sheet.set_column('L:L', 12, percentage_format)


# main script
if __name__ == '__main__':
    pass
