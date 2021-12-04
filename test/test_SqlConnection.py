import unittest
import SqlConnection


class MyTestCase(unittest.TestCase):
    def test_connection(self):
        try:
            TestConnection = SqlConnection.SQLConnection()
            TestConnection.Execute("select * from masterdata.mpp")
            row = TestConnection.Next()
            self.assertIsNotNone(row, "No rows returned")
            self.assertEqual(row[0], "4411", "First row is not Be-Mobile")

        except Exception:
            print(Exception)
            self.assertTrue(False, "Error testing TestConnection")


if __name__ == '__main__':
    unittest.main()
