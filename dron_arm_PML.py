import threading
import time


from pymavlink import mavutil


def _arm(self):
    mode = 'GUIDED'

    # Check if mode is available
    if mode not in self.vehicle.mode_mapping():
        print('Unknown mode : {}'.format(mode))
        print('Try:', list(self.vehicle.mode_mapping().keys()))

    # Get mode ID
    mode_id = self.vehicle.mode_mapping()[mode]
    self.vehicle.mav.set_mode_send(
        self.vehicle.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)
    arm_msg = self.vehicle.recv_match(type='COMMAND_ACK', blocking=True, timeout=3)
    print('he cambiado el modo')

    self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component,
                                         mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
    self.vehicle.motors_armed_wait()
    self.state = "armado"


def arm(self):
    y = threading.Thread(target=self._arm)
    y.start()
