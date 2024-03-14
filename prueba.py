import time

import dronekit
from dronekit import connect
print ('voy a conectarme')
vehicle = connect('127.0.0.1:5763', wait_ready=False, baud=115200)
vehicle.wait_ready(True, timeout=5000)

print ("Connected")

vehicle.armed = True # armem el dron

while not vehicle.armed:
    pass

while vehicle.armed:
    print (vehicle.mode.name)
    print ("Altitud", vehicle.location.global_relative_frame.alt)
    print ("Heading", vehicle.heading)
    time.sleep(2)

vehicle.close()


