import math
import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk
from tkinter import Tk, Toplevel, messagebox
from tkinter.ttk import Label, Button
from PIL import Image
import os
import paho.mqtt.client as mqtt
import json
from geographiclib.geodesic import Geodesic
from ConfiguraciónyConexiónClass import ConfiguraciónyConexiónClass
from TelemetríayControlClass import TelemetríayControlClass
from GeofenceDesignClass import GeofenceDesignClass
from tkinter import *
from PIL import Image, ImageTk


ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class ComputeCoords:
    def __init__(self):
        self.geod = Geodesic.WGS84
        # two points (x,y) in the canvas and their corresponding positions (lat,lon)
        # self.refCoord = [60, 290]
        # self.refPosition = [41.27643361279337, 1.988196484744549]
        # self.refCoord2 = [790, 370]
        # self.refPosition2 = [41.27635096595008, 1.9891352578997614]

        self.refCoord = [84, 293]
        self.refPosition = [41.2764267, 1.9882317]
        self.refCoord2 = [768, 358]
        self.refPosition2 = [41.2763652, 1.98911288]
        distCoord = (
                math.sqrt(
                    (self.refCoord[0] - self.refCoord2[0]) ** 2
                    + (self.refCoord[1] - self.refCoord2[1]) ** 2
                ))
        g = self.geod.Inverse(
            self.refPosition[0],
            self.refPosition[1],
            self.refPosition2[0],
            self.refPosition2[1],
        )
        distPositions = float(g["s12"])
        self.mpp = distPositions/distCoord #meters per pixel
        self.ppm = 1 / self.mpp # pixels per metter


    def convertToCoords(self, position):
        g = self.geod.Inverse(
            self.refPosition[0],
            self.refPosition[1],
            float(position[0]),
            float(position[1]),
        )
        azimuth = float(g["azi2"])
        dist = float(g["s12"])

        x = self.refCoord[0] + math.trunc(
            dist * self.ppm * math.sin(math.radians(180-azimuth))
        )
        y = self.refCoord[1] + math.trunc(
            dist * self.ppm * math.cos(math.radians(180-azimuth))
        )
        return x, y

    def convertToPosition(self, coords):
        # compute distance with ref coords
        dist = (
            math.sqrt(
                (coords[0] - self.refCoord[0]) ** 2
                + (coords[1] - self.refCoord[1]) ** 2
            )
            * self.mpp
        )
        azimuth = math.degrees(
            math.atan2((self.refCoord[0] - coords[0]), (self.refCoord[1] - coords[1]))
        ) * (-1)
        if azimuth < 0:
            azimuth = azimuth + 360
        # compute lat,log of new wayp
        g = self.geod.Direct(
            float(self.refPosition[0]), float(self.refPosition[1]), azimuth, dist
        )
        lat = float(g["lat2"])
        lon = float(g["lon2"])
        return lat, lon
class App(ctk.CTk):


    def on_message(self, client, userdata, message):

        if message.topic == 'autopilotService/miMain/parameters':
            p1 = json.loads(message.payload)
            print ("paramList1", p1)

            FENCE_ALT_MAX_valor = p1[0]['FENCE_ALT_MAX']
            FENCE_ENABLE_valor = p1[1]['FENCE_ENABLE']
            margen_geof = p1[2]['FENCE_MARGIN']
            geof_action = p1[3]['FENCE_ACTION']
            RTL_ALT_valor = p1[4]['RTL_ALT']
            PILOT_SPEED_UP_valor = p1[5]['PILOT_SPEED_UP']
            FLTMODE6_valor = p1[6]['FLTMODE6']


            if Confcreado:
                self.connectionFrameObject.getParameters("d1", FENCE_ALT_MAX_valor, FENCE_ENABLE_valor,
                                                         margen_geof, geof_action, RTL_ALT_valor,
                                                         PILOT_SPEED_UP_valor, FLTMODE6_valor)


        if message.topic == 'autopilotService2/miMain/parameters':
            p2 = json.loads(message.payload)
            FENCE_ALT_MAX_valor = p2[0]['FENCE_ALT_MAX']
            FENCE_ENABLE_valor = p2[1]['FENCE_ENABLE']
            margen_geof = p2[2]['FENCE_MARGIN']
            geof_action = p2[3]['FENCE_ACTION']
            RTL_ALT_valor = p2[4]['RTL_ALT']
            PILOT_SPEED_UP_valor = p2[5]['PILOT_SPEED_UP']
            FLTMODE6_valor = p2[6]['FLTMODE6']

            if Confcreado:
                self.connectionFrameObject.getParameters("d2", FENCE_ALT_MAX_valor, FENCE_ENABLE_valor,
                                                         margen_geof, geof_action, RTL_ALT_valor,
                                                         PILOT_SPEED_UP_valor, FLTMODE6_valor)

        if message.topic == 'autopilotService3/miMain/parameters':
            p3 = json.loads(message.payload)
            FENCE_ALT_MAX_valor = p3[0]['FENCE_ALT_MAX']
            FENCE_ENABLE_valor = p3[1]['FENCE_ENABLE']
            margen_geof = p3[2]['FENCE_MARGIN']
            geof_action = p3[3]['FENCE_ACTION']
            RTL_ALT_valor = p3[4]['RTL_ALT']
            PILOT_SPEED_UP_valor = p3[5]['PILOT_SPEED_UP']
            FLTMODE6_valor = p3[6]['FLTMODE6']

            if Confcreado:
                self.connectionFrameObject.getParameters("d3", FENCE_ALT_MAX_valor, FENCE_ENABLE_valor,
                                                         margen_geof, geof_action, RTL_ALT_valor,
                                                         PILOT_SPEED_UP_valor, FLTMODE6_valor)

        if message.topic == 'autopilotService4/miMain/parameters':
            p4 = json.loads(message.payload)
            FENCE_ALT_MAX_valor = p4[0]['FENCE_ALT_MAX']
            FENCE_ENABLE_valor = p4[1]['FENCE_ENABLE']
            margen_geof = p4[2]['FENCE_MARGIN']
            geof_action = p4[3]['FENCE_ACTION']
            RTL_ALT_valor = p4[4]['RTL_ALT']
            PILOT_SPEED_UP_valor = p4[5]['PILOT_SPEED_UP']
            FLTMODE6_valor = p4[6]['FLTMODE6']

            if Confcreado:
                self.connectionFrameObject.getParameters("d4", FENCE_ALT_MAX_valor, FENCE_ENABLE_valor,
                                                         margen_geof, geof_action, RTL_ALT_valor,
                                                         PILOT_SPEED_UP_valor, FLTMODE6_valor)


        if message.topic == 'autopilotService/miMain/telemetryInfo':
            a = json.loads(message.payload)


            self.vel = a["groundSpeed"]
            self.alt = a["alt"]
            self.state = a["state"]
            print ('state', self.state)
            self.lat = a["lat"]
            self.lon = a["lon"]

            if Telemcreado:

                self.controlFrameObject.setTelemetryInfo(self.vel, self.alt, "d1")

            if Confcreado:
                self.connectionFrameObject.getStateInfo(self.state, "d1")

            if Maincreado:
                self.drawDrone(self.lat, self.lon, "d1", self.state)


        if message.topic == 'autopilotService2/miMain/telemetryInfo':
            b = json.loads(message.payload)

            self.vel2 = b["groundSpeed"]
            self.alt2 = b["alt"]
            self.state2 = b["state"]
            self.lat2 = b["lat"]
            self.lon2 = b["lon"]
            # print(self.vel2)
            # print(self.alt2)

            if Telemcreado:

                self.controlFrameObject.setTelemetryInfo(self.vel2, self.alt2, "d2")

            if Confcreado:
                self.connectionFrameObject.getStateInfo(self.state2, "d2")

            if Maincreado:
                self.drawDrone(self.lat2, self.lon2, "d2", self.state2)

        if message.topic == 'autopilotService3/miMain/telemetryInfo':
            c = json.loads(message.payload)

            self.vel3 = c["groundSpeed"]
            self.alt3 = c["alt"]
            self.state3 = c["state"]
            self.lat3 = c["lat"]
            self.lon3 = c["lon"]
            # print(self.vel3)
            # print(self.alt3)

            if Telemcreado:

                self.controlFrameObject.setTelemetryInfo(self.vel3, self.alt3, "d3")

            if Confcreado:
                self.connectionFrameObject.getStateInfo(self.state3, "d3")

            if Maincreado:
                self.drawDrone(self.lat3, self.lon3, "d3", self.state3)

        if message.topic == 'autopilotService4/miMain/telemetryInfo':
            d = json.loads(message.payload)

            self.vel4 = d["groundSpeed"]
            self.alt4 = d["alt"]
            self.state4 = d["state"]
            self.lat4 = d["lat"]
            self.lon4 = d["lon"]
            # print(self.vel4)
            # print(self.alt4)

            if Telemcreado:

                self.controlFrameObject.setTelemetryInfo(self.vel4, self.alt4, "d4")

            if Confcreado:
                self.connectionFrameObject.getStateInfo(self.state4, "d4")

            if Maincreado:
                self.drawDrone(self.lat4, self.lon4, "d4", self.state4)

    def __init__(self):
        super().__init__()

        global Telemcreado
        global Confcreado
        global Maincreado
        global cargarGeof

        Telemcreado=False
        Confcreado=False
        Maincreado=False
        cargarGeof = False
        self.cd1 = False
        self.cd2 = False
        self.cd3 = False
        self.cd4 = False

        self.conversor = ComputeCoords()
        self.title("Dronelab control application.py")

        self.client = mqtt.Client("Main", transport="websockets")
        self.client.on_message = self.on_message
        self.client.username_pw_set(username, password)
        self.client.connect("classpip.upc.edu", 8000)
        print('Connected to classpip.upc.edu:8000')
        self.client.loop_start()

        self.client.subscribe("autopilotService/miMain/telemetryInfo")
        self.client.subscribe("autopilotService2/miMain/telemetryInfo")
        self.client.subscribe("autopilotService3/miMain/telemetryInfo")
        self.client.subscribe("autopilotService4/miMain/telemetryInfo")

        self.client.subscribe("autopilotService/miMain/parameters")
        self.client.subscribe("autopilotService2/miMain/parameters")
        self.client.subscribe("autopilotService3/miMain/parameters")
        self.client.subscribe("autopilotService4/miMain/parameters")

        self.Mainframe = ctk.CTkFrame(self.geometry("1100x640"), width=140, corner_radius=0)
        self.Mainframe.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.Mainframe.grid_rowconfigure(0, weight=1)
        self.Mainframe.grid_rowconfigure(1, weight=1)
        self.Mainframe.grid_rowconfigure(2, weight=1)
        self.Mainframe.grid_rowconfigure(3, weight=1)

        self.Mainframe.grid_columnconfigure(0, weight=1)
        self.Mainframe.grid_columnconfigure(1, weight=20)
        self.Mainframe.grid_columnconfigure(2, weight=20)
        self.Mainframe.grid_columnconfigure(3, weight=20)
        self.Mainframe.grid_columnconfigure(4, weight=20)
        self.logo_label = ctk.CTkLabel(self.Mainframe, text="Panel de Control",
                                                 font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 1))
        self.sidebar_button_1 = ctk.CTkButton(self.Mainframe, text = 'Configuración y conexión', command=self.ConfiguraciónClicked)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=1)
        self.sidebar_button_2 = ctk.CTkButton(self.Mainframe, text = 'Cargar Geofence', command=self.CargarGeofenceClicked)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=1)
        self.sidebar_button_3 = ctk.CTkButton(self.Mainframe, text = 'Telemetría y Control', command=self.TelemetriaControlClicked)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=1)
        self.RTL1_button = ctk.CTkButton(self.Mainframe, text='RTL1', fg_color="red", text_color= "black",
                                              command=self.d1RTLbuttonClicked)
        self.RTL1_button.grid(row=4, column=1, padx=20, pady=1)
        self.RTL2_button = ctk.CTkButton(self.Mainframe, text='RTL2', fg_color= "blue", text_color= "black",
                                         command=self.d2RTLbuttonClicked)
        self.RTL2_button.grid(row=4, column=2, padx=20, pady=1)
        self.RTL3_button = ctk.CTkButton(self.Mainframe, text='RTL3', fg_color= "yellow", text_color= "black",
                                         command=self.d3RTLbuttonClicked)
        self.RTL3_button.grid(row=4, column=3, padx=20, pady=1)
        self.RTL4_button = ctk.CTkButton(self.Mainframe, text='RTL4', fg_color= "green", text_color= "black",
                                         command=self.d4RTLbuttonClicked)
        self.RTL4_button.grid(row=4, column=4, padx=20, pady=1)



        self.canvas = Canvas(self.Mainframe, height=595, width=851 ,bg='black')
        self.canvas.grid(row=0, column=1, rowspan=4, columnspan=4) #, padx=1, pady=1, sticky="nsew")
        self.image = Image.open("recintoDrone.png")
        # self.image = self.image.resize((1350, 700), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.image, anchor='nw')
        # self.drone1 = self.canvas.create_oval(-1, -1, 1, 1)


        Maincreado=True


    def d1RTLbuttonClicked(self):


        self.client.publish("miMain/autopilotService/returnToLaunch")
    def d2RTLbuttonClicked(self):
        self.client.publish("miMain/autopilotService2/returnToLaunch")
    def d3RTLbuttonClicked(self):
        self.client.publish("miMain/autopilotService3/returnToLaunch")
    def d4RTLbuttonClicked(self):
        self.client.publish("miMain/autopilotService4/returnToLaunch")
    def ConfiguraciónClicked(self):

        global Confcreado
        print("Accediendo a Conexión de drones")
        newWindow = ctk.CTkToplevel(self.Mainframe)
        newWindow.title("Conexión drones")
        newWindow.geometry("1000x500")
        newWindow.grab_set()


        self.connectionFrameObject = ConfiguraciónyConexiónClass()
        self.connectionFrame, self.Ndrones= self.connectionFrameObject.BuildFrame(newWindow, self.client)
        self.connectionFrame.pack(fill="both", expand="yes", padx=10, pady=10)
        Confcreado = True


    def CargarGeofenceClicked(self):
        global cargarGeof

        self.cargarGeofenceObject = GeofenceDesignClass()
        self.geofence_type, self.x_y_coord1, self.x_y_coord2, self.x_y_coord3, self.x_y_coord4 = self.cargarGeofenceObject.cargarGeofence(self.Ndrones)

        # self.cargarParametrosConfObject = ConfiguraciónyConexiónClass()
        # self.altura_toff1, self.altura_toff2, self.altura_toff3, self.altura_toff4 = self.cargarParametrosConfObject.cargarAltura()

        # print ("altura vuelo", self.altura_toff1)
        cargarGeof = True

        # self.AAc = [290, 60]
        # self.BBc = [85, 695]
        # self.CCc = [370, 790]
        # self.DDc = [570, 145]

        self.AAc = [293, 84]
        self.BBc = [105, 683]
        self.CCc = [358, 768]
        self.DDc = [554, 168]
        self.AB1c = [((self.BBc[0] - self.AAc[0]) / 4) + self.AAc[0], ((self.BBc[1] - self.AAc[1]) / 4) + self.AAc[1]]
        self.AB2c = [((self.BBc[0] - self.AAc[0]) / 2) + self.AAc[0], ((self.BBc[1] - self.AAc[1]) / 2) + self.AAc[1]]
        self.AB3c = [((self.BBc[0] - self.AAc[0]) * 3 / 4) + self.AAc[0],
                     ((self.BBc[1] - self.AAc[1]) * 3 / 4) + self.AAc[1]]
        self.AB1_3c = [((self.BBc[0] - self.AAc[0]) / 3) + self.AAc[0], ((self.BBc[1] - self.AAc[1]) / 3) + self.AAc[1]]
        self.AB2_3c = [((self.BBc[0] - self.AAc[0]) * 2 / 3) + self.AAc[0],
                     ((self.BBc[1] - self.AAc[1]) * 2 / 3) + self.AAc[1]]
        self.DC1c = [((self.CCc[0] - self.DDc[0]) / 4) + self.DDc[0], ((self.CCc[1] - self.DDc[1]) / 4) + self.DDc[1]]
        self.DC2c = [((self.CCc[0] - self.DDc[0]) / 2) + self.DDc[0], ((self.CCc[1] - self.DDc[1]) / 2) + self.DDc[1]]
        self.DC3c = [((self.CCc[0] - self.DDc[0]) * 3 / 4) + self.DDc[0],
                     ((self.CCc[1] - self.DDc[1]) * 3 / 4) + self.DDc[1]]
        self.DC1_3c = [((self.CCc[0] - self.DDc[0]) / 3) + self.DDc[0], ((self.CCc[1] - self.DDc[1]) / 3) + self.DDc[1]]
        self.DC2_3c = [((self.CCc[0] - self.DDc[0]) * 2 / 3) + self.DDc[0],
                     ((self.CCc[1] - self.DDc[1]) * 2 / 3) + self.DDc[1]]
        self.AD1c = [((self.AAc[0] - self.DDc[0]) / 2) + self.DDc[0], ((self.DDc[1] - self.AAc[1]) / 2) + self.AAc[1]]
        self.AD1_3c = [((self.AAc[0] - self.DDc[0]) / 3) + self.DDc[0], ((self.DDc[1] - self.AAc[1]) * 2 / 3) + self.AAc[1]]
        self.AD2_3c = [((self.AAc[0] - self.DDc[0]) * 2 / 3) + self.DDc[0],
                       ((self.DDc[1] - self.AAc[1])  / 3) + self.AAc[1]]
        self.BC1c = [((self.BBc[0] - self.CCc[0]) / 2) + self.CCc[0], ((self.CCc[1] - self.BBc[1]) / 2) + self.BBc[1]]
        self.BC1_3c = [((self.BBc[0] - self.CCc[0]) / 3) + self.CCc[0], ((self.CCc[1] - self.BBc[1]) * 2 / 3) + self.BBc[1]]
        self.BC2_3c = [((self.BBc[0] - self.CCc[0]) * 2 / 3) + self.CCc[0],
                       ((self.CCc[1] - self.BBc[1]) / 3) + self.BBc[1]]
        self.MMc = [((self.AB2c[0] - self.DC2c[0]) / 2) + self.DC2c[0],
                    ((self.BC1c[1] - self.AD1c[1]) / 2) + self.AD1c[1]]

        if self.geofence_type == "g1":

            if self.Ndrones == "1":
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=self.image, anchor='nw')

                self.canvas.create_line(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], width=2, fill="red")
                self.canvas.create_line(self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], width=2, fill="red")
                self.canvas.create_line(self.CCc[1], self.CCc[0], self.DDc[1], self.DDc[0], width=2, fill="red")
                self.canvas.create_line(self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], width=2, fill="red")

                self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0],
                                           self.DDc[1], self.DDc[0], fill='red', stipple="gray12")

            if self.Ndrones == "2":
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=self.image, anchor='nw')

                self.canvas.create_line(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], width=2, fill="red")
                self.canvas.create_line(self.BBc[1], self.BBc[0], self.BC1c[1], self.BC1c[0], width=2, fill="red")
                self.canvas.create_line(self.BC1c[1], self.BC1c[0], self.AD1c[1], self.AD1c[0], width=2, fill="red")
                self.canvas.create_line(self.AD1c[1], self.AD1c[0], self.AAc[1], self.AAc[0], width=2, fill="red")

                self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], self.BC1c[1],
                                           self.BC1c[0], self.AD1c[1], self.AD1c[0], self.AAc[1], self.AAc[0],
                                           fill='red', stipple="gray12")

                self.canvas.create_line(self.AD1c[1], self.AD1c[0], self.BC1c[1], self.BC1c[0], width=2, fill="blue")
                self.canvas.create_line(self.BC1c[1], self.BC1c[0], self.CCc[1], self.CCc[0], width=2, fill="blue")
                self.canvas.create_line(self.CCc[1], self.CCc[0], self.DDc[1], self.DDc[0], width=2, fill="blue")
                self.canvas.create_line(self.DDc[1], self.DDc[0], self.AD1c[1], self.AD1c[0], width=2, fill="blue")
                self.canvas.create_polygon(self.AD1c[1], self.AD1c[0], self.BC1c[1], self.BC1c[0], self.CCc[1],
                                           self.CCc[0], self.DDc[1], self.DDc[0], self.AD1c[1], self.AD1c[0],
                                           fill='blue', stipple="gray12")

            if self.Ndrones == "3":
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=self.image, anchor='nw')

                self.canvas.create_line(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], width=2, fill="red")
                self.canvas.create_line(self.BBc[1], self.BBc[0], self.BC2_3c[1], self.BC2_3c[0], width=2, fill="red")
                self.canvas.create_line(self.BC2_3c[1], self.BC2_3c[0], self.AD2_3c[1], self.AD2_3c[0], width=2,
                                        fill="red")
                self.canvas.create_line(self.AD2_3c[1], self.AD2_3c[0], self.AAc[1], self.AAc[0], width=2, fill="red")
                self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], self.BC2_3c[1],
                                           self.BC2_3c[0], self.AD2_3c[1], self.AD2_3c[0], self.AAc[1], self.AAc[0],
                                           fill='red', stipple="gray12")

                self.canvas.create_line(self.AD1_3c[1], self.AD1_3c[0], self.BC1_3c[1], self.BC1_3c[0], width=2,
                                        fill="blue")
                self.canvas.create_line(self.BC1_3c[1], self.BC1_3c[0], self.BC2_3c[1], self.BC2_3c[0], width=2,
                                        fill="blue")
                self.canvas.create_line(self.BC2_3c[1], self.BC2_3c[0], self.AD2_3c[1], self.AD2_3c[0], width=2,
                                        fill="blue")
                self.canvas.create_line(self.AD2_3c[1], self.AD2_3c[0], self.AD1_3c[1], self.AD1_3c[0], width=2,
                                        fill="blue")
                self.canvas.create_polygon(self.AD1_3c[1], self.AD1_3c[0], self.BC1_3c[1], self.BC1_3c[0],
                                           self.BC2_3c[1], self.BC2_3c[0], self.AD2_3c[1], self.AD2_3c[0],
                                           self.AD1_3c[1], self.AD1_3c[0], fill='blue', stipple="gray12")

                self.canvas.create_line(self.AD1_3c[1], self.AD1_3c[0], self.BC1_3c[1], self.BC1_3c[0], width=2,
                                        fill="yellow")
                self.canvas.create_line(self.BC1_3c[1], self.BC1_3c[0], self.CCc[1], self.CCc[0], width=2,
                                        fill="yellow")
                self.canvas.create_line(self.CCc[1], self.CCc[0], self.DDc[1], self.DDc[0], width=2, fill="yellow")
                self.canvas.create_line(self.DDc[1], self.DDc[0], self.AD1_3c[1], self.AD1_3c[0], width=2,
                                        fill="yellow")
                self.canvas.create_polygon(self.AD1_3c[1], self.AD1_3c[0], self.BC1_3c[1], self.BC1_3c[0], self.CCc[1],
                                           self.CCc[0], self.DDc[1], self.DDc[0], self.AD1_3c[1], self.AD1_3c[0],
                                           fill='yellow', stipple="gray12")

            if self.Ndrones == "4":
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=self.image, anchor='nw')

                self.canvas.create_line(self.AAc[1], self.AAc[0], self.AB2c[1], self.AB2c[0], width=2, fill="red")
                self.canvas.create_line(self.AB2c[1], self.AB2c[0], self.MMc[1], self.MMc[0], width=2, fill="red")
                self.canvas.create_line(self.MMc[1], self.MMc[0], self.AD1c[1], self.AD1c[0], width=2, fill="red")
                self.canvas.create_line(self.AD1c[1], self.AD1c[0], self.AAc[1], self.AAc[0], width=2, fill="red")
                self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.AB2c[1], self.AB2c[0], self.MMc[1],
                                           self.MMc[0], self.AD1c[1], self.AD1c[0], self.AAc[1], self.AAc[0],
                                           fill='red', stipple="gray12")

                self.canvas.create_line(self.AB2c[1], self.AB2c[0], self.BBc[1], self.BBc[0], width=2, fill="blue")
                self.canvas.create_line(self.BBc[1], self.BBc[0], self.BC1c[1], self.BC1c[0], width=2, fill="blue")
                self.canvas.create_line(self.BC1c[1], self.BC1c[0], self.MMc[1], self.MMc[0], width=2, fill="blue")
                self.canvas.create_line(self.MMc[1], self.MMc[0], self.AB2c[1], self.AB2c[0], width=2, fill="blue")
                self.canvas.create_polygon(self.AB2c[1], self.AB2c[0], self.BBc[1], self.BBc[0], self.BC1c[1],
                                           self.BC1c[0], self.MMc[1], self.MMc[0], self.AB2c[1], self.AB2c[0],
                                           fill='blue', stipple="gray12")

                self.canvas.create_line(self.AD1c[1], self.AD1c[0], self.MMc[1], self.MMc[0], width=2, fill="yellow")
                self.canvas.create_line(self.MMc[1], self.MMc[0], self.DC2c[1], self.DC2c[0], width=2, fill="yellow")
                self.canvas.create_line(self.DC2c[1], self.DC2c[0], self.DDc[1], self.DDc[0], width=2, fill="yellow")
                self.canvas.create_line(self.DDc[1], self.DDc[0], self.AD1c[1], self.AD1c[0], width=2, fill="yellow")
                self.canvas.create_polygon(self.AD1c[1], self.AD1c[0], self.MMc[1], self.MMc[0], self.DC2c[1],
                                           self.DC2c[0], self.DDc[1], self.DDc[0], self.AD1c[1], self.AD1c[0],
                                           fill='yellow', stipple="gray12")

                self.canvas.create_line(self.MMc[1], self.MMc[0], self.BC1c[1], self.BC1c[0], width=2, fill="green")
                self.canvas.create_line(self.BC1c[1], self.BC1c[0], self.CCc[1], self.CCc[0], width=2, fill="green")
                self.canvas.create_line(self.CCc[1], self.CCc[0], self.DC2c[1], self.DC2c[0], width=2, fill="green")
                self.canvas.create_line(self.DC2c[1], self.DC2c[0], self.MMc[1], self.MMc[0], width=2, fill="green")
                self.canvas.create_polygon(self.MMc[1], self.MMc[0], self.BC1c[1], self.BC1c[0], self.CCc[1],
                                           self.CCc[0], self.DC2c[1], self.DC2c[0], self.MMc[1], self.MMc[0],
                                           fill='green', stipple="gray12")

        if self.geofence_type == "g2":

            if self.Ndrones == "1":
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=self.image, anchor='nw')

                self.canvas.create_line(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], width=2, fill="red")
                self.canvas.create_line(self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], width=2, fill="red")
                self.canvas.create_line(self.CCc[1], self.CCc[0], self.DDc[1], self.DDc[0], width=2, fill="red")
                self.canvas.create_line(self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], width=2, fill="red")
                self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0],
                                           self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], fill='red',
                                           stipple="gray12")

            if self.Ndrones == "2":
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=self.image, anchor='nw')

                self.canvas.create_line(self.AAc[1], self.AAc[0], self.AB2c[1], self.AB2c[0], width=2, fill="red")
                self.canvas.create_line(self.AB2c[1], self.AB2c[0], self.DC2c[1], self.DC2c[0], width=2, fill="red")
                self.canvas.create_line(self.DC2c[1], self.DC2c[0], self.DDc[1], self.DDc[0], width=2, fill="red")
                self.canvas.create_line(self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], width=2, fill="red")
                self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.AB2c[1], self.AB2c[0], self.DC2c[1],
                                           self.DC2c[0], self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], fill='red',
                                           stipple="gray12")

                self.canvas.create_line(self.AB2c[1], self.AB2c[0], self.BBc[1], self.BBc[0], width=2, fill="blue")
                self.canvas.create_line(self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], width=2, fill="blue")
                self.canvas.create_line(self.CCc[1], self.CCc[0], self.DC2c[1], self.DC2c[0], width=2, fill="blue")
                self.canvas.create_line(self.DC2c[1], self.DC2c[0], self.AB2c[1], self.AB2c[0], width=2, fill="blue")
                self.canvas.create_polygon(self.AB2c[1], self.AB2c[0], self.BBc[1], self.BBc[0], self.CCc[1],
                                           self.CCc[0], self.DC2c[1], self.DC2c[0], self.AB2c[1], self.AB2c[0],
                                           fill='blue', stipple="gray12")

            if self.Ndrones == "3":
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=self.image, anchor='nw')

                self.canvas.create_line(self.AAc[1], self.AAc[0], self.AB1_3c[1], self.AB1_3c[0], width=2, fill="red")
                self.canvas.create_line(self.AB1_3c[1], self.AB1_3c[0], self.DC1_3c[1], self.DC1_3c[0], width=2,
                                        fill="red")
                self.canvas.create_line(self.DC1_3c[1], self.DC1_3c[0], self.DDc[1], self.DDc[0], width=2,
                                        fill="red")
                self.canvas.create_line(self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], width=2, fill="red")
                self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.AB1_3c[1], self.AB1_3c[0], self.DC1_3c[1],
                                           self.DC1_3c[0], self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0],
                                           fill='red', stipple="gray12")

                self.canvas.create_line(self.AB1_3c[1], self.AB1_3c[0], self.AB2_3c[1], self.AB2_3c[0], width=2,
                                        fill="blue")
                self.canvas.create_line(self.AB2_3c[1], self.AB2_3c[0], self.DC2_3c[1], self.DC2_3c[0], width=2,
                                        fill="blue")
                self.canvas.create_line(self.DC2_3c[1], self.DC2_3c[0], self.DC1_3c[1], self.DC1_3c[0], width=2,
                                        fill="blue")
                self.canvas.create_line(self.DC1_3c[1], self.DC1_3c[0], self.AB1_3c[1], self.AB1_3c[0], width=2,
                                        fill="blue")
                self.canvas.create_polygon(self.AB1_3c[1], self.AB1_3c[0], self.AB2_3c[1], self.AB2_3c[0],
                                           self.DC2_3c[1], self.DC2_3c[0], self.DC1_3c[1], self.DC1_3c[0],
                                           self.AB1_3c[1], self.AB1_3c[0], fill='blue', stipple="gray12")

                self.canvas.create_line(self.AB2_3c[1], self.AB2_3c[0], self.BBc[1], self.BBc[0], width=2,
                                        fill="yellow")
                self.canvas.create_line(self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], width=2,
                                        fill="yellow")
                self.canvas.create_line(self.CCc[1], self.CCc[0], self.DC2_3c[1], self.DC2_3c[0], width=2,
                                        fill="yellow")
                self.canvas.create_line(self.DC2_3c[1], self.DC2_3c[0], self.AB2_3c[1], self.AB2_3c[0], width=2,
                                        fill="yellow")
                self.canvas.create_polygon(self.AB2_3c[1], self.AB2_3c[0], self.BBc[1], self.BBc[0], self.CCc[1],
                                           self.CCc[0], self.DC2_3c[1], self.DC2_3c[0], self.AB2_3c[1], self.AB2_3c[0],
                                           fill='yellow', stipple="gray12")

            if self.Ndrones == "4":
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=self.image, anchor='nw')

                self.canvas.create_line(self.AAc[1], self.AAc[0], self.AB1c[1], self.AB1c[0], width=2, fill="red")
                self.canvas.create_line(self.AB1c[1], self.AB1c[0], self.DC1c[1], self.DC1c[0], width=2, fill="red")
                self.canvas.create_line(self.DC1c[1], self.DC1c[0], self.DDc[1], self.DDc[0], width=2, fill="red")
                self.canvas.create_line(self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], width=2, fill="red")
                self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.AB1c[1], self.AB1c[0], self.DC1c[1],
                                           self.DC1c[0], self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], fill='red',
                                           stipple="gray12")

                self.canvas.create_line(self.AB1c[1], self.AB1c[0], self.AB2c[1], self.AB2c[0], width=2, fill="blue")
                self.canvas.create_line(self.AB2c[1], self.AB2c[0], self.DC2c[1], self.DC2c[0], width=2, fill="blue")
                self.canvas.create_line(self.DC2c[1], self.DC2c[0], self.DC1c[1], self.DC1c[0], width=2, fill="blue")
                self.canvas.create_line(self.DC1c[1], self.DC1c[0], self.AB1c[1], self.AB1c[0], width=2, fill="blue")
                self.canvas.create_polygon(self.AB1c[1], self.AB1c[0], self.AB2c[1], self.AB2c[0], self.DC2c[1],
                                           self.DC2c[0], self.DC1c[1], self.DC1c[0], self.AB1c[1], self.AB1c[0],
                                           fill='blue', stipple="gray12")

                self.canvas.create_line(self.AB2c[1], self.AB2c[0], self.AB3c[1], self.AB3c[0], width=2, fill="yellow")
                self.canvas.create_line(self.AB3c[1], self.AB3c[0], self.DC3c[1], self.DC3c[0], width=2, fill="yellow")
                self.canvas.create_line(self.DC3c[1], self.DC3c[0], self.DC2c[1], self.DC2c[0], width=2, fill="yellow")
                self.canvas.create_line(self.DC2c[1], self.DC2c[0], self.AB2c[1], self.AB2c[0], width=2, fill="yellow")
                self.canvas.create_polygon(self.AB2c[1], self.AB2c[0], self.AB3c[1], self.AB3c[0], self.DC3c[1],
                                           self.DC3c[0], self.DC2c[1], self.DC2c[0], self.AB2c[1], self.AB2c[0],
                                           fill='yellow', stipple="gray12")

                self.canvas.create_line(self.AB3c[1], self.AB3c[0], self.BBc[1], self.BBc[0], width=2, fill="green")
                self.canvas.create_line(self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], width=2, fill="green")
                self.canvas.create_line(self.CCc[1], self.CCc[0], self.DC3c[1], self.DC3c[0], width=2, fill="green")
                self.canvas.create_line(self.DC3c[1], self.DC3c[0], self.AB3c[1], self.AB3c[0], width=2, fill="green")
                self.canvas.create_polygon(self.AB3c[1], self.AB3c[0], self.BBc[1], self.BBc[0], self.CCc[1],
                                           self.CCc[0], self.DC3c[1], self.DC3c[0], self.AB3c[1], self.AB3c[0],
                                           fill='green', stipple="gray12")

        if self.geofence_type == "custom":

            if self.Ndrones == "1":
                for i in range(len(self.x_y_coord1) - 1):
                    self.canvas.create_line(self.x_y_coord1[i][0], self.x_y_coord1[i][1], self.x_y_coord1[i + 1][0],
                                            self.x_y_coord1[i + 1][1], width=2, fill="red")
                    i = 0


                self.x_y_poligon1 = []
                for n in self.x_y_coord1:
                    self.x_y_poligon1 += n

                self.canvas.create_polygon(self.x_y_poligon1, fill='red', stipple="gray12")



            if self.Ndrones == "2":
                for i in range(len(self.x_y_coord1) - 1):
                    self.canvas.create_line(self.x_y_coord1[i][0], self.x_y_coord1[i][1], self.x_y_coord1[i + 1][0],
                                            self.x_y_coord1[i + 1][1], width=2, fill="red")
                    i = 0

                    self.x_y_poligon1 = []
                    for n in self.x_y_coord1:
                        self.x_y_poligon1 += n

                    self.canvas.create_polygon(self.x_y_poligon1, fill='red', stipple="gray12")



                for j in range(len(self.x_y_coord2) - 1):
                    self.canvas.create_line(self.x_y_coord2[j][0], self.x_y_coord2[j][1], self.x_y_coord2[j + 1][0],
                                            self.x_y_coord2[j + 1][1], width=2, fill="blue")
                    j = 0

                    self.x_y_poligon2 = []
                    for n in self.x_y_coord2:
                        self.x_y_poligon2 += n

                    self.canvas.create_polygon(self.x_y_poligon2, fill='blue', stipple="gray12")



            if self.Ndrones == "3":
                for i in range(len(self.x_y_coord1) - 1):
                    self.canvas.create_line(self.x_y_coord1[i][0], self.x_y_coord1[i][1], self.x_y_coord1[i + 1][0],
                                            self.x_y_coord1[i + 1][1], width=2, fill="red")
                    i = 0

                    self.x_y_poligon1 = []
                    for n in self.x_y_coord1:
                        self.x_y_poligon1 += n

                    self.canvas.create_polygon(self.x_y_poligon1, fill='red', stipple="gray12")



                for j in range(len(self.x_y_coord2) - 1):
                    self.canvas.create_line(self.x_y_coord2[j][0], self.x_y_coord2[j][1], self.x_y_coord2[j + 1][0],
                                            self.x_y_coord2[j + 1][1], width=2, fill="blue")
                    j = 0

                    self.x_y_poligon2 = []
                    for n in self.x_y_coord2:
                        self.x_y_poligon2 += n

                    self.canvas.create_polygon(self.x_y_poligon2, fill='blue', stipple="gray12")

                for k in range(len(self.x_y_coord3) - 1):
                    self.canvas.create_line(self.x_y_coord3[k][0], self.x_y_coord3[k][1], self.x_y_coord3[k + 1][0],
                                            self.x_y_coord3[k + 1][1], width=2, fill="yellow")
                    k = 0

                    self.x_y_poligon3 = []
                    for n in self.x_y_coord3:
                        self.x_y_poligon3 += n

                    self.canvas.create_polygon(self.x_y_poligon3, fill='yellow', stipple="gray12")


            if self.Ndrones == "4":
                for i in range(len(self.x_y_coord1) - 1):
                    self.canvas.create_line(self.x_y_coord1[i][0], self.x_y_coord1[i][1], self.x_y_coord1[i+1][0], self.x_y_coord1[i+1][1], width=2, fill="red")
                    i=0

                    self.x_y_poligon1 = []
                    for n in self.x_y_coord1:
                        self.x_y_poligon1 += n

                    self.canvas.create_polygon(self.x_y_poligon1, fill='red', stipple="gray12")



                for j in range(len(self.x_y_coord2) - 1):
                    self.canvas.create_line(self.x_y_coord2[j][0], self.x_y_coord2[j][1], self.x_y_coord2[j + 1][0],
                                            self.x_y_coord2[j + 1][1], width=2, fill="blue")
                    j = 0

                    self.x_y_poligon2 = []
                    for n in self.x_y_coord2:
                        self.x_y_poligon2 += n

                    self.canvas.create_polygon(self.x_y_poligon2, fill='blue', stipple="gray12")

                for k in range(len(self.x_y_coord3) - 1):
                    self.canvas.create_line(self.x_y_coord3[k][0], self.x_y_coord3[k][1], self.x_y_coord3[k + 1][0],
                                            self.x_y_coord3[k + 1][1], width=2, fill="yellow")
                    k = 0

                    self.x_y_poligon3 = []
                    for n in self.x_y_coord3:
                        self.x_y_poligon3 += n

                    self.canvas.create_polygon(self.x_y_poligon3, fill='yellow', stipple="gray12")

                for l in range(len(self.x_y_coord4) - 1):
                    self.canvas.create_line(self.x_y_coord4[l][0], self.x_y_coord4[l][1], self.x_y_coord4[l + 1][0],
                                            self.x_y_coord4[l + 1][1], width=2, fill="green")
                    l = 0

                    self.x_y_poligon4 = []
                    for n in self.x_y_coord4:
                        self.x_y_poligon4 += n

                    self.canvas.create_polygon(self.x_y_poligon4, fill='green', stipple="gray12")


            # print ("custom geof", len(self.x_y_coord1), len(self.x_y_coord2), len(self.x_y_coord3), len(self.x_y_coord4))

    def TelemetriaControlClicked(self):

        global Telemcreado
        global cargarGeof

        if not cargarGeof:
            messagebox.showinfo("warning", "No se ha cargado el Geofence")

        if cargarGeof:

            print("Accediendo a Telemetría y Control")
            self.cargarParametrosConfObject = ConfiguraciónyConexiónClass()
            self.altura_toff1, self.altura_toff2, self.altura_toff3, self.altura_toff4 = self.cargarParametrosConfObject.cargarAltura()
            newWindow = ctk.CTkToplevel(self.Mainframe)
            newWindow.title("Telemetría y Control")
            newWindow.geometry("600x335")
            newWindow.grab_set()

            self.controlFrameObject = TelemetríayControlClass()
            self.controlFrame= self.controlFrameObject.BuildFrame(newWindow, self.client, self.altura_toff1, self.altura_toff2, self.altura_toff3, self.altura_toff4)
            self.controlFrame.pack(fill="both", expand="yes", padx=10, pady=10)
            # self.controlFrameObject.setTelemetryInfo(vel, alt)
            # print ("velocidad enviada", self.vel)
            # print ("altitud enviada", self.alt)
            Telemcreado = True


    def drawDrone(self, lat, lon, drone, state):


        self.OO = [41.27640942348419, 1.9886658713221552]
        # self.AA = [41.27643361279337, 1.988196484744549]
        # self.BB = [41.27663317425185, 1.9890118762850764]
        # self.CC = [41.27635096595008, 1.9891352578997614]
        # self.DD = [41.27615341941283, 1.9883145019412043]

        self.AA = [41.2764267, 1.9882317]
        self.BB = [41.2766066, 1.9890182]
        self.CC = [41.2763652, 1.98911288]
        self.DD = [41.2761717, 1.9883336]
        self.AB1 = [((self.BB[0] - self.AA[0]) / 4) + self.AA[0], ((self.BB[1] - self.AA[1]) / 4) + self.AA[1]]
        self.AB2 = [((self.BB[0] - self.AA[0]) / 2) + self.AA[0], ((self.BB[1] - self.AA[1]) / 2) + self.AA[1]]
        self.AB3 = [((self.BB[0] - self.AA[0]) * 3 / 4) + self.AA[0], ((self.BB[1] - self.AA[1]) * 3 / 4) + self.AA[1]]
        self.DC1 = [((self.CC[0] - self.DD[0]) / 4) + self.DD[0], ((self.CC[1] - self.DD[1]) / 4) + self.DD[1]]
        self.DC2 = [((self.CC[0] - self.DD[0]) / 2) + self.DD[0], ((self.CC[1] - self.DD[1]) / 2) + self.DD[1]]
        self.DC3 = [((self.CC[0] - self.DD[0]) * 3 / 4) + self.DD[0], ((self.CC[1] - self.DD[1]) * 3 / 4) + self.DD[1]]
        self.AD1 = [((self.AA[0] - self.DD[0]) / 2) + self.DD[0], ((self.DD[1] - self.AA[1]) / 2) + self.AA[1]]
        self.BC1 = [((self.BB[0] - self.CC[0]) / 2) + self.CC[0], ((self.CC[1] - self.BB[1]) / 2) + self.BB[1]]
        self.MM = [((self.AB2[0] - self.DC2[0]) / 2) + self.DC2[0], ((self.BC1[1] - self.AD1[1]) / 2) + self.AD1[1]]

        # self.xcoord_canv = ((lon-self.AA[1])*(1170-170)/(self.BB[1]-self.AA[1])) + 170
        # self.ycoord_canv = ((lat-self.DD[0])*(575-145)/(self.AA[0]-self.DD[0])) - 140
        self.xcoord_canv, self.ycoord_canv = self.conversor.convertToCoords([lat, lon])

        # self.xcoord_canv_conv = self.xcoord_canv*math.cos(20*math.pi/180)
        # self.ycoord_canv_conv = self.xcoord_canv*math.sin(20*math.pi/180) +145

        self.ov_x0 = self.xcoord_canv - 15
        self.ov_y0 = self.ycoord_canv - 15
        self.ov_x1 = self.xcoord_canv + 15
        self.ov_y1 = self.ycoord_canv + 15

        # print ("xcord", self.xcoord_canv)
        # print ("ycord", self.ycoord_canv)

        if drone == "d1":

            if not self.cd1:

                if state == "volando":
                    self.drone1 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1, fill="red")
                else:
                    self.drone1 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1, outline="red",
                                                          width=3)

                self.cd1 = True

            if self.cd1:

                self.canvas.delete(self.drone1)
                if state == "volando":
                    self.drone1 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1, fill="red")
                else:
                    self.drone1 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1, outline="red",
                                                          width=3)

        if drone == "d2":

            if not self.cd2:

                if state == "volando":
                    self.drone2 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1, fill="blue")
                else:
                    self.drone2 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1, outline="blue", width=3)

                self.cd2 = True

            if self.cd2:

                self.canvas.delete(self.drone2)
                if state == "volando":
                    self.drone2 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1, fill="blue")
                else:
                    self.drone2 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1,
                                                          outline="blue", width=3)

        if drone == "d3":

            if not self.cd3:

                if state == "volando":
                    self.drone3 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1, fill="yellow")
                else:
                    self.drone3 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1, outline="yellow", width=3)


                self.cd3 = True

            if self.cd3:

                self.canvas.delete(self.drone3)
                if state == "volando":
                    self.drone3 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1, fill="yellow")
                else:
                    self.drone3 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1,
                                                          outline="yellow", width=3)

        if drone == "d4":

            if not self.cd4:

                if state == "volando":
                    self.drone4 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1, fill="green")
                else:
                    self.drone4 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1, outline="green", width=3)


                self.cd4 = True

            if self.cd4:

                self.canvas.delete(self.drone4)
                if state == "volando":
                    self.drone4 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1, fill="green")
                else:
                    self.drone4 = self.canvas.create_oval(self.ov_x0, self.ov_y0, self.ov_x1, self.ov_y1,
                                                          outline="green", width=3)










if __name__ == "__main__":

    import sys

    connection_mode = sys.argv[1]  # global or local
    operation_mode = sys.argv[2]  # simulation or production
    username = None
    password = None
    if connection_mode == 'global':
        external_broker = sys.argv[3]
        if external_broker == 'classpip_cred' or external_broker == 'classpip_cert':
            username = sys.argv[4]
            password = sys.argv[5]
    else:
        external_broker = None


    app = App()
    app.mainloop()

