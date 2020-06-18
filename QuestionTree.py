from CloseQuestion import *
from OpenQuestion import *

OPEN_QUESTION_ANS = "open_question"


class QuestionNode:
    def __init__(self, question):
        self._question = question
        self._answers = {}

        if isinstance(question, CloseQuestion):
            answers = question.get_possible_answers()
            for i in range(len(answers)):
                self._answers[answers[i]] = None
        else:
            self._answers[question] = None

    def get_qstn_obj(self):
        return self._question

    def set_next(self, question_node, answer=""):
        answer = answer.lower()
        self._answers[answer] = question_node

    def get_next(self):
        return self._answers


class QuestionTree:

    def __init__(self):
        self.root = None

    def get_first_msg(self):
        if self.root is not None:
            return self.root.get_qstn_obj()

    def _add_question_node_helper(self, question, last_question_node=None, answer=""):
        """
        :param question: current question object to add
        :param last_question_node: last node
        :param answer: last answer
        :return: new node generated
        """

        qnode = QuestionNode(question)
        if self.root is None:
            self.root = qnode
            return qnode

        if isinstance(last_question_node.get_qstn_obj(), CloseQuestion):
            last_question_node.set_next(qnode, answer)
        else:
            last_question_node.set_next(qnode)

        return qnode

    def add_question_node(self, lst_question, question, answer="", answers=None):
        """
        add answer to tree
        :param lst_question: question to add upon
        :param question: current question to add
        :param answer: if the question is answering a closed question
        :param answers: if the new answer is a closed question
        :return:
        """

        answer = answer.lower()
        question = question.lower()
        if answers is not None:
            for ans in answers:
                ans = ans.lower()

        if answers is None:
            question = OpenQuestion(question)
        else:
            question = CloseQuestion(question, answers)

        lst_node = self.find_question(lst_question)

        return self._add_question_node_helper(question, lst_node, answer)

    def find_question(self, question):
        """

        :param question: string of question
        :return: question node if found, and None otherwise
        """
        return self._find_helper(self.root, question)

    def get_question_obj(self, question):
        return self.find_question(question).get_qstn_obj()

    def get_next_question(self, question, ans=""):
        """
        get the next question that comes after the answer
        :param question: string question
        :param ans: string answer
        :return: Question object
        """
        node = self.find_question(question)
        ans = ans.lower()
        if node is not None and node.get_next()[ans] is not None:
            return node.get_next()[ans].get_qstn_obj()
        return None

    def is_close(self, question):
        """
        true if the question is a closed question and false otherwise
        will return false also if question is not exist
        :param question: string
        :return: boolean
        """
        node = self.find_question(question)
        if node is not None:
            return isinstance(node.get_qstn_obj(), CloseQuestion)
        return False

    def _find_helper(self, node, question):
        if node is None:
            return None

        question = question.lower()
        if node.get_qstn_obj().get_question() == question:
            return node

        lst = list(node.get_next().values())
        for i in range(len(lst)):
            res = self._find_helper(lst[i], question)
            if res is not None:
                return res

        return None


if __name__ == '__main__':
    tree = QuestionTree()
    tree.add_question_node("", "How are you?", answers=["good", "bad", "excellent"])

    tree.add_question_node("How are you?", "next question?", answer="good")
    tree.add_question_node("How are you?", "next 2 question?", answer="bad")
    tree.add_question_node("How are you?", "next 3 question?", answer="excellent")

    tree.add_question_node("next question?", "what now?", answers=["ans1", "ans2"])

    node = tree.find_question("next question?")
    print(tree.get_next_question("next question?"))
    print(tree.is_close("next 2 question?"))

