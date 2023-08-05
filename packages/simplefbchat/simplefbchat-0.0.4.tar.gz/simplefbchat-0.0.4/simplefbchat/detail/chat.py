import threading
import queue
from .fbbot import FbBot

class SimpleFbMessage:
    def __init__(self, bot, text, author_uid):
        self.__bot = bot
        self.text = text
        self.author_uid = author_uid

    def reply(self, text):
        self.__bot.send(text, self.author_uid)

class Chat(threading.Thread):

    def __init__(self, user, password):
        super().__init__()
        self.__user = user
        self.__password = password
        self.__received = queue.Queue()
        self.start()

    def run(self):
        self.__fbbot = FbBot(self.__user, self.__password, self.__received)
        self.__fbbot.listen()

    def receive(self):
        received = self.__received.get()
        return SimpleFbMessage(self, received[0], received[1])

    def send(self, text, author_id):
        self.__fbbot.send_message(text, author_id)

