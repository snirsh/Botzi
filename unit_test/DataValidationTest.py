import unittest
from DataValidation import ValidData


class ValidTest(unittest.TestCase):
    def test_valid_email(self):
        """
        Test that it identified valid email
        """
        result1 = ValidData.valid_email('osnato4050@gmail.com')
        result2 = ValidData.valid_email('osnato4050@@gmail.com')
        result3 = ValidData.valid_email('osnato4050@gmai.l.com')
        result4 = ValidData.valid_email('osnato4050gmail.com')

        self.assertTrue(result1)
        self.assertFalse(result2)
        self.assertFalse(result3)
        self.assertFalse(result4)

    def test_valid_phone_number(self):
        """
        Test that it identified valid phone number
        """
        result1 = ValidData.valid_phone_number('053-9802048')
        result2 = ValidData.valid_phone_number('0539802048')
        result3 = ValidData.valid_phone_number('053--9802048')
        result4 = ValidData.valid_phone_number('053-98020408')
        result5 = ValidData.valid_phone_number('0583-9802048')
        result6 = ValidData.valid_phone_number('05398020489')

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
        result = ValidData.string_to_list(str)
        self.assertEqual(result, str.split(','))


if __name__ == '__main__':
    unittest.main()
