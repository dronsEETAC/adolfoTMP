import threading
class Dron_PML(object):
    def __init__(self, broker):
        self.client = broker # necesita el broker para publicar respuestas
        self.lock = threading.Lock()
        self.state = "desconectado"
        self.lat = None
        self.lon = None
        self.alt = None
        ''' os otros estados son:
            conectado
            armando
            volando
            regresando
        '''

        self.going = False # se usa en dron_nav

    # aqui se importan los métodos de la clase Dron, que están organizados en ficheros.
    # Así podría orgenizarse la aportación de futuros alumnos que necesitasen incorporar nuevos servicios
    # para sus aplicaciones. Crearían un fichero con sus nuevos métodos y lo importarían aquí
    # Lo que no me gusta mucho es que si esa contribución nueva requiere de algún nuevo atributo de clase
    # ese atributo hay que declararlo aqui y no en el fichero con los métodos nuevos.
    # Ese es el caso del atributo going, que lo tengo que declarar aqui y preferiría poder declararlo en el fichero dron_goto

    from dron_connect_PML import connect, _connect, _send_telemetry_info
    from dron_arm_PML import arm, _arm
    from dron_takeOff_PML import takeOff, _takeOff
    from dron_RTL_Land_PML import  RTL, Land, _goDown
    from dron_nav_PML import _prepare_command, startGo, stopGo, go, _startGo
    from dron_setGeofence_PML import _setGeofence, setGeofence
    from dron_parameters_PML import _setParams, setParams, _getParams, getParams


