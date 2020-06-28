'''
Registers itself as a subscriber to a ZMQ topic and enables the caller to receive tagged messages.
It can handle multiple topics at a time, which eliminates the need to monitor multiple sockets.
'''

import zmq
from config.config import MBUS_SOCKET_PATH_PUB
import pickle


class Subscriber:

    def __init__(self, topics=None):
        if topics is None:
            topics = [""]

        self.zmq_context = zmq.Context()
        self.sub_socket = self.zmq_context.socket(zmq.SUB)
        self.sub_socket.connect(MBUS_SOCKET_PATH_PUB)

        for t in topics:
            # Topic name needs to be in bytes
            self.sub_socket.setsockopt(zmq.SUBSCRIBE, t.encode())

    def recv(self):
        topic, message = self.sub_socket.recv_multipart()

        topic = topic.decode()
        message = pickle.loads(message)

        return topic, message

    def recv_noblock(self):
        try:
            topic, message = self.sub_socket.recv_multipart(flags=zmq.NOBLOCK)

            topic = topic.decode()
            message = pickle.loads(message)

            return topic, message

        except zmq.ZMQError as e:
            # Expected, we just want this to fail quietly
            return None, None

    def close(self):
        self.sub_socket.close()
        self.zmq_context.term()
