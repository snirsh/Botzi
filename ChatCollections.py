from Chat import *


class ChatCollections:
    def __init__(self):
        self._chats = {}  # dictionary save the chat by id_recipient ?

    def add_chat(self, id_recipient):
        self._chats[id_recipient] = Chat(id_recipient)

    def is_exist(self, id_recipient):
        return id_recipient in self._chats

    def get_chat(self, id_recipient):
        # create chat if the user not exists in history
        if not self.is_exist(id_recipient):
            new_chat = Chat(id_recipient)
            self._chats[id_recipient] = new_chat

        return self._chats[id_recipient]

    def remove_chat(self, recipient_id):
        if recipient_id in self._chats:
            self._chats.pop(recipient_id)

    def delete_chat(self):
        pass
