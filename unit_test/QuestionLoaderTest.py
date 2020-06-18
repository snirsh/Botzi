import QuestionLoader as ql
import QuestionTree as qt


if __name__ == '__main__':
    tree = qt.QuestionTree()
    ql.initialize_static_questions(tree)

    q1 = tree.get_first_msg()
    print(q1.get_question())

    q2 = tree.get_next_question(q1.get_question(), "volunteer")

    print(q2.get_question())

