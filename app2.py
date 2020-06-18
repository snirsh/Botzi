# Python libraries that we need to import for our bot
import os
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

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

CHATS = ChatCollections()
QUESTIONS = QuestionsCollections()

# WIT_ACCESS_TOKEN = os.environ['WIT_ACCESS_TOKEN']
# my_resp = [['NGO', 'VOLUNTEER'], ['MALE', 'FEMALE'], ['YES', 'NO']]
# question = ["Hello!!\n Are You a NGO or VOLUNTEER?", "Are you a male/female?", "Do you have a car?"]

COUNT = 0
flag = True
bot: Bot = Bot(ACCESS_TOKEN)

# BLOCK
# wit_client = Wit(WIT_ACCESS_TOKEN)
# resp = wit_client.message("Hi there!")
# print('Yay! got Wit.ai response: ' + str(resp))


@app.rout('/', methods=['GET'])
def verify_fb():
    global COUNT

    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not get, it must be POST and we can just proceed with sending a message back to user


@app.route('/', methods=['POST'])
def receive_message():
    # get whatever message a user sent the bot
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

                # answer management:
                txt = message['message'].get('text')
                if txt:
                    chat.add_to_history(recipient_id, txt)

                # question management:
                lst_msg_num = chat.get_msgs_num()
                nxt_qstn = lst_msg_num+1

                cur_qstn = QUESTIONS.get_question(nxt_qstn)
                if cur_qstn != -1:
                    chat.add_to_history(sender_id, cur_qstn)

                manage_qstns(recipient_id, nxt_qstn, nxt_qstn)

                # # TODO: 2: Saving the user message in a dictionary somewhere
                # # Waiting to receive a response
                # if COUNT < len(my_resp):
                # send_quick_resp(recipient_id, my_resp[COUNT])

                return "Message Processed"


def manage_qstns(recipient_id, cur_qstn, msg_number):
    if msg_number >= QUESTIONS.question_number():
        send_message(recipient_id, "Thank you for signing up")
        return

    if isinstance(cur_qstn, OpenQuestion):
        send_message(recipient_id, cur_qstn.get_question())
    elif isinstance(cur_qstn, CloseQuestion):
        send_quick_resp(recipient_id, cur_qstn.get_question(), cur_qstn.get_possible_answers())


def verify_fb_token(token_sent):
    global COUNT
    COUNT = 0
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def increment():
    global COUNT
    COUNT = COUNT+1
# uses PyMessenger to send response to user


def send_quick_resp(recipient_id, cur_qstn, options):
    global COUNT
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
    increment()
    return "success"


# uses PyMessenger to send response to user
def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    dict_of_users = {}
    app.run()
