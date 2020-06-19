from Question import *


class CloseQuestion(Question):

    def __init__(self, question, answers):
        Question.__init__(self, question)
        self._answers = answers

    def get_possible_answers(self):
        return self._answers

