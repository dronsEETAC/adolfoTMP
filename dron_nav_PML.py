'''
Coleccion de métodos para la navegación según los puntos cardinales.
El dron debe estar en estado 'volando'
Para iniciar la navegación debe ejecutarse el método startGo,
que pone en marcha el thread que mantiene el rumbo.
El rumbo puede cambiar mediante el método go que recibe como parámetro
el nuevo rumbo (north, south, etc).
Para acabar la navegación hay que ejecutar el método stopGo

'''
import threading
import time
from pymavlink import mavutil


def _prepare_command(self, velocity_x, velocity_y, velocity_z):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg =  mavutil.mavlink.MAVLink_set_position_target_global_int_message(
        10,  # time_boot_ms (not used)
        self.vehicle.target_system,
        self.vehicle.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0,
        0,
        0,  # x, y, z positions (not used)
        velocity_x,
        velocity_y,
        velocity_z,  # x, y, z velocity in m/s
        0,
        0,
        0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0,
        0,
    )  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    return msg


def _startGo(self):
    self.cmd = self._prepare_command(0, 0, 0)
    while self.going:
        self.vehicle.mav.send(self.cmd)
        time.sleep(1)
    self.cmd = self._prepare_command(0, 0, 0)
    time.sleep(1)
def startGo(self):
    if self.state == 'volando':
        self.going = True
        y = threading.Thread(target=self._startGo)
        y.start()
def stopGo(self):
    self.going = False
def go(self, direction):
    if self.going:
        speed = 1
        if direction == "North":
            self.cmd = self._prepare_command(speed, 0, 0)  # NORTH
        if direction == "South":
            self.cmd = self._prepare_command(-speed, 0, 0)  # SOUTH
        if direction == "East":
            self.cmd = self._prepare_command(0, speed, 0)  # EAST
        if direction == "West":
            self.cmd = self._prepare_command(0, -speed, 0)  # WEST
        if direction == "NorthWest":
            self.cmd = self._prepare_command(speed, -speed, 0)  # NORTHWEST
        if direction == "NorthEast":
            self.cmd = self._prepare_command(speed, speed, 0)  # NORTHEST
        if direction == "SouthWest":
            self.cmd = self._prepare_command(-speed, -speed, 0)  # SOUTHWEST
        if direction == "SouthEast":
            self.cmd = self._prepare_command(-speed, speed, 0)  # SOUTHEST
        if direction == "Stop":
            self.cmd = self._prepare_command(0, 0, 0)  # STOP