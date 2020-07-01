import re
import datetime
# import FirestoreDb as fb


class DataValidator:

    def __init__(self, db):
        self._db = db
        self._p_type = ""
        self._validator_matcher = {
            "mail": self.valid_email,
            "phone": DataValidator.valid_phone_number,
            "password": DataValidator.valid_password,
            "start date": DataValidator.valid_date,
            "end date": DataValidator.valid_date
        }

    def valid_email(self, email):
        """
       :param email: need to be appropriate to regex
       :return: if is a valid email address
       """
        email = email.lower()
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        if not re.search(regex, email):
            raise ValueError("Email is not valid")
        self._db.is_email_exist(email, self._p_type)

    def valid_answer(self, answer, field, chat):
        self._p_type = chat.get_p_type()
        return self._valid_answer(
            answer,
            field
        )

    @staticmethod
    def valid_phone_number(phone_number):
        """
            :param phone_number: 000-0000000 or 0000000000
            :return: if is a valid phone number
            """
        if len(phone_number) == 11 and '-' in phone_number:
            number = phone_number[0:3] + phone_number[4:11]
            if number.isdigit():
                return
        elif len(phone_number) == 10:
            if phone_number.isdigit():
                return
        raise ValueError("Phone number is not valid")

    @staticmethod
    def valid_password(password):
        """
        :param password: the password str : 6=< len(password) <= 20
        :return: if is a valid password
        """
        if 6 > len(password) or len(password) > 20:
            raise ValueError("Password must be between 6 to 20 characters")

    @staticmethod
    def valid_date(date_text):
        date_text = date_text.replace('/', '-')
        try:
            datetime.datetime.strptime(date_text, '%d-%m-%Y')
        except ValueError:
            raise ValueError("Date must be in the format \"DD/MM/YYYY\" ")

    def _valid_answer(self, answer, field):
        if field in self._validator_matcher:
            return self._validator_matcher[field](answer)


