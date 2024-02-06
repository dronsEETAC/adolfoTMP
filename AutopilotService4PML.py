import json
import math

import threading
import paho.mqtt.client as mqtt
import time
import dronekit
from dronekit import connect, Command, VehicleMode
from paho.mqtt.client import ssl
from pymavlink import mavutil
from Dron_PML import Dron_PML








'''
These are the different values for the state of the autopilot:
    'connected' (only when connected the telemetry_info packet will be sent every 250 miliseconds)
    'arming'
    'armed'
    'disarmed'
    'takingOff'
    'flying'
    'returningHome'
    'landing'
    'onHearth'

The autopilot can also be 'disconnected' but this state will never appear in the telemetry_info packet 
when disconnected the service will not send any packet
'''

def process_message(message, client):
    global vehicle
    global dron
    global direction
    global go
    global sending_telemetry_info
    global sending_topic
    global op_mode
    global sending_topic
    global state


    splited = message.topic.split("/")
    origin = splited[0]
    command = splited[2]
    sending_topic = "autopilotService4/" + origin  #autopilotService/miMain/telemetryInfo
    print ('autopiloto4 recibe ', command)

    if command == "position":
        print("Position: ", message.payload )

    if command == "connect":
        if state == 'disconnected':
            print("Autopilot service connected by " + origin)
            #para conectar este autopilotService al dron al mismo tiempo que conectamos el Mission Planner
            # hay que ejecutar el siguiente comando desde PowerShell desde  C:\Users\USER>
            #mavproxy - -master =COM12 - -out = udp:127.0.0.1: 14550 - -out = udp:127.0.0.1: 14551
            # ahora el servicio puede conectarse por udp a cualquira de los dos puertos 14550 o 14551 y Mission Planner
            # al otro

            if op_mode == 'simulation':
                connection_string = "tcp:127.0.0.1:5793"

            else:

                connection_string = "com6"

            dron.connect(sending_topic, connection_string)
            print ('Connected to flight controller')
            state = 'connected'


        else:
            print ('Autopilot already connected')

    if command == "takeOff":
        state = 'takingOff'
        altitude = message.payload.decode("utf-8")
        dron.takeOff(float(altitude))

    if command == "returnToLaunch":
        # stop the process of getting positions
        dron.RTL()
        state = 'returningHome'
        

    if command == "armDrone":
        print ('arming')
        state = 'arming'
        dron.arm()

        # the vehicle will disarm automatically is takeOff does not come soon
        # when attribute 'armed' changes run function armed_change
        # vehicle.add_attribute_listener('armed', armed_change)
        state = 'armed'

    if command == "land":
        dron.Land()
        state = 'landing'

    if command == "go":
        direction = message.payload.decode("utf-8")
        print("Going ", direction)
        # go = True
        dron.startGo()
        dron.go(direction)

    if command == 'setGeofence':
        fence_listt = json.loads((message.payload))
        # fence_list = str(message.payload.decode("utf-8"))
        print ("geofence", fence_listt)
        print ("length", len(fence_listt))
        fence_list = []
        fv = []
        for n in fence_listt:
            fv += n['lat'], n['lon']
            fence_list.append(fv)
            fv = []

        print("real_geof", fence_list)
        dron.setGeofence(fence_list)

    if command == 'setParameters':

        param_list = json.loads((message.payload))
        print ('paramList', param_list)
        for n in param_list:
            FENCE_ALT_MAX_valor = n['FENCE_ALT_MAX']
            FENCE_ENABLE_valor = n['FENCE_ENABLE']
            margen_geof = n['FENCE_MARGIN']
            geof_action = n['FENCE_ACTION']
            PILOT_SPEED_UP_valor = n['PILOT_SPEED_UP']
            RTL_ALT_valor = n['RTL_ALT']
            FLTMODE6_valor = n['FLTMODE6']

        dron.setParams('FENCE_ALT_MAX', FENCE_ALT_MAX_valor)
        dron.setParams('FENCE_ENABLE', FENCE_ENABLE_valor)
        dron.setParams('FENCE_MARGIN', margen_geof)
        dron.setParams('FENCE_ACTION', geof_action)
        dron.setParams('PILOT_SPEED_UP', PILOT_SPEED_UP_valor)
        dron.setParams('RTL_ALT', RTL_ALT_valor)
        dron.setParams('FLTMODE6', FLTMODE6_valor)

    if command == 'getParameters':
        dron.getParams(sending_topic)






def on_internal_message(client, userdata, message):
    global internal_client
    process_message(message, internal_client)

def on_external_message(client, userdata, message):
    global external_client
    process_message(message, external_client)

def on_connect(external_client, userdata, flags, rc):
    if rc==0:
        print("Connection OK")
    else:
        print("Bad connection")

def AutopilotService (connection_mode, operation_mode, external_broker, username, password):
    global op_mode
    global dron
    global external_client
    global internal_client
    global state

    state = 'disconnected'

    print ('Connection mode: ', connection_mode)
    print ('Operation mode: ', operation_mode)
    op_mode = operation_mode



    internal_client = mqtt.Client("Autopilot_internal4")
    internal_client.on_message = on_internal_message
    internal_client.connect("localhost", 1884)


    external_client = mqtt.Client("Autopilot_external4_Adolfo", transport="websockets")
    external_client.on_message = on_external_message
    external_client.on_connect = on_connect

    if connection_mode== "global":
        if external_broker == "hivemq":
            external_client.connect("broker.hivemq.com", 8000)
            print('Connected to broker.hivemq.com:8000')

        elif external_broker == "hivemq_cert":
            external_client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                           tls_version=ssl.PROTOCOL_TLS, ciphers=None)
            external_client.connect("broker.hivemq.com", 8884)
            print('Connected to broker.hivemq.com:8884')

        elif external_broker == "classpip_cred":
            external_client.username_pw_set(username, password)
            external_client.connect("classpip.upc.edu", 8000)
            print('Connected to classpip.upc.edu:8000')

        elif external_broker == "classpip_cert":
            external_client.username_pw_set(username, password)
            external_client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                           tls_version=ssl.PROTOCOL_TLS, ciphers=None)
            external_client.connect("classpip.upc.edu", 8883)
            print('Connected to classpip.upc.edu:8883')
        elif external_broker == "localhost":
            external_client.connect("localhost", 8000)
            print('Connected to localhost:8000')
        elif external_broker == "localhost_cert":
            print('Not implemented yet')

    elif connection_mode == "local":
        if operation_mode == "simulation":
            external_client.connect("localhost", 8000)
            print('Connected to localhost:8000')
        else:
            external_client.connect("10.10.10.1", 8000)
            print('Connected to 10.10.10.1:8000')

    dron = Dron_PML(external_client)



    print("Waiting....")
    external_client.subscribe("+/autopilotService4/#", 2)
    external_client.subscribe("cameraService/+/#", 2)
    internal_client.subscribe("+/autopilotService4/#")
    internal_client.loop_start()
    if operation_mode == 'simulation':
        external_client.loop_forever()
    else:
        #external_client.loop_start() #when executed on board use loop_start instead of loop_forever
        external_client.loop_forever()




if __name__ == '__main__':
    import sys
    connection_mode = sys.argv[1] # global or local
    operation_mode = sys.argv[2] # simulation or production
    username = None
    password = None
    if connection_mode == 'global':
        external_broker = sys.argv[3]
        if external_broker == 'classpip_cred' or external_broker == 'classpip_cert':
            username = sys.argv[4]
            password = sys.argv[5]
    else:
        external_broker = None

    AutopilotService(connection_mode,operation_mode, external_broker, username, password)