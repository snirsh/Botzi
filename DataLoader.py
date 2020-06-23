import os

from QuestionTree import *
from DataValidation import *
from googletrans import Translator
import codecs

USER_TYPES = ["volunteer", "campaign", "association"]


def initialize_validation_NGO_function():
    NGO_list = [None, None, DataValidation.valid_email, None]
    return NGO_list


def initialize_validation_volunteer_function():
    volunteer_list = [None, DataValidation.valid_email, DataValidation.valid_phone_number, None, None, None, None, None]
    return volunteer_list


def initialize_validation_campaign_function():
    campaign_list = [None, None, DataValidation.valid_date, DataValidation.valid_date, None]
    return campaign_list


def initialize_db_NGO_keyword():
    NGO_list = ['name', 'contact name', 'mail', 'skills']
    return NGO_list


def initialize_db_volunteer_keyword():
    volunteer_list = ['name', 'mail', 'phone number', 'password', 'skills', 'experience level', 'free time',
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


def make_file_for_translate(file_name):
    """
    :param file_name: to make ready to translate
    :return: the name of the new file that ready to translate without the data 'key_value'
    """
    flag = True
    script_dir = os.path.dirname(__file__)
    file_for_translate_name = script_dir + r'\languages\file_for_translate.txt'
    f_read = codecs.open(file_name, "r", "utf-8")
    f_write = codecs.open(file_for_translate_name, "a", "utf-8")
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
    f = codecs.open(file_name, "r", "utf-8")
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


def make_translate_to_language__file_to_format_file(translate_file_name, english_file_name, language):
    """
    :param translate_file_name: a name of translate file
    :param english_file_name: a name of the translate file before translate - in english
    :return: a name of a new translate file  in the appropriate format
    """
    script_dir = os.path.dirname(__file__)
    format_file_name = script_dir + f'\\languages\\translate_to_{language}_file_in_format.txt'
    translate_file = codecs.open(translate_file_name, 'r', "utf-8")
    english_file = codecs.open(english_file_name, 'r', "utf-8")
    format_file = codecs.open(format_file_name, 'a', "utf-8")

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
    script_dir = os.path.dirname(__file__)
    f_eb_name = script_dir + r'\file_translate_to_hebrew.txt'
    f_eb = codecs.open(f_eb_name, 'w', "utf-8")
    f_eb.write(result)
    return f_eb_name


def translate_to_another_language(translate_file_name, language):
    """
    :param translate_file_name: a file with text in English
    :return: a name of the translate file to language
    """
    translator = Translator()
    f_en = open(translate_file_name, 'r')
    data = f_en.read()
    result = translator.translate(data, src='en', dest=language).text
    script_dir = os.path.dirname(__file__)
    f_language_name = script_dir + f'\\languages\\file_translate_to_{language}.txt'
    f_language = codecs.open(f_language_name, 'w', "utf-8")
    f_language.write(result)
    return f_language_name


def get_language_question_collection(language):
    """
    :param language: of the question collection that we need for exe: 'he', 'en', 'fr'
    :return: a question collection in the language 'language'
    """
    script_dir = os.path.dirname(__file__)
    translate_format_file_name = f'translate_to_{language}_file_in_format.txt'
    translate_format_file = script_dir + f'\\languages\\{translate_format_file_name}'
    languages = script_dir + '\\languages'
    for root, dir, files in os.walk(languages):
        if translate_format_file_name in files:
            return load_question_data(translate_format_file)
    english_file = script_dir + f'\\languages\\english.txt'
    for_translate_file = make_file_for_translate(english_file)
    translate_file_in_language = translate_to_another_language(for_translate_file, language)
    format_file_in_language = make_translate_to_language__file_to_format_file(translate_file_in_language, english_file,
                                                                              language)
    os.remove(for_translate_file)
    os.remove(translate_file_in_language)
    return load_question_data(format_file_in_language)


if __name__ == '__main__':
    # script_dir = os.path.dirname(__file__)
    # english_file1 = script_dir + r'\english.txt'
    # for_translate_file1 = make_file_for_translate(english_file1)
    # translate_file1 = translate_to_hebrew(for_translate_file1)
    # translate_file1 = translate_to_another_language(for_translate_file1, 'fr')
    # format_file1 = make_translate_to_language__file_to_format_file(translate_file1, english_file1, 'fr')
    # qtree1 = load_question_data(format_file1)
    qtree1 = get_language_question_collection('fr')
    qtree2 = get_language_question_collection('he')
