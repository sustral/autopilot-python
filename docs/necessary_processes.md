## Necessary Processes

Onboard Remote Vehicle:

   - MessageBus.run()
   - VehicleZMQ.run_feed_in()
   - VehicleZMQ.run_feed_out()
   - Barometer.run()
   - IMU.run("mpu")
   - IMU.run("lsm")
   - Motor.run(0, "fr")
   - Motor.run(1, "bl")
   - Motor.run(2, "fl")
   - Motor.run(3, "br")
