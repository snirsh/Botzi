
import os
from Bot.QuestionTree import QuestionTree
# from Bot.DataValidator import *
from googletrans import Translator
import codecs

USER_TYPES = ["volunteer", "campaign", "association"]
END_FILE_SIGN = "END_FILE"
EMPTY_SIGN_T = '~'


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
    script_dir = os.path.dirname(__file__)
    file_for_translate_name = script_dir + r'/languages/file_for_translate.txt'
    f_read = codecs.open(file_name, "r", "utf-8")
    f_write = codecs.open(file_for_translate_name, "a", "utf-8")

    def split_value(value):
        value = value.split(':')
        value = f'{value[1].strip()}\n'
        if value == "\n":
            value = f'{EMPTY_SIGN_T}\n'
        return value

    while f_read and f_write:
        last_question = f_read.readline()
        if last_question.strip() == END_FILE_SIGN:
            f_read.close()
            f_write.close()
            flag = False
            break
        if last_question.strip() == "":
            continue
        if last_question:  # if its not the end of the file
            answer_to = f_read.readline()
            question = f_read.readline()
            answers = f_read.readline()
            key_value = f_read.readline()

            last_question = split_value(last_question)

            answer_to = split_value(answer_to)

            question = question.split(':')
            question = f'{question[1].strip()}\n'
            if question == "":
                raise ValueError("error: no question text")

            answers = split_value(answers)

            key_value = split_value(key_value)

            f_write.write(last_question)
            f_write.write(answer_to)
            f_write.write(question)
            f_write.write(answers)

        else:
            f_read.close()
            f_write.close()
            flag = False
            break

    # if flag:
    #     f_read.close()
    #     f_write.close()
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
        if last_question.strip() == END_FILE_SIGN:
            f.close()
            break
        if last_question.strip() == "":
            continue
        if last_question:  # if its not the end of the file
            answer_to = f.readline()
            question = f.readline()
            answers = f.readline()
            key_value = f.readline()

            last_question = last_question.split(':')
            last_question = last_question[1].strip()

            answer_to = answer_to.split(':')
            answer_to = answer_to[1].strip()

            question = question.split(':')
            question = question[1].strip()
            if question.strip() == "":
                raise ValueError("error: no question text")

            answers = answers.split(':')
            answers = answers[1].strip()
            if len(answers) > 1 and answers != "":
                answers = answers.split(',')
                for i in range(len(answers)):
                    answers[i] = answers[i].strip()
            else:
                answers = None

            key_value = key_value.split(':')
            key_value = key_value[1].strip()

            question_tree.add_question_node(last_question, question, key_value, answer_to, answers)

        else:
            f.close()
            break

    f.close()
    return question_tree


def make_translate_to_language__file_to_format_file(translate_file_name, english_file_name, language):
    """
    :param language:
    :param translate_file_name: a name of translate file
    :param english_file_name: a name of the translate file before translate - in english
    :return: a name of a new translate file  in the appropriate format
    """
    script_dir = os.path.dirname(__file__)
    format_file_name = script_dir + rf'/languages/translate_to_{language}_file_in_format.txt'
    translate_file = codecs.open(translate_file_name, 'r', "utf-8")
    english_file = codecs.open(english_file_name, 'r', "utf-8")
    format_file = codecs.open(format_file_name, 'a', "utf-8")

    def get_answer(answer):
        if answer.strip() == f'{EMPTY_SIGN_T}':
            return "\n"
        return answer

    while translate_file and english_file and format_file:

        translate_last_question = translate_file.readline()
        english_last_question = english_file.readline()
        while english_last_question.strip() == "":
            english_last_question = english_file.readline()

        if translate_last_question and english_last_question:  # if its not the end of the file

            translate_answer_to = translate_file.readline()
            translate_question = translate_file.readline()
            translate_answers = translate_file.readline()

            # if translate_last_question == '\n':
            #     translate_last_question = '"\n'
            # if translate_answer_to == '\n':
            #     translate_answer_to = '"\n'
            # if translate_question == '\n':
            #     translate_question = '"\n'
            # if translate_answers == '\n':
            #     translate_answers = '"\n'
            #
            # if translate_last_question == "" or not translate_last_question[-1] == "\n":
            #     translate_last_question += '\n'
            # if translate_answer_to == "" or not translate_answer_to[-1] == "\n":
            #     translate_answer_to += '\n'
            # if translate_question == "" or not translate_question[-1] == "\n":
            #     translate_question += '\n'
            # if translate_answers == "" or not translate_answers[-1] == "\n":
            #     translate_answers += '\n'

            english_answer_to = english_file.readline()
            english_question = english_file.readline()
            english_answers = english_file.readline()
            english_key_value = english_file.readline()

            english_last_question = english_last_question.split(':')
            # if len(english_last_question) > 1 and '"' not in english_last_question[1]:
            english_last_question = f'{english_last_question[0].strip()}:{get_answer(translate_last_question)}'

            english_answer_to = english_answer_to.split(':')
            english_answer_to = f'{english_answer_to[0].strip()}:{get_answer(translate_answer_to)}'

            english_question = english_question.split(':')
            english_question = f'{english_question[0].strip()}:{get_answer(translate_question)}'

            english_answers = english_answers.split(':')
            english_answers = f'{english_answers[0].strip()}:{get_answer(translate_answers)}'

            format_file.write(english_last_question)
            format_file.write(english_answer_to)
            format_file.write(english_question)
            format_file.write(english_answers)
            format_file.write(english_key_value)

        else:
            format_file.write(END_FILE_SIGN + "\n")
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
    f_eb_name = script_dir + r'/file_translate_to_hebrew.txt'
    f_eb = codecs.open(f_eb_name, 'w', "utf-8")
    f_eb.write(result)
    return f_eb_name


def translate_to_another_language(translate_file_name, language):
    """
    :param language:
    :param translate_file_name: a file with text in English
    :return: a name of the translate file to language
    """
    translator = Translator()
    f_en = open(translate_file_name, 'r')
    data = f_en.read()
    result = translator.translate(data, src='en', dest=language).text
    script_dir = os.path.dirname(__file__)
    f_language_name = script_dir + rf'/languages/file_translate_to_{language}.txt'
    f_language = codecs.open(f_language_name, 'w', "utf-8")
    f_language.write(result)
    return f_language_name


def get_language_question_collection(language):
    """
    :param language: of the question collection that we need for exe: 'he', 'en', 'fr'
    :return: a question collection in the language 'language' if Google Translate does not recognize the language return
     a question collection in English
    """
    script_dir = os.path.dirname(__file__)
    # in english_file do not put ':' besides after the type of the data because we do split by that character to get the
    # data. only like that - last_question:Please enter your phone number - [xxx-xxxxxxx]
    # but not like that - last_question:Please enter your phone number : [xxx-xxxxxxx]
    # that's will make error in our algorithm
    # also in every data that he is empty put " , for exe: last_question:" (that's good - do only like that)
    #                                                      last_question: (that's bad - do not do like that,
    #                                                                                                 we are missing ")
    english_file = script_dir + rf'/languages/english.txt'
    if language == 'en':
        return load_question_data(english_file)
    try:
        translate_format_file_name = f'translate_to_{language}_file_in_format.txt'
        translate_format_file = script_dir + rf'/languages/{translate_format_file_name}'
        languages = script_dir + r'/languages'
        for root, dir, files in os.walk(languages):
            if translate_format_file_name in files:
                return load_question_data(translate_format_file)
        file_for_translate_name = 'file_for_translate.txt'
        for_translate_file = script_dir + rf'/languages/{file_for_translate_name}'
        flag = True
        for root, dir, files in os.walk(languages):
            if file_for_translate_name in files:
                flag = False
        if flag:
            for_translate_file = make_file_for_translate(english_file)
        translate_file_in_language = translate_to_another_language(for_translate_file, language)
        format_file_in_language = make_translate_to_language__file_to_format_file(
            translate_file_in_language,
            english_file,
            language
        )
        os.remove(translate_file_in_language)
        return load_question_data(format_file_in_language)
    except Exception:
        return load_question_data(english_file)


if __name__ == '__main__':
    # script_dir = os.path.dirname(__file__)
    # english_file1 = script_dir + r'\english.txt'
    # for_translate_file1 = make_file_for_translate(english_file1)
    # translate_file1 = translate_to_hebrew(for_translate_file1)
    # translate_file1 = translate_to_another_language(for_translate_file1, 'fr')
    # format_file1 = make_translate_to_language__file_to_format_file(translate_file1, english_file1, 'fr')
    # qtree1 = load_question_data(format_file1)
    # qtree1 = get_language_question_collection('fr')
    # qtree3 = get_language_question_collection('en')
    # qtree2 = get_language_question_collection('he')
    # qtree4 = get_language_question_collection('ja')
    # qtree5 = get_language_question_collection('hekjs')
    # qtree6 = get_language_question_collection('persian')
    # print('a')
    path = r"languages/english.txt"
    etree = get_language_question_collection("en")
    fq = etree.get_first_msg()
    next = etree.get_next_question(fq.get_question())
    nnext = etree.get_next_question(next.get_question())
    nnext = etree.get_next_question(nnext.get_question(), "volunteer")
    print(nnext.get_question())

