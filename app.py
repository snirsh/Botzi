# Python libraries that we need to import for our bot
import os
import requests

import random
from itertools import count
import json
from flask import Flask, request
from pymessenger import Bot
from pymessenger.bot import Bot
from QuestionsCollection import *
from ChatCollections import *
from Question import *
from Chat import *
from QuestionTree import *
import DataLoader as ql
from DataValidation import valid_answer
import FirestoreDb as FDB

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

CHATS = ChatCollections()
TREE = QuestionTree()

# WIT_ACCESS_TOKEN = os.environ['WIT_ACCESS_TOKEN']
# my_resp = [['NGO', 'VOLUNTEER'], ['MALE', 'FEMALE'], ['YES', 'NO']]
# question = ["Hello!!\n Are You a NGO or VOLUNTEER?", "Are you a male/female?", "Do you have a car?"]

flag = True
bot: Bot = Bot(ACCESS_TOKEN)

# BLOCK
# wit_client = Wit(WIT_ACCESS_TOKEN)
# resp = wit_client.message("Hi there!")
# print('Yay! got Wit.ai response: ' + str(resp))


# @app.route('/', methods=['GET'])
# def verify_fb():
#
#     if request.method == 'GET':
#         """Before allowing people to message your bot, Facebook has implemented a verify token
#         that confirms all requests that your bot receives came from Facebook."""
#         token_sent = request.args.get("hub.verify_token")
#         return verify_fb_token(token_sent)
#     # if the request was not get, it must be POST and we can just proceed with sending a message back to user


@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)

    output = request.get_json()
    id = output['entry'][0].get('id')  # TODO: TO GET ID NOT IN THIS FORM
    print(id)
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                print(output)
                # TODO: 1: Parsing the user message

                recipient_id = message['sender']['id']
                sender_id = message['recipient']['id']

                print(sender_id)  # TODO: debug purpose, delete later
                print(recipient_id)

                chat = CHATS.get_chat(recipient_id)
                is_chat_empty = chat.is_empty()

                # answer management:
                ans = message['message'].get('text')
                lst_msg = chat.get_last_qstn()

                if ans:
                    chat.add_to_history(recipient_id, ans)

                is_valid_ans = True
                if chat.get_msgs_num() > 3:
                    is_valid_ans = valid_answer(lst_msg, ans, chat)

                # question management:
                if ans == "work" and is_valid_ans is False:
                    print("NOT GOOD!!")
                else:
                    print("??????")
                if is_chat_empty:
                    cur_qstn = TREE.get_first_msg()
                elif not is_valid_ans:
                    send_message(recipient_id, "invalid response")
                    cur_qstn = TREE.find_question(lst_msg).get_qstn_obj()
                    print("!!!!!!")
                elif TREE.is_close(lst_msg):
                    cur_qstn = TREE.get_next_question(lst_msg, ans)
                else:
                    cur_qstn = TREE.get_next_question(lst_msg)

                if cur_qstn is not None:
                    chat.add_to_history(sender_id, cur_qstn.get_question())

                finished = manage_qstns(recipient_id, cur_qstn)

                if finished:
                    chat.update_final_result()
                    print(chat.get_final_result())
                    if len(chat.get_final_result()) != 0:
                        db = FDB.FirebaseDb()
                        db.add_collection(chat.get_p_type(), chat.get_final_result())
                        CHATS.remove_chat(recipient_id)

                # # TODO: 2: Saving the user message in a dictionary somewhere
                # # Waiting to receive a response
                # if COUNT < len(my_resp):
                # send_quick_resp(recipient_id, my_resp[COUNT])

                return "Message Processed"


def manage_qstns(recipient_id, cur_qstn):
    """

    :param recipient_id:
    :param cur_qstn:
    :return: True if we finished to ask all the questions, False otherwise
    """
    if cur_qstn is None:
        send_message(recipient_id, "Thank you for signing up")
        return True

    if isinstance(cur_qstn, OpenQuestion):
        send_message(recipient_id, cur_qstn.get_question())
    elif isinstance(cur_qstn, CloseQuestion):
        send_quick_resp(recipient_id, cur_qstn.get_question(), cur_qstn.get_possible_answers())

    return False


def verify_fb_token(token_sent):
    global COUNT
    COUNT = 0
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def send_quick_resp(recipient_id, cur_qstn, options):
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
    bot.send_message(recipient_id, {'text': cur_qstn, "quick_replies": responses})
    return "success"


# uses PyMessenger to send response to user
def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


def start(port=5000):
    ql.initialize_static_questions(TREE)
    app.run(port=port)

    request_endpoint = '{0}/me/messenger_profile'.format(bot.graph_url)
    response = requests.post(
        request_endpoint,
        params=bot.auth_args,
        data=json.dumps({"get_started": {"payload": "first"}}),
        headers={'Content-Type': "application/json"}
    )
    result = response.json()
    Bot.send_raw(response)


if __name__ == "__main__":
    q1 = TREE.get_first_msg()
    q2 = TREE.get_next_question(q1, "Volunteer")
