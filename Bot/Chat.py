
from Bot.DataLoader import USER_TYPES


class Chat:

    def __init__(self, id_recipient):
        self._id_recipient = id_recipient
        self._history = []
        self._final_result = {}
        self.p_type = ""
        self._last_massage = ""
        self._last_question = ""

    def add_to_history(self, sender_id, message, msg_key):
        """
        add a new message to the history dictionary
        :param msg_key:
        :param sender_id: the id of who send the message
        :param message: the message is text or string
        """
        if message in USER_TYPES:
            self.p_type = message

        if sender_id == self._id_recipient:
            self._last_massage = message
        else:
            self._last_question = message

        self._history.append((sender_id, message, msg_key))

    def add_to_final_result(self, key, value):
        self._final_result[key] = value

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
        return self._last_question

    def is_empty(self):
        return len(self._history) == 0

    @staticmethod
    def string_to_list(str_cur):
        """
        :param str_cur: is list we get in str
        :return: the list of the str
        """
        lst = str_cur.split(',')
        for i in range(len(lst)):
            lst[i] = lst[i].strip()
        return lst

    def update_final_result(self):
        print(self._history)
        for idx, record in enumerate(self._history):
            if idx >= 1 and record[2] != "":
                field = record[2]
                field = field.replace(' ', '_')
                self._final_result[field] = self._history[idx][1]
        multiple_options = ["skills", "requirements"]
        for mo in multiple_options:
            if mo in self._final_result:
                self._final_result[mo] = self.string_to_list(self._final_result[mo])

    def get_final_result(self):
        return self._final_result

    def set_history(self, history):
        self._history = history


if __name__ == '__main__':
    history = [('100834055011426', "what's your name?", ''), ('3151275694916094', 'osnagdhg jf]\\', 'name'), ('100834055011426', 'welcome and thank you for reaching me! first, please choose which one describes you best', ''), ('3151275694916094', 'volunteer', '"'), ('100834055011426', "i need your email for the sign-up, what's your email address??", ''), ('3151275694916094', 'orem@gmail.com', 'mail'), ('100834055011426', "and what's your phone number, please?", ''), ('3151275694916094', '99999999999', 'phone'), ('100834055011426', "and what's your phone number, please?", ''), ('3151275694916094', '0000000000', 'phone'), ('100834055011426', 'where do you live?', ''), ('3151275694916094', 'jdjg', 'city'), ('100834055011426', "and just one last question, would you please write your skills in which you're willing to volunteer", ''), ('3151275694916094', 'jfghildg', 'skills'), ('3151275694916094', 'jfghildg', 'skills'), ('3151275694916094', 'jfghildg', 'skills'), ('3151275694916094', 'jfghildg', 'skills'), ('3151275694916094', 'jfghildg', 'skills')]
    chat = Chat(2921984041247793)
    chat.set_history(history)
    chat.update_final_result()
    print(chat.get_final_result())

