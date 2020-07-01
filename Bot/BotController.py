from pymessenger.bot import Bot
from pymessenger.graph_api import FacebookGraphApi

from Bot.ChatCollections import ChatCollections
from Bot.OpenQuestion import OpenQuestion
from Bot.CloseQuestion import CloseQuestion
from Bot.QuestionTree import QuestionTree
from Bot import DataLoader as dl
from Bot.DataValidator import DataValidator
import os
import requests
import json


class BotController:

    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

    def __init__(self, db):
        self._bot = Bot(BotController.ACCESS_TOKEN)
        self._fb = FacebookGraphApi(BotController.ACCESS_TOKEN)
        self._db = db
        self._chat_history = ChatCollections()
        self._qtree = QuestionTree()
        self._data_validator = DataValidator(self._db)
        dl.initialize_static_questions(self._qtree)
        self._has_permission = False

    def first_response(self, recipient_id, sender_id):

        chat = self._chat_history.get_chat(recipient_id)

        pdetails = self._get_personal_details(recipient_id)

        if not pdetails.get("error"):
            self._has_permission = True
            lan = pdetails.get("locale")
            if lan:
                lan = lan.split("_")[0]
            else:
                lan = "en"
            self._qtree = dl.get_language_question_collection(lan)
            cur_qstn = self._qtree.get_first_msg()

            name = f'{pdetails.get("first_name")} {pdetails.get("last_name")}'
            greeting_message = f'{cur_qstn.get_question()} {name}!'
            chat.add_to_final_result('name', f'{name}')

            print(greeting_message)
            self._send_message(recipient_id, greeting_message)

            cur_qstn = self._qtree.get_next_question(cur_qstn.get_question())
            cur_qstn = self._qtree.get_next_question(cur_qstn.get_question())
            self._manage_questions_sending(recipient_id, cur_qstn)
            # self._send_quick_resp(recipient_id, cur_qstn.get_question(), cur_qstn.get_possible_answers())

            chat.add_to_history(sender_id, cur_qstn.get_question(), "")
        else:
            self._qtree = dl.get_language_question_collection("en")
            cur_qstn = self._qtree.get_first_msg()

            greeting_message = f'{cur_qstn.get_question()}!'

            print(greeting_message)
            self._send_message(recipient_id, greeting_message)

            cur_qstn = self._qtree.get_next_question(cur_qstn.get_question())
            self._manage_questions_sending(recipient_id, cur_qstn)
            # self._send_quick_resp(recipient_id, cur_qstn.get_question(), cur_qstn.get_possible_answers())

            chat.add_to_history(sender_id, cur_qstn.get_question(), "")

        return "Message Processed"

    def next_response(self, recipient_id, sender_id, ans):
        # get chat history and relevant questions:
        chat = self._chat_history.get_chat(recipient_id)

        # check if this is the start of the conversation
        is_chat_empty = chat.is_empty()

        # answer management - parse the answer:
        if is_chat_empty:
            self.first_response(recipient_id, sender_id)
            return "Message Processed"
        else:
            question_str = chat.get_last_qstn()
            last_question = self._qtree.find_question(question_str)
            chat.add_to_history(recipient_id, ans, last_question.get_key())

        print(f'last_question: {question_str}')  # TODO: remove
        print(f'answer: {ans}')
        print(f'nums of msgs: {chat.get_msgs_num()}')
        is_valid_ans = True

        if chat.get_msgs_num() >= 2:
            try:
                self._data_validator.valid_answer(ans, last_question.get_key(), chat)
            except ValueError as err:
                is_valid_ans = False
                self._send_message(recipient_id, err.__str__())

        # if is_chat_empty:
        #     cur_qstn = self._qtree.get_first_msg()
        if not is_valid_ans:
            cur_qstn = self._qtree.find_question(question_str)
        elif self._qtree.is_close(question_str):
            cur_qstn = self._qtree.get_next_question(question_str, ans)
            print(f'next questions will be closed: {cur_qstn}')
        else:
            cur_qstn = self._qtree.get_next_question(question_str)
            print(f'next question will be opened: {cur_qstn}')

        if cur_qstn is not None:
            chat.add_to_history(sender_id, cur_qstn.get_question(), "")

        finished = self._manage_questions_sending(recipient_id, cur_qstn)

        if finished:
            chat.update_final_result()
            print(chat.get_final_result())
            if len(chat.get_final_result()) != 0:
                self._db.add_collection(chat.get_p_type(), chat.get_final_result())
                self._chat_history.remove_chat(recipient_id)

    def start(self):
        request_endpoint = '{0}/me/messenger_profile'.format(self._bot.graph_url)
        response = requests.post(
            request_endpoint,
            params=self._bot.auth_args,
            data=json.dumps({"get_started": {"payload": "first"}}),
            headers={'Content-Type': "application/json"}
        )
        result = response.json()
        self._bot.send_raw(response)
        return result

    def _get_personal_details(self, recipient_id):
        user_details_url = "https://graph.facebook.com/v2.6/%s" % recipient_id
        user_details_params = {
            'fields': 'first_name, last_name, locale, gender',
            'access_token': BotController.ACCESS_TOKEN
        }
        user_details = requests.get(user_details_url, user_details_params).json()
        print(user_details)

        # # my_text = 'Hey' + ' ' + user_details['first_name'] +' '+ user_details['last_name']
        # # print(user_details['locale'])  # THE LANGUAGE OF THE USER
        # # print(user_details['gender'])  # THE SEXE OF THE USER
        # user_ = UserProfileApi(self._fb)
        # print(user_.get(recipient_id, 'first_name'))
        return user_details

    def _manage_questions_sending(self, recipient_id, cur_qstn):
        """

        :param recipient_id:
        :param cur_qstn:
        :return: True if we finished to ask all the questions, False otherwise
        """
        if cur_qstn is None:
            self._send_message(recipient_id, "Thank you for signing up")
            return True

        if isinstance(cur_qstn, OpenQuestion):
            self._send_message(recipient_id, cur_qstn.get_question())
        elif isinstance(cur_qstn, CloseQuestion):
            self._send_quick_resp(recipient_id, cur_qstn.get_question(), cur_qstn.get_possible_answers())

        return False

    def _send_quick_resp(self, recipient_id, cur_qstn, options):
        # options = [STRING]

        # create a list of response
        responses = []
        for option in options:
            responses.append({
                "content_type": "text",
                "title": option,
                "payload": "verification"
            })

        # send a Quick response
        self._bot.send_message(recipient_id, {'text': cur_qstn, "quick_replies": responses})
        return "success"

    # uses PyMessenger to send response to user
    def _send_message(self, recipient_id, response):
        # sends user the text message provided via input response parameter
        self._bot.send_text_message(recipient_id, response)
        return "success"

