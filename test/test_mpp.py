import unittest

from mpp import MPP, MPPList


class MyTestCase(unittest.TestCase):
    def test_MPP(self):
        testMpp = MPP("4411")
        self.assertEqual(testMpp.GetName(), "4411", "Wrong MPP returned")
        self.assertEqual(testMpp.GetEmail(), "nicolas.talpe@be-mobile.com", "Wrong mail address")
        self.assertEqual(testMpp.GetLanguage(), "NL", "Wrong language")
        self.assertRegex(testMpp.GetFileName(), ".*.xlsx", "Wrong file name")

    def test_MPPList(self):
        testMPPList = MPPList()
        self.assertEqual(testMPPList.list.__len__(), 9, "Not all MPP returned")


if __name__ == '__main__':
    unittest.main()
