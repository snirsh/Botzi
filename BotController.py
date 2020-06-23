from ChatCollections import *
from QuestionTree import *
from pymessenger.bot import Bot
import DataLoader as dl
from DataValidator import DataValidator
import os


class BotController:

    def __init__(self, db):
        ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
        self._bot = Bot(ACCESS_TOKEN)
        self._db = db
        self._chat_history = ChatCollections()
        self._qtree = QuestionTree()
        self._data_validator = DataValidator(self._db)
        dl.initialize_static_questions(self._qtree)

    def next_response(self, recipient_id, sender_id, ans):
        chat = self._chat_history.get_chat(recipient_id)
        is_chat_empty = chat.is_empty()

        # answer management:
        question_str = chat.get_last_qstn()
        last_question = self._qtree.find_question(question_str)
        if not is_chat_empty:
            chat.add_to_history(recipient_id, ans, last_question.get_key())

        print(f'last_question: {question_str}')
        print(f'answer: {ans}')
        print(f'nums of msgs: {chat.get_msgs_num()}')
        is_valid_ans = True
        if chat.get_msgs_num() >= 3:
            try:
                self._data_validator.valid_answer(ans, last_question.get_key(), chat)
            except ValueError as err:
                is_valid_ans = False
                self._send_message(recipient_id, err.__str__())

        # question management:
        if is_chat_empty:
            cur_qstn = self._qtree.get_first_msg()
        elif not is_valid_ans:
            # self._send_message(recipient_id, "invalid response")
            cur_qstn = self._qtree.find_question(question_str)
        elif self._qtree.is_close(question_str):
            cur_qstn = self._qtree.get_next_question(question_str, ans)
        else:
            cur_qstn = self._qtree.get_next_question(question_str)

        if cur_qstn is not None:
            chat.add_to_history(sender_id, cur_qstn.get_question(), "")

        finished = self._manage_questions(recipient_id, cur_qstn)

        if finished:
            chat.update_final_result()
            print(chat.get_final_result())
            if len(chat.get_final_result()) != 0:
                self._db.add_collection(chat.get_p_type(), chat.get_final_result())
                self._chat_history.remove_chat(recipient_id)

    def _manage_questions(self, recipient_id, cur_qstn):
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

