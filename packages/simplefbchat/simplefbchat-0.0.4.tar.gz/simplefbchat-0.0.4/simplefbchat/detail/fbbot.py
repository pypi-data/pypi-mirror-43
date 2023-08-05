from fbchat import Client
from fbchat.models import *

class FbBot(Client):
    def __init__(self, name, password, received_queue):
        super().__init__(name, password)
        self.received_queue = received_queue

    def onMessage(self, message_object, author_id, **kwargs):
        self.received_queue.put((message_object.text, author_id))

    def onInbox(self, **kwargs):
        threads = (self.fetchThreadList(thread_location=ThreadLocation.PENDING)
                   + self.fetchThreadList(thread_location=ThreadLocation.OTHER)
                   )

        for node in threads:
            self.moveThreads(ThreadLocation.INBOX, node.uid)
            msgs = self.fetchThreadMessages(thread_id=node.uid)
            for msg in msgs:
                self.onMessage(msg, node.uid)

    def send_message(self, text, uid):
        if uid != self.uid:
            self.send(Message(text=text), uid)

