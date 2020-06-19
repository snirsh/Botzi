from QuestionTree import *


def initialize_static_questions(tree):
    q1 = "Are you Association, Campaign or Volunteer?"
    ans1 = ["association", 'volunteer', 'campaign']
    tree.add_question_node("", q1, answers=ans1)

    q2 = "What's your Association name?"
    tree.add_question_node(q1, q2, answer="association")

    q3 = "Please enter contact name of your association"
    tree.add_question_node(q2, q3)

    q4 = "What is the email of your association?"
    tree.add_question_node(q3, q4)

    q5 = "What are your association skills?"
    tree.add_question_node(q4, q5)

    q6 = "What's your campaign name?"
    tree.add_question_node(q1, q6, answer="campaign")

    q7 = "What are your requirements? : [type,quantity,domain]"
    tree.add_question_node(q6, q7)

    q8 = "What is your start campaign Date? : [dd/mm/yyyy]"
    tree.add_question_node(q7, q8)

    q9 = "What is your end campaign Date? : [dd/mm/yyyy]"
    tree.add_question_node(q8, q9)

    q10 = "What is your city campaign?"
    tree.add_question_node(q9, q10)

    # volunteer
    q12 = "What's your Name?"
    tree.add_question_node(q1, q12, answer="volunteer")

    q13 = "What's your mail address?"
    tree.add_question_node(q12, q13)

    q14 = "Please enter your phone number : [xxx-xxxxxxx]"
    tree.add_question_node(q13, q14)

    q15 = "Please Enter your password"
    tree.add_question_node(q14, q15)

    q16 = "What are your skills domains? :[X,X,X...]"
    tree.add_question_node(q15, q16)

    q17 = "What's your free time?"
    tree.add_question_node(q16, q17, answers=['Free', 'open', 'here and there', 'only one day per week'])

