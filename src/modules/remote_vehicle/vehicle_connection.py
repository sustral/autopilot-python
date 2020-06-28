'''
DEPRECATED
Binds the interdevice message bus to the internal message bus via the socket library.
'''

import socket
import pickle
from modules.internal_bus.publisher import Publisher
from modules.internal_bus.subscriber import Subscriber
from config.config import ADDRESS_DATA, ADDRESS_INST, TOPICS_DATA, TOPICS_INST, VEHICLE_MODE


class VehicleConnection:

    @staticmethod
    def run_feed_in():

        # If in vehicle mode, this will ingest motor instructions
        # If not, this will ingest sensor data

        address = ADDRESS_INST if VEHICLE_MODE else ADDRESS_DATA

        pub_socket = Publisher()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if VEHICLE_MODE:
            sock.bind(address)
            sock.listen(1)

        while True:

            if VEHICLE_MODE:
                sock_or_conn, _ = sock.accept()
            else:
                sock.connect(address)
                sock_or_conn = sock

            full_msg = b''
            new_msg = True

            try:
                while True:
                    # Read in 16 bytes at a time
                    msg = sock_or_conn.recv(16)
                    if not msg:
                        break

                    if new_msg:
                        msglen = int(msg[:10])
                        new_msg = False

                    full_msg += msg

                    if len(full_msg) - 10 == msglen:
                        obj_data = pickle.loads(full_msg[10:])

                        topic = obj_data["topic"]
                        message = obj_data["message"]

                        pub_socket.send(topic, message)

                        full_msg = b''
                        new_msg = True
            except Exception as e:
                # fail quietly
                pass
            finally:
                if VEHICLE_MODE:
                    sock_or_conn.close()

    @staticmethod
    def run_feed_out():

        # If in vehicle mode, this will emit sensor data
        # If not, this will emit motor instructions

        listen_topics = TOPICS_DATA if VEHICLE_MODE else TOPICS_INST
        address = ADDRESS_DATA if VEHICLE_MODE else ADDRESS_INST

        sub_socket = Subscriber(listen_topics)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if VEHICLE_MODE:
            sock.bind(address)
            sock.listen(1)

        while True:

            if VEHICLE_MODE:
                sock_or_conn, _ = sock.accept()
            else:
                sock.connect(address)
                sock_or_conn = sock

            try:
                while True:
                    topic, message = sub_socket.recv()

                    obj_data = {
                        "topic": topic,
                        "message": message
                    }

                    msg = pickle.dumps(obj_data)
                    msg = bytes('{:<10}'.format(len(msg)), "utf-8") + msg
                    sock_or_conn.sendall(msg)

            except socket.error as e:
                # fail quietly
                pass
            finally:
                if VEHICLE_MODE:
                    sock_or_conn.close()
