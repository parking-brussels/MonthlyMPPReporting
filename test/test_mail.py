import unittest

from mail import Mail


class MyTestCase(unittest.TestCase):
    def test_mail(self):
        Mail('kcox@parking.brussels', [], '<html> <h3>Dag Kris,</h3> <p> dit is een test <p> mvg, <p> Kris Cox</html>').send()

        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
