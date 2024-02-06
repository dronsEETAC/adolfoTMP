import json
import threading
import pymavlink.dialects.v20.all as dialect



def _setParams(self, ID, value):
    message = dialect.MAVLink_param_set_message(target_system=self.vehicle.target_system,
                                                target_component=self.vehicle.target_component, param_id=ID.encode("utf-8"),
                                                param_value=value, param_type=dialect.MAV_PARAM_TYPE_REAL32)
    self.vehicle.mav.send(message)
    pass

def _getParams(self, sending_topic):
    print ('vamos con los parametros')
    parameters = ['FENCE_ALT_MAX', 'FENCE_ENABLE', 'FENCE_MARGIN', 'FENCE_ACTION',
                  "RTL_ALT", "PILOT_SPEED_UP", 'FLTMODE6']
    result = []

    for PARAM in parameters:
        message = dialect.MAVLink_param_request_read_message(target_system=self.vehicle.target_system,
                                                         target_component=self.vehicle.target_component,
                                                         param_id=PARAM.encode(encoding="utf-8"), param_index=-1)
        self.vehicle.mav.send(message)
        while True:
            message = self.vehicle.recv_match(type="PARAM_VALUE", blocking=False)
            if message:
                message = message.to_dict()
                if message["param_id"] == PARAM:
                    result.append({
                        PARAM: message["param_value"]
                    })
                    break


    self.lock.acquire()
    self.client.publish(sending_topic + '/parameters', json.dumps(result))
    self.lock.release()

def getParams(self, sending_topic):
    y = threading.Thread(target=self._getParams,args=[sending_topic])
    y.start()

def setParams(self, ID, value):
    y = threading.Thread(target=self._setParams, args=[ID, value])
    y.start()