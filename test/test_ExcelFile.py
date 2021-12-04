import datetime
import unittest

from excelfile import ExcelFile
from mpp import MPP


class MyTestCase(unittest.TestCase):
    def test_something(self):
        mpp = MPP('4411')
        file = ExcelFile(mpp)
        self.assertIsNotNone(file.wb, "Worksheet not open")
        # self.assertEqual(file.wb.sheetnames[0], "January 2021", "Wrong file")

    def test_addworksheet(self):
        mpp = MPP('4411')
        file = ExcelFile(mpp)
        file.AddWorkSheet(datetime.date(2020, 12, 5))
        self.assertIsNotNone(file.wb["December 2020"], "Failed adding sheet")

    def test_adddata(self):
        mpp = MPP('4411')
        file = ExcelFile(mpp)
        file.AddData()

if __name__ == '__main__':
    unittest.main()
