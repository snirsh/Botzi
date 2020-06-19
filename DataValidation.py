import re
import DataLoader as dl


class DataValidation:
    @staticmethod
    def valid_email(email):
        """
       :param email: need to be appropriate to regex
       :return: if is a valid email address
       """
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        # pass the regular expression
        # and the string in search() method
        if re.search(regex, email):
            return True
        return False

    @staticmethod
    def valid_phone_number(phone_number):
        """
            :param phone_number: 000-0000000 or 0000000000
            :return: if is a valid phone number
            """
        if len(phone_number) == 11 and '-' in phone_number:
            number = phone_number[0:3] + phone_number[4:11]
            return number.isdigit()
        elif len(phone_number) == 10:
            return phone_number.isdigit()
        return False

    @staticmethod
    def string_to_list(str_cur):
        """
        :param str_cur: is list we get in str
        :return: the list of the str
        """
        return str_cur.split(',')



def _valid_answer(question, answer, fields, fields_functions):
    zip_dict = dict(zip(fields, fields_functions))
    for field in fields:
        if field in question:
            if zip_dict[field]:
                return zip_dict[field](answer)
            else:
                return True
    return False


def valid_answer(question, answer, chat):
    p_type = chat.get_p_type()
    return _valid_answer(question, answer, dl.get_fields(p_type), dl.get_validation_functions(p_type))


