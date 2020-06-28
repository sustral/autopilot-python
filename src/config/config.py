'''
Configures the message bus.
'''

# Set to 'True' if running on the navio equipped RPi,
# 'False' if running on the brain
VEHICLE_MODE = True

# IP address of navio equipped RPi, any open ports
# If using socket as interdevice bus (deprecated)
ADDRESS_INST = ("192.168.70.132", 7955)
ADDRESS_DATA = ("192.168.70.132", 7957)
# If using ZMQ as interdevice bus
ZMQ_INST = "tcp://192.168.70.132:7955"
ZMQ_DATA = "tcp://192.168.70.132:7957"

# Only change when adding features
TOPICS_INST = ["motor_inst", "leds_inst"]
TOPICS_DATA = ["baro_raw", "mpu_raw", "lsm_raw", "gps_raw"]

# Internal bus - labeled relative to bus
# Only change if the below files are already in use
MBUS_SOCKET_PATH_SUB = "ipc:///tmp/feeds_0"
MBUS_SOCKET_PATH_PUB = "ipc:///tmp/feeds_1"
