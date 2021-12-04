# Script to create and send monthly MPP reports to the MPP

# main script
from excelfile import ExcelFile
from mpp import MPPList, MPP

if __name__ == '__main__':
    for mpp in MPPList().list:
        file = ExcelFile(mpp)
        file.AddData()
