import threading
import time
from pymavlink import mavutil

def _takeOff(self, aTargetAltitude):
    self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component,
                                         mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, aTargetAltitude)

    while True:
        if self.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)
    self.state = "volando"


def takeOff(self, aTargetAltitude):
    y = threading.Thread(target=self._takeOff, args=[aTargetAltitude, ])
    y.start()