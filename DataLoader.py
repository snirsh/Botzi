from Bot.QuestionTree import *

from Bot.DataValidator import *

from googletrans import Translator


USER_TYPES = ["volunteer", "campaign", "association"]


def initialize_validation_NGO_function():
    NGO_list = [None, None, DataValidator.valid_email, None]
    return NGO_list


def initialize_validation_volunteer_function():
    volunteer_list = [None, DataValidator.valid_email, DataValidator.valid_phone_number, None, None, None, None, None]
    return volunteer_list


def initialize_validation_campaign_function():
    campaign_list = [None, None, DataValidator.valid_date, DataValidator.valid_date, None]
    return campaign_list


def initialize_organization_keyword():
    NGO_list = ['name', 'contact name', 'mail', 'phone']
    return NGO_list


def initialize_db_volunteer_keyword():
    volunteer_list = ['name', 'mail', 'phone', 'password', 'skills', 'experience level', 'free time',
                    'preferences']
    return volunteer_list


def initialize_db_campaign_keyword():
    campaign_list = ['name', 'requirements', 'start date', 'end date', 'city']
    return campaign_list


def get_fields(p_type):
    if p_type == USER_TYPES[0]:
        return initialize_db_volunteer_keyword()
    elif p_type == USER_TYPES[1]:
        return initialize_db_campaign_keyword()
    else:
        return initialize_organization_keyword()


def initialize_static_questions(qtree):
    q1 = "Are you Association, Campaign or Volunteer?"
    ans1 = ["association", 'volunteer', 'campaign']
    qtree.add_question_node("", q1, "type", answers=ans1)

    q2 = "What's your Association name?"
    qtree.add_question_node(q1, q2, "name", answer="association")

    q3 = "Please enter contact name of your association"
    qtree.add_question_node(q2, q3, "contact name")

    q4 = "What is the email of your association?"
    qtree.add_question_node(q3, q4, "mail")

    q5 = "What is your association phone number? [xxx-xxxxxxx]"
    qtree.add_question_node(q4, q5, "phone")

    q6 = "What's your campaign name?"
    qtree.add_question_node(q1, q6, "name", answer="campaign")

    q7 = "What are your requirements? : [type,quantity,domain]"
    qtree.add_question_node(q6, q7, "requirements")

    q8 = "What is your start date campaign? : [dd/mm/yyyy]"
    qtree.add_question_node(q7, q8, "start date")

    q9 = "What is your end date campaign? : [dd/mm/yyyy]"
    qtree.add_question_node(q8, q9, "end date")

    q10 = "What is your city campaign?"
    qtree.add_question_node(q9, q10, "city")

    # volunteer
    q12 = "What's your Name?"
    qtree.add_question_node(q1, q12, "name", answer="volunteer")

    q13 = "What's your mail address?"
    qtree.add_question_node(q12, q13, "mail")

    q14 = "Please enter your phone number : [xxx-xxxxxxx]"
    qtree.add_question_node(q13, q14, "phone")

    q15 = "Please Enter your password"
    qtree.add_question_node(q14, q15, "password")

    q16 = "What are your skills domains? :[X,X,X...]"
    qtree.add_question_node(q15, q16, "skills")

    q17 = "What's your free time?"
    qtree.add_question_node(q16, q17, "free time", answers=['Free', 'open', 'here and there', 'only one day per week'])


def make_file_for_translate(file_name):
    """
    :param file_name: to make ready to translate
    :return: the name of the new file that ready to translate without the data 'key_value'
    """
    flag = True
    file_for_translate_name = r'C:\Users\osnat\botzi\file_for_translate.txt'
    f_read = open(file_name, "r")
    f_write = open(file_for_translate_name, "a")
    while f_read and f_write:
        last_question = f_read.readline()
        if not last_question == '"""' and last_question:  # if its not the end of the file
            answer_to = f_read.readline()
            question = f_read.readline()
            answers = f_read.readline()
            key_value = f_read.readline()

            last_question = last_question.split(':')
            if len(last_question) > 1 and '"' not in last_question[1]:
                last_question = last_question[1]
            else:
                last_question = "-\n"

            answer_to = answer_to.split(':')
            if len(answer_to) > 1 and '"' not in answer_to[1]:
                answer_to = answer_to[1]
            else:
                answer_to = "-\n"

            question = question.split(':')
            if len(question) > 1 and '"' not in question[1]:
                question = question[1]
            else:  # don't need to happen
                raise ValueError("error: no question text")

            answers = answers.split(':')
            if len(answers) > 1 and '"' not in answers[1]:
                answers = answers[1]
            else:
                answers = "-\n"

            key_value = key_value.split(':')
            if len(key_value) > 1 and '"' not in key_value[1]:
                key_value = key_value[1]
            else:
                key_value = "\n"

            f_write.write(last_question)
            f_write.write(answer_to)
            f_write.write(question)
            f_write.write(answers)

        else:
            f_read.close()
            f_write.close()
            flag = False
            break
    if flag:
        f_read.close()
        f_write.close()
    return file_for_translate_name


def load_question_data(file_name):
    """
    :param file_name: file in appropriate format to make the QuestionTree collection
    :return: the QuestionTree collection of the file 'file_name'
    """
    question_tree = QuestionTree()
    f = open(file_name, "r")
    while f:
        last_question = f.readline()
        if not last_question == '"""' and last_question:  # if its not the end of the file
            answer_to = f.readline()
            question = f.readline()
            answers = f.readline()
            key_value = f.readline()

            last_question = last_question.split(':')
            if len(last_question) > 1 and '"' not in last_question[1] or '-' not in last_question[1]:
                last_question = last_question[1].rstrip()
            else:
                last_question = ""

            answer_to = answer_to.split(':')
            if len(answer_to) > 1 and '"' not in answer_to[1] or '-' not in answer_to[1]:
                answer_to = answer_to[1].rstrip()
            else:
                answer_to = ""

            question = question.split(':')
            if len(question) > 1 and '"' not in question[1] or '-' not in question[1]:
                question = question[1].rstrip()
            else:  # don't need to happen
                raise ValueError("error: no question text")

            answers = answers.split(':')
            if len(answers) > 1 and '"' not in answers[1] or '-' not in answers[1]:
                answers = answers[1].split(',')
                answers[-1] = answers[-1].rstrip()
            else:
                answers = None

            key_value = key_value.split(':')
            if len(key_value) > 1 and '"' not in key_value[1] or '-' not in key_value[1]:
                key_value = key_value[1].rstrip()
            else:
                key_value = ""

            question_tree.add_question_node(last_question, question, answer_to, answers)
            # question_tree.add_question_node(last_question, question, key_value, answer_to, answers)

        else:
            f.close()
            break

    f.close()
    return question_tree


def make_translate_file_to_format_file(translate_file_name, english_file_name):
    """
    :param translate_file_name: a name of translate file
    :param english_file_name: a name of the translate file before translate - in english
    :return: a name of a new translate file  in the appropriate format
    """
    format_file_name = r'C:\Users\osnat\botzi\translate_file_in_format.txt'
    translate_file = open(translate_file_name, 'r')
    english_file = open(english_file_name, 'r')
    format_file = open(format_file_name, 'a')

    while translate_file and english_file and format_file:

        translate_last_question = translate_file.readline()
        english_last_question = english_file.readline()
        if translate_last_question and not english_last_question == '"""' and english_last_question:  # if its not the end of the file

            translate_answer_to = translate_file.readline()
            translate_question = translate_file.readline()
            translate_answers = translate_file.readline()

            if translate_last_question == '\n':
                translate_last_question = '"\n'
            if translate_answer_to == '\n':
                translate_answer_to = '"\n'
            if translate_question == '\n':
                translate_question = '"\n'
            if translate_answers == '\n':
                translate_answers = '"\n'

            if translate_last_question == "" or not translate_last_question[-1] == "\n":
                translate_last_question += '\n'
            if translate_answer_to == "" or not translate_answer_to[-1] == "\n":
                translate_answer_to += '\n'
            if translate_question == "" or not translate_question[-1] == "\n":
                translate_question += '\n'
            if translate_answers == "" or not translate_answers[-1] == "\n":
                translate_answers += '\n'

            english_answer_to = english_file.readline()
            english_question = english_file.readline()
            english_answers = english_file.readline()
            english_key_value = english_file.readline()

            english_last_question = english_last_question.split(':')
            if len(english_last_question) > 1 and '"' not in english_last_question[1]:
                english_last_question = english_last_question[0] + ':'
            else:
                english_last_question = "last_question:"

            english_answer_to = english_answer_to.split(':')
            if len(english_answer_to) > 1 and '"' not in english_answer_to[1]:
                english_answer_to = english_answer_to[0] + ':'
            else:
                english_answer_to = "answers_to:"

            english_question = english_question.split(':')
            if len(english_question) > 1 and '"' not in english_question[1]:
                english_question = english_question[0] + ':'
            else:  # don't need to happen
                raise ValueError("error: no question text")

            english_answers = english_answers.split(':')
            if len(english_answers) > 1 and '"' not in english_answers[1]:
                english_answers = english_answers[0] + ':'
            else:
                english_answers = "answers:"

            format_file.write(english_last_question + translate_last_question)
            format_file.write(english_answer_to + translate_answer_to)
            format_file.write(english_question + translate_question)
            format_file.write(english_answers + translate_answers)
            format_file.write(english_key_value)

        else:
            english_file.close()
            translate_file.close()
            format_file.close()
            break

    english_file.close()
    translate_file.close()
    format_file.close()
    return format_file_name


def translate_to_hebrew(translate_file_name):
    """
    :param translate_file_name: a file with text in English
    :return: a name of the translate file to hebrew
    """
    translator = Translator()
    f_en = open(translate_file_name, 'r')
    data = f_en.read()
    result = translator.translate(data, src='en', dest='he').text
    f_en_name = r'C:\Users\osnat\botzi\file_translate_to_hebrew.txt'
    f_eb = open(f_en_name, 'w')
    f_eb.write(result)
    return f_en_name


if __name__ == '__main__':
    english_file1 = r'C:\Users\osnat\botzi\english.txt'
    for_translate_file1 = make_file_for_translate(english_file1)
    translate_file1 = translate_to_hebrew(for_translate_file1)
    format_file1 = make_translate_file_to_format_file(translate_file1, english_file1)
    qtree1 = load_question_data(format_file1)
