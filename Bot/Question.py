
class Question:

    def __init__(self, question, key):
        question = question.lower()
        key = key.lower()
        self._question = question
        self._key = key

    def get_question(self):
        return self._question

    def get_key(self):
        return self._key
