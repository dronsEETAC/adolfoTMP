import json
import threading
import time
import pymavlink
from pymavlink.mavutil import default_native
import pymavlink.dialects.v20.all as dialect
from pymavlink import mavutil


def _setGeofence(self, fence_list):
    FENCE_TOTAL = "FENCE_TOTAL".encode(encoding="utf-8")
    FENCE_ACTION = "FENCE_ACTION".encode(encoding="utf-8")

    message = dialect.MAVLink_param_request_read_message(target_system=self.vehicle.target_system,
                                                         target_component=self.vehicle.target_component,
                                                         param_id=FENCE_ACTION, param_index=-1)
    self.vehicle.mav.send(message)

    while True:
        message = self.vehicle.recv_match(type="PARAM_VALUE", blocking=True)
        message = message.to_dict()

        if message["param_id"] == "FENCE_ACTION":
            fence_action_original = int(message["param_value"])
            break

    while True:
        message = dialect.MAVLink_param_set_message(target_system=self.vehicle.target_system,
                                                    target_component=self.vehicle.target_component,
                                                    param_id=FENCE_ACTION, param_value=dialect.FENCE_ACTION_NONE,
                                                    param_type=dialect.MAV_PARAM_TYPE_REAL32)
        self.vehicle.mav.send(message)

        message = self.vehicle.recv_match(type="PARAM_VALUE", blocking=True)
        message = message.to_dict()

        if message["param_id"] == "FENCE_ACTION":
            if int(message["param_value"]) == dialect.FENCE_ACTION_NONE:
                break

    while True:
        message = dialect.MAVLink_param_set_message(target_system=self.vehicle.target_system,
                                                    target_component=self.vehicle.target_component,
                                                    param_id=FENCE_TOTAL, param_value=0,
                                                    param_type=dialect.MAV_PARAM_TYPE_REAL32)
        self.vehicle.mav.send(message)
        message = self.vehicle.recv_match(type="PARAM_VALUE", blocking=True)
        message = message.to_dict()

        if message["param_id"] == "FENCE_TOTAL":
            if int(message["param_value"]) == 0:
                break

    while True:
        message = dialect.MAVLink_param_set_message(target_system=self.vehicle.target_system,
                                                    target_component=self.vehicle.target_component,
                                                    param_id=FENCE_TOTAL, param_value=len(fence_list),
                                                    param_type=dialect.MAV_PARAM_TYPE_REAL32)
        self.vehicle.mav.send(message)
        message = self.vehicle.recv_match(type="PARAM_VALUE", blocking=True)
        message = message.to_dict()

        if message["param_id"] == "FENCE_TOTAL":
            if int(message["param_value"]) == len(fence_list):
                break

    idx = 0

    while idx < len(fence_list):
        message = dialect.MAVLink_fence_point_message(target_system=self.vehicle.target_system,
                                                      target_component=self.vehicle.target_component,
                                                      idx=idx, count=len(fence_list), lat=fence_list[idx][0],
                                                      lng=fence_list[idx][1])
        self.vehicle.mav.send(message)

        message = dialect.MAVLink_fence_fetch_point_message(target_system=self.vehicle.target_system,
                                                            target_component=self.vehicle.target_component, idx=idx)

        self.vehicle.mav.send(message)

        message = self.vehicle.recv_match(type="FENCE_POINT", blocking=True)
        message = message.to_dict()

        latitude = message["lat"]
        longitude = message["lng"]

        if latitude != 0.0 and longitude != 0.0:
            idx += 1

    while True:
        message = dialect.MAVLink_param_set_message(target_system=self.vehicle.target_system,
                                                    target_component=self.vehicle.target_component,
                                                    param_id=FENCE_ACTION,
                                                    param_value=fence_action_original,
                                                    param_type=dialect.MAV_PARAM_TYPE_REAL32)
        # dialect.F
        self.vehicle.mav.send(message)
        message = self.vehicle.recv_match(type="PARAM_VALUE", blocking=True)
        message = message.to_dict()
        if message["param_id"] == "FENCE_ACTION":
            if int(message["param_value"]) == fence_action_original:
                break


def setGeofence(self, fence_list):

    w = threading.Thread(target=self._setGeofence, args=[fence_list])
    w.start()