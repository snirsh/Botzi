from QuestionTree import *
from DataValidation import *

USER_TYPES = ["volunteer", "campaign", "association"]


def initialize_validation_NGO_function():
    NGO_list = [None, None, DataValidation.valid_email, None]
    return NGO_list


def initialize_validation_volunteer_function():
    volunteer_list = [None, DataValidation.valid_email, DataValidation.valid_phone_number, None, None, None, None, None]
    return volunteer_list


def initialize_validation_campaign_function():
    campaign_list = [None, None, None, None, None, None, None]
    return campaign_list


def initialize_db_NGO_keyword():
    NGO_list = ['name', 'contact name', 'mail', 'skills']
    return NGO_list


def initialize_db_volunteer_keyword():
    volunteer_list = ['name', 'mail', 'phone number', 'password', 'skills', 'experience level', 'free time',
                    'preferences']
    return volunteer_list


def initialize_db_campaign_keyword():
    campaign_list = ['name', 'id', 'description', 'requirements', 'start date', 'end date', 'city']
    return campaign_list


def get_fields(p_type):
    if p_type == USER_TYPES[0]:
        return initialize_db_volunteer_keyword()
    elif p_type == USER_TYPES[1]:
        return initialize_db_campaign_keyword()
    else:
        return initialize_db_NGO_keyword()


def get_validation_functions(p_type):
    if p_type == USER_TYPES[0]:
        return initialize_validation_volunteer_function()
    elif p_type == USER_TYPES[1]:
        return initialize_validation_campaign_function()
    else:
        return initialize_validation_NGO_function()


def initialize_static_questions(qtree):
    q1 = "Are you Association, Campaign or Volunteer?"
    ans1 = ["association", 'volunteer', 'campaign']
    qtree.add_question_node("", q1, answers=ans1)

    q2 = "What's your Association name?"
    qtree.add_question_node(q1, q2, answer="association")

    q3 = "Please enter contact name of your association"
    qtree.add_question_node(q2, q3)

    q4 = "What is the email of your association?"
    qtree.add_question_node(q3, q4)

    q5 = "What are your association skills?"
    qtree.add_question_node(q4, q5)

    q6 = "What's your campaign name?"
    qtree.add_question_node(q1, q6, answer="campaign")

    q7 = "What are your requirements? : [type,quantity,domain]"
    qtree.add_question_node(q6, q7)

    q8 = "What is your start date campaign? : [dd/mm/yyyy]"
    qtree.add_question_node(q7, q8)

    q9 = "What is your end date campaign? : [dd/mm/yyyy]"
    qtree.add_question_node(q8, q9)

    q10 = "What is your city campaign?"
    qtree.add_question_node(q9, q10)

    # volunteer
    q12 = "What's your Name?"
    qtree.add_question_node(q1, q12, answer="volunteer")

    q13 = "What's your mail address?"
    qtree.add_question_node(q12, q13)

    q14 = "Please enter your phone number : [xxx-xxxxxxx]"
    qtree.add_question_node(q13, q14)

    q15 = "Please Enter your password"
    qtree.add_question_node(q14, q15)

    q16 = "What are your skills domains? :[X,X,X...]"
    qtree.add_question_node(q15, q16)

    q17 = "What's your free time?"
    qtree.add_question_node(q16, q17, answers=['Free', 'open', 'here and there', 'only one day per week'])

