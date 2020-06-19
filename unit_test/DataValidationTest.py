import unittest
from DataValidation import *


class ValidTest(unittest.TestCase):
    def test_valid_email(self):
        """
        Test that it identified valid email
        """
        result1 = DataValidation.valid_email('osnato4050@gmail.com')
        result2 = DataValidation.valid_email('osnato4050@@gmail.com')
        result3 = DataValidation.valid_email('osnato4050@gmai.l.com')
        result4 = DataValidation.valid_email('osnato4050gmail.com')

        self.assertTrue(result1)
        self.assertFalse(result2)
        self.assertFalse(result3)
        self.assertFalse(result4)

    def test_valid_phone_number(self):
        """
        Test that it identified valid phone number
        """
        result1 = DataValidation.valid_phone_number('053-9802048')
        result2 = DataValidation.valid_phone_number('0539802048')
        result3 = DataValidation.valid_phone_number('053--9802048')
        result4 = DataValidation.valid_phone_number('053-98020408')
        result5 = DataValidation.valid_phone_number('0583-9802048')
        result6 = DataValidation.valid_phone_number('05398020489')

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertFalse(result3)
        self.assertFalse(result4)
        self.assertFalse(result5)
        self.assertFalse(result6)

    def test_string_to_list(self):
        """
        Test string to list
        """
        str = 'a,b,c,d,e,f'
        result = DataValidation.string_to_list(str)
        self.assertEqual(result, str.split(','))

    def test_valid_password(self):
        """
        Test if is a valid password
        """

        # len(password) < 6
        result1 = DataValidation.valid_password('12345')
        self.assertFalse(result1)

        # len(password) = 6
        result2 = DataValidation.valid_password('123456')
        self.assertTrue(result2)

        # 6 =< len(password) <= 20
        result3 = DataValidation.valid_password('1234567')
        self.assertTrue(result3)

        # len(password) = 20
        result4 = DataValidation.valid_password('11111111111111111111')
        self.assertTrue(result4)

        # len(password) > 20
        result5 = DataValidation.valid_password('1111111111111111111111')
        self.assertFalse(result5)


if __name__ == '__main__':
    unittest.main()
