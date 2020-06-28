'''
Creates the central message bus that binds publishers to subscribers.
It is accomplished by funneling a universal subscriber to a universal publisher.
'''

import zmq
from config.config import MBUS_SOCKET_PATH_SUB, MBUS_SOCKET_PATH_PUB


class MessageBus:

    @staticmethod
    def run():

        try:
            zmq_context = zmq.Context()

            sub_side = zmq_context.socket(zmq.SUB)
            sub_side.bind(MBUS_SOCKET_PATH_SUB)
            sub_side.setsockopt(zmq.SUBSCRIBE, "".encode())

            pub_side = zmq_context.socket(zmq.PUB)
            pub_side.bind(MBUS_SOCKET_PATH_PUB)

            zmq.proxy(sub_side, pub_side)
        except Exception as e:
            # print(e)
            # Will fail on startup
            pass
        finally:
            sub_side.close()
            pub_side.close()
            zmq_context.term()
