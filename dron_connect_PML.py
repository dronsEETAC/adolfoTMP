import json
import math
import threading
import time

from pymavlink import mavutil

'''def _get_telemetry_info(self):
    telemetry_info = {
        'lat': self.vehicle.location.global_frame.lat,
        'lon': self.vehicle.location.global_frame.lon,
        'heading': self.vehicle.heading,
        'groundSpeed': self.vehicle.groundspeed,
        'altitude': self.vehicle.location.global_relative_frame.alt,
        'battery': self.vehicle.battery.level,
        'state': self.state
    }
    return telemetry_info
'''

def _send_telemetry_info(self, sending_topic):
    print('empiezo a enviar datos de telemetria ', self.state)
    frequency_hz = 2
    self.vehicle.mav.command_long_send(
        self.vehicle.target_system,  self.vehicle.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
        mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT, # The MAVLink message ID
        1e6 / frequency_hz, # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
        0, 0, 0, 0, # Unused parameters
        0, # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
    )

    while self.state != 'desconectado':
        #msg = self.vehicle.recv_match(type='AHRS2', blocking= True).to_dict()
        msg = self.vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking= False)
        if msg:
            msg = msg.to_dict()
            self.lat = float(msg['lat'] / 10 ** 7)
            self.lon = float(msg['lon'] / 10 ** 7)
            self.alt = float(msg['relative_alt']/1000)
            vx = float(msg['vx'])
            vy = float(msg['vy'])
            self.groundSpeed = math.sqrt(vx * vx + vy * vy) / 100

            telemetry_info = {
                'lat': self.lat,
                'lon': self.lon,
                'alt': self.alt,
                'state': self.state,
                'groundSpeed': self.groundSpeed
            }
            self.lock.acquire()
            self.client.publish(sending_topic + '/telemetryInfo', json.dumps(telemetry_info))
            # print ("estado", self.state)
            self.lock.release()
        time.sleep(0.25)


# Some more small functions
def _connect(self, sending_topic, connection_string ):
    print ('vamos a conectar')
    print (connection_string)
    self.vehicle = mavutil.mavlink_connection(connection_string, baud=57600)
    self.vehicle.wait_heartbeat()
    print('conectado')
    self.state = "conectado"
    y = threading.Thread(target=self._send_telemetry_info, args=[sending_topic ])
    y.start()



def connect(self, sending_topic, connection_string):
    y = threading.Thread(target=self._connect, args=[sending_topic, connection_string])
    y.start()

