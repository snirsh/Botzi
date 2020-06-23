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

    def add_question_node(self, lst_question, question, key, answer="", answers=None):
        """
        add answer to tree
        :param key:
        :param lst_question: question to add upon
        :param question: current question to add
        :param answer: if the question is answering a closed question
        :param answers: if the new answer is a closed question
        :return:
        """

        if answers is None:
            question = OpenQuestion(question, key)
        else:
            question = CloseQuestion(question, answers, key)

        lst_node = self._find_helper(self.root, lst_question)

        return self._add_question_node_helper(question, lst_node, answer)

    def find_question(self, question):
        """

        :param question: string of question
        :return: question node if found, and None otherwise
        """
        qnode = self._find_helper(self.root, question)
        if qnode is not None:
            return qnode.get_qstn_obj()

    #
    # def get_question_obj(self, question):
    #     return self.find_question(question).get_qstn_obj()

    def get_next_question(self, question, ans=""):
        """
        get the next question that comes after the answer
        :param question: string question
        :param ans: string answer
        :return: Question object
        """
        qnode = self._find_helper(self.root, question)
        ans = ans.lower()
        if qnode is not None and qnode.get_next() is not None and qnode.get_next().get(ans) is not None:
            return qnode.get_next()[ans].get_qstn_obj()
        return None

    def is_close(self, question):
        """
        true if the question is a closed question and false otherwise
        will return false also if question is not exist
        :param question: string
        :return: boolean
        """
        qnode = self._find_helper(self.root, question)
        if qnode is not None:
            return isinstance(qnode.get_qstn_obj(), CloseQuestion)
        return False

    def _find_helper(self, qnode, question):
        """
        find the node in the tree which contains question
        :param qnode: QuestionNode
        :param question: string
        :return:
        """
        if qnode is None:
            return None

        question = question.lower()
        if qnode.get_qstn_obj().get_question() == question:
            return qnode

        lst = list(qnode.get_next().values())
        for i in range(len(lst)):
            res = self._find_helper(lst[i], question)
            if res is not None:
                return res

        return None

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

if __name__ == '__main__':
    tree = QuestionTree()
    tree.add_question_node("", "How are you?", "closed", answers=["good", "bad", "excellent"])

    tree.add_question_node("How are you?", "next question?", "you", answer="good")
    tree.add_question_node("How are you?", "next 2 question?", "som", answer="bad")
    tree.add_question_node("How are you?", "next 3 question?", "stam", answer="excellent")

    tree.add_question_node("next question?", "what now?", "another", answers=["ans1", "ans2"])

    question = tree.find_question("next question?")
    print(question.get_key())
    print(tree.get_next_question("How are you?", ans="bad").get_key())
    # print(tree.get_next_question("next question?"))
    # print(tree.is_close("next 2 question?"))

