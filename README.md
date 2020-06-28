# Autopilot Python

This program shuttles sensor data from the Navio 2 equipped Raspberry Pi (navio) to the Nvidia Jetson Xavier (brain)
and shuttles motor instructions in the opposite direction. No further code is needed on board the navio.

The Navio 2 equipped Raspberry Pi contains a suite of sensors required for aircraft but it does not possess the compute
power required to run ML models. The Nvidia Jetson Xavier is a high density compute module that is capable of running
(reasonable) ML models, but does not come with sensors. A combination of the two yields a relatively affordable, powerful,
and easy to assemble airborne compute platform.

## Design

An instance of this program must be run on both the navio and the brain (with different configs). In order to automatically
start the necessary processes on the navio, a systemd configuration is provided in `src/ops`.

This software is comprised of three components:

1. Internal Message Bus
   - This bus is built on ZMQ and uses IPC to communicate
   - Uses custom Subscribers and Publishers 

2. Interdevice Message Bus
   - Links the internal buses of the navio and of the brain using tcp sockets

3. Driver Wrappers (only on navio)
   - Wraps the sensor and pwm drivers (some drivers are modified) and constantly pushes/pulls data from the internal bus

## Misc

   - `src/tools/navio` contains a utility that calibrates all motors to exact duty cycles (1000 - 2000 standard).
