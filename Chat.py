_information_list = []


class Chat:

    def __init__(self, id_recipient):
        self._id_recipient = id_recipient
        self._history = []
        self._final_result = {}

    def add_to_history(self, sender_id, message):
        """
        add a new message to the history dictionary
        :param sender_id: the id of who send the message
        :param message: the message is text or string
        """
        self._history.append((sender_id, message))
        self.update_final_result()

    def get_msgs_num(self):
        """
        :return: the amount of messages that the user send to me
        """
        return len(self._history)/2

    def update_final_result(self):
        if len(self._history) >= 2:
            if self._history[-1][0] == self._id_recipient and self._history[-2][0] != self._id_recipient:
              self._final_result[self._history[-2][1]] = self._history[-1][1]

    def perfect_final_result(self):
        count_information_number = 0
        for information in _information_list:
            if information in self._final_result:
                count_information_number += 1
        if count_information_number == len(_information_list):
            return True
