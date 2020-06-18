from OpenQuestion import *
from CloseQuestion import *

OPEN_QUESTION = "OpenQuestion"
CLOSE_QUESTION = "CloseQuestion"


class QuestionsCollections:

    def __init__(self):
        self._dict = {}
        self._index = 0

    def get_question(self, index):
        if index < len(self._dict):
            return self._dict[index]
        return -1

    def question_number(self):
        return len(self._dict)

    def add_new_question(self, q_type, question, answers):
        # add a open question
        if q_type == OPEN_QUESTION:
            self._dict[self._index] = OpenQuestion(question)
        # add a close question
        elif q_type == CLOSE_QUESTION:
            # if question in self._dict:
            # self._dict[question]._answers = self._dict[question]._answers + answers
            self._dict[self._index] = CloseQuestion(question, answers)

        # set the index of the question
        self._index += 1


