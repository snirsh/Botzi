# _information_list = []

from DataLoader import USER_TYPES


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

    def update_final_result(self, fields, fields_functions):
        zip_dict = dict(zip(fields, fields_functions))
        i = 0
        valid = False
        for field in fields:
            while i < len(self._history):
                if i % 2 == 0 and field in self._history[i][1]:
                    answer = self._history[i + 1][1]
                    if zip_dict[field]:
                        valid = zip_dict[field](answer)
                    else:
                        valid = True
                    if valid:
                        self._final_result[field] = answer
                    i += 2
                i += 1

    # def perfect_final_result(self):
    #     count_information_number = 0
    #     for information in _information_list:
    #         if information in self._final_result:
    #             count_information_number += 1
    #     if count_information_number == len(_information_list):
    #         return True


if __name__ == '__main__':
    chat = Chat(1234)
    chat.add_to_history(144, "m1")
