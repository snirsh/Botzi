# _information_list = []

from DataLoader import USER_TYPES, get_fields, get_validation_functions


class Chat:

    def __init__(self, id_recipient):
        self._id_recipient = id_recipient
        self._history = []
        self._final_result = {}
        self.p_type = ""

    def add_to_history(self, sender_id, message):
        """
        add a new message to the history dictionary
        :param sender_id: the id of who send the message
        :param message: the message is text or string
        """
        if message in USER_TYPES:
            self.p_type = message

        self._history.append((sender_id, message))

    def get_msgs_num(self):
        """
        :return: the amount of messages that the user send to me
        """
        return len(self._history)/2

    def get_p_type(self):
        return self.p_type

    def get_message(self, index):
        if index < len(self._history):
            return self._history[index]

    def get_last_qstn(self):
        """
        get the last message in the history of the chat
        :return: string. will return empty string if not found any
        """
        if len(self._history) == 0:
            return ""
        return self._history[-1][1]

    def is_empty(self):
        return len(self._history) == 0

    @staticmethod
    def string_to_list(str_cur):
        """
        :param str_cur: is list we get in str
        :return: the list of the str
        """
        return str_cur.split(',')

    def update_final_result(self):

        fields = get_fields(self.p_type)
        # fields_functions = get_validation_functions(self.p_type)

        # zip_dict = dict(zip(fields, fields_functions))
        i = 3
        # valid = False
        for field in fields:
            while i < len(self._history):
                if i % 2 != 0 and field in self._history[i][1]:
                    answer = self._history[i + 1][1]
                    # if zip_dict[field]:
                    #     valid = zip_dict[field](answer)
                    # else:
                    #     valid = True
                    # if valid:
                    field = field.replace(' ', '_')
                    self._final_result[field] = answer
                i += 1
            i = 3

        multiple_options = ["skills", "requirements"]
        for mo in multiple_options:
            if mo in self._final_result:
                self._final_result[mo] = self.string_to_list(self._final_result[mo])

    def get_final_result(self):
        return self._final_result
    # def perfect_final_result(self):
    #     count_information_number = 0
    #     for information in _information_list:
    #         if information in self._final_result:
    #             count_information_number += 1
    #     if count_information_number == len(_information_list):
    #         return True


# if __name__ == '__main__':
#     history = [('2921984041247793', 'yo'), ('111305403958818', 'are you association, campaign or volunteer?'), ('2921984041247793', 'volunteer'), ('111305403958818', "what's your name?"), ('2921984041247793', 'dfsdf'), ('111305403958818', "what's your mail address?"), ('2921984041247793', 'dfsd@fds.com'), ('111305403958818', 'please enter your phone number : [xxx-xxxxxxx]'), ('2921984041247793', '0501112223'), ('111305403958818', 'please enter your password'), ('2921984041247793', '1234567'), ('111305403958818', 'what are your skills domains? :[x,x,x...]'), ('2921984041247793', 'sdf,sdf'), ('111305403958818', "what's your free time?"), ('2921984041247793', 'here and there'), ('2921984041247793', 'here and there'), ('2921984041247793', 'here and there'), ('2921984041247793', 'here and there'), ('2921984041247793', 'here and there'), ('2921984041247793', 'here and there'), ('2921984041247793', 'here and there'), ('2921984041247793', 'here and there'), ('2921984041247793', 'here and there'), ('2921984041247793', 'here and there'), ('2921984041247793', 'here and there'), ('2921984041247793', 'here and there'), ('2921984041247793', 'here and there'), ('2921984041247793', 'here and there')]
#     chat = Chat(123)
#     chat.update_final_result(history)
#     print(chat.get_final_result())

