import unittest
from Bot.DataLoader import *


class ValidTest(unittest.TestCase):
    def test_valid_QuestionTree(self):
        """
        Test if we find the appropriate next question in a QuestionTree
        """
        qtree = QuestionTree()
        initialize_static_questions(qtree)

        # check first message
        q1 = qtree.get_first_msg().get_question()
        pq1 = "are you association, campaign or volunteer?"
        self.assertEquals(q1, pq1)
        ###

        # check close message with questions to answers
        q2 = qtree.get_next_question(pq1, 'Volunteer').get_question()
        pq2 = "what's your name?"
        self.assertEquals(q2, pq2)
        ###

        # check open messages
        q3 = qtree.get_next_question(pq2).get_question()
        pq3 = "what's your mail address?"
        self.assertEquals(q3, pq3)

        q4 = qtree.get_next_question(pq3).get_question()
        pq4 = "please enter your phone number : [xxx-xxxxxxx]"
        self.assertEquals(q4, pq4)

        q5 = qtree.get_next_question(pq4).get_question()
        pq5 = "please enter your password"
        self.assertEquals(q5, pq5)

        q6 = qtree.get_next_question(pq5).get_question()
        pq6 = "what are your skills domains? :[x,x,x...]"
        self.assertEquals(q6, pq6)

        q7 = qtree.get_next_question(pq6).get_question()
        pq7 = "what's your free time?"
        self.assertEquals(q7, pq7)
        ###

        # check close message with no questions to answers
        q8 = qtree.get_next_question(pq7, 'open')
        self.assertIsNone(q8)
        ###


if __name__ == '__main__':
    unittest.main()
