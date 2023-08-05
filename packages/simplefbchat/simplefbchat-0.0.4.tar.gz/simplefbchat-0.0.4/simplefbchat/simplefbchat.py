from .detail.chat import Chat

class SimpleFbChat():

    def __init__(self, user, password):
        self.__chat = Chat(user, password)

    def receive(self):
        return self.__chat.receive()

    def send(self, text, author_id):
        self.__chat.send(text, author_id)

