# Python libraries that we need to import for our bot
import os

import json
import requests

import json
from flask import Flask, request
from flask_cors import CORS

# from pymessenger import Bot
from pymessenger.bot import Bot
# from Bot.ChatCollections import *
# from Bot.QuestionTree import *

from FirestoreDb import FirebaseDb
from Bot.BotController import BotController

app = Flask(__name__)
CORS(app)

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

# CHATS = ChatCollections()
# TREE = QuestionTree()
DataBase = FirebaseDb()
bot_controller = BotController(DataBase)


# WIT_ACCESS_TOKEN = os.environ['WIT_ACCESS_TOKEN']
# my_resp = [['NGO', 'VOLUNTEER'], ['MALE', 'FEMALE'], ['YES', 'NO']]
# question = ["Hello!!\n Are You a NGO or VOLUNTEER?", "Are you a male/female?", "Do you have a car?"]

flag = True
# bot: Bot = Bot(ACCESS_TOKEN)


@app.route('/app/volunteer_matches/', methods=['GET'])
def volunteer_matchers():
    print("Front need me")
    if request.method == 'GET':
        print(request.args)
        print(request.data)
        print(request.json)
        id = request.args.get("volunteerID")
        matches = DataBase.get_campaigns_matches(id)
        response = {
            "volunteer_mail": id,
            "body": matches,
            "Yael": "I'm busy"  # TODO: remove
        }
        print(response)
        return response


@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)

    output = request.get_json()
    message = output.get('entry')[0].get('messaging')[0]

    # user details:
    recipient_id = message['sender']['id']
    sender_id = message['recipient']['id']

    if message.get('postback'):
        bot_controller.first_response(recipient_id, sender_id)
    if message.get('message'):
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
    bot_controller.start()


# if __name__ == "__main__":
#     q1 = TREE.get_first_msg()
#     q2 = TREE.get_next_question(q1, "Volunteer")
