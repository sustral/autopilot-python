'''
Binds the interdevice message bus to the internal message bus via ZMQ.
ZMQ is more stable and supports a higher throughput than Python's socket library.
'''

import zmq
from config.config import ZMQ_DATA, ZMQ_INST, TOPICS_DATA, TOPICS_INST, VEHICLE_MODE
from config.config import MBUS_SOCKET_PATH_SUB, MBUS_SOCKET_PATH_PUB


class VehicleZMQ:

    @staticmethod
    def run_feed_in():

        # If in vehicle mode, this will ingest motor instructions
        # If not, this will ingest sensor data

        try:

            zmq_context = zmq.Context()

            sub_side = zmq_context.socket(zmq.SUB)
            if VEHICLE_MODE:
                sub_side.bind(ZMQ_INST)
                for t in TOPICS_INST:
                    sub_side.setsockopt(zmq.SUBSCRIBE, t.encode())
            else:
                sub_side.connect(ZMQ_DATA)
                for t in TOPICS_DATA:
                    sub_side.setsockopt(zmq.SUBSCRIBE, t.encode())

            pub_side = zmq_context.socket(zmq.PUB)
            pub_side.connect(MBUS_SOCKET_PATH_SUB)

            zmq.proxy(sub_side, pub_side)

        except Exception as e:
            # fail quietly
            pass
        finally:
            sub_side.close()
            pub_side.close()
            zmq_context.term()

    @staticmethod
    def run_feed_out():

        # If in vehicle mode, this will emit sensor data
        # If not, this will emit motor instructions

        try:

            zmq_context = zmq.Context()

            sub_side = zmq_context.socket(zmq.SUB)
            sub_side.connect(MBUS_SOCKET_PATH_PUB)
            if VEHICLE_MODE:
                for t in TOPICS_DATA:
                    sub_side.setsockopt(zmq.SUBSCRIBE, t.encode())
            else:
                for t in TOPICS_INST:
                    sub_side.setsockopt(zmq.SUBSCRIBE, t.encode())

            pub_side = zmq_context.socket(zmq.PUB)
            if VEHICLE_MODE:
                pub_side.bind(ZMQ_DATA)
            else:
                pub_side.connect(ZMQ_INST)

            zmq.proxy(sub_side, pub_side)

        except Exception as e:
            # fail quietly
            pass
        finally:
            sub_side.close()
            pub_side.close()
            zmq_context.term()
