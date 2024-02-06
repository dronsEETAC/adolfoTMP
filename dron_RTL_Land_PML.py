import threading
import time
from pymavlink import mavutil

def _goDown(self, mode):

    # Get mode ID
    mode_id = self.vehicle.mode_mapping()[mode]
    self.vehicle.mav.set_mode_send(
        self.vehicle.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)
    arm_msg = self.vehicle.recv_match(type='COMMAND_ACK', blocking=True, timeout=3)
    self.vehicle.motors_disarmed_wait()
    self.state = "conectado"


def RTL(self):
    self.state = 'retornando'
    y = threading.Thread(target=self._goDown, args=['RTL', ])
    y.start()




def Land(self):
    self.state = 'aterrizando'
    y = threading.Thread(target=self._goDown, args=['LAND', ])
    y.start()