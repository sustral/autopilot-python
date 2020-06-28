'''
Registers itself as a ZMQ publisher and enables callers to send messages.
Any publisher can publish messages with any topic.
'''

import zmq
from config.config import MBUS_SOCKET_PATH_SUB
import pickle


class Publisher:

    def __init__(self):
        self.zmq_context = zmq.Context()
        self.pub_socket = self.zmq_context.socket(zmq.PUB)
        self.pub_socket.connect(MBUS_SOCKET_PATH_SUB)

    def send(self, topic, message):

        topic = topic.encode() # To bytes
        message = pickle.dumps(message)

        self.pub_socket.send_multipart([topic, message])

    def close(self):
        self.pub_socket.close()
        self.zmq_context.term()
