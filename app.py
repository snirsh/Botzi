# Python libraries that we need to import for our bot
import os
import requests

import random
from itertools import count
import json
from flask import Flask, request
# from pymessenger import Bot
from pymessenger.bot import Bot
from ChatCollections import *
from Question import *
from Chat import *
from QuestionTree import *
import DataLoader as ql
# from DataValidator import valid_answer
from FirestoreDb import FirebaseDb
from BotController import BotController

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

CHATS = ChatCollections()
TREE = QuestionTree()
DataBase = FirebaseDb()
bot_controller = BotController(DataBase)


# WIT_ACCESS_TOKEN = os.environ['WIT_ACCESS_TOKEN']
# my_resp = [['NGO', 'VOLUNTEER'], ['MALE', 'FEMALE'], ['YES', 'NO']]
# question = ["Hello!!\n Are You a NGO or VOLUNTEER?", "Are you a male/female?", "Do you have a car?"]

flag = True
bot: Bot = Bot(ACCESS_TOKEN)

# BLOCK
# wit_client = Wit(WIT_ACCESS_TOKEN)
# resp = wit_client.message("Hi there!")
# print('Yay! got Wit.ai response: ' + str(resp))

# @app.route('/orgnization/campaigns', methods=['GET'])


@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)

    output = request.get_json()
    message = output.get('entry')[0].get('messaging')[0]

    if message.get('message'):
        recipient_id = message['sender']['id']
        sender_id = message['recipient']['id']
        ans = message['message'].get('text')

        bot_controller.next_response(recipient_id, sender_id, ans)

        return "Message Processed"


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def start(port=5000):
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
