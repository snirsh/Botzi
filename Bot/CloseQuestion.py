from Bot.Question import *


class CloseQuestion(Question):

    def __init__(self, question, answers, key):
        Question.__init__(self, question, key)
        self._answers = answers

    def get_possible_answers(self):
        return self._answers

