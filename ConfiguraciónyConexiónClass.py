import json
import threading
from tkinter import messagebox

import customtkinter as ctk
import tkinter as tk
import time
import os
from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from PIL import Image
import paho.mqtt.client as mqtt
from GeofenceDesignClass import GeofenceDesignClass

global altura_drone1
global altura_drone2
global altura_drone3
global altura_drone4
global Ndrones


d1connected = False
d2connected = False
d3connected = False
d4connected = False
geofence = False
param1_conf = False
param2_conf = False
param3_conf = False
param4_conf = False
replica = False

class ConfiguraciónyConexiónClass:



    def BuildFrame (self, fatherFrame, client):

        self.client = client
        global Ndrones

        self.AskNdrones = ctk.CTkInputDialog(title='Ndrones', text='¿Cuantos drones quieres volar?')
        Ndrones = self.AskNdrones.get_input()

        self.radio_var1 = tk.IntVar(value=0)
        self.radio_var2 = tk.IntVar(value=0)
        self.radio_var3 = tk.IntVar(value=0)
        self.radio_var4 = tk.IntVar(value=0)
        self.ConnectionFrame =ctk.CTkFrame(fatherFrame)
        self.ConnectionFrame.rowconfigure(0, weight=1)
        self.ConnectionFrame.rowconfigure(1, weight=10)
        self.ConnectionFrame.rowconfigure(2, weight=1)
        self.ConnectionFrame.rowconfigure(3, weight=10)
        self.ConnectionFrame.rowconfigure(4, weight=1)
        self.ConnectionFrame.columnconfigure(0, weight=1)
        self.ConnectionFrame.columnconfigure(1, weight=1)

        self.geofencebutton = ctk.CTkButton(self.ConnectionFrame, text='Configurar geofence',
                                              command=self.Geofencebuttonclicked)
        self.geofencebutton.grid(row=0, column=0, columnspan=2,  padx=20, pady=10)
        # self.conf_param = ctk.CTkButton(self.ConnectionFrame, text='Configurar parámetros',
        #                                       command=self.conf_param1_clicked)
        # self.conf_param.grid(row=0, column=1, padx=20, pady=10)

        self.Button1 = ctk.CTkButton(self.ConnectionFrame, text="drone1", fg_color="red", text_color="black",
                                     command=self.Button1Clicked)
        self.Button1.grid(row=1, column=0, padx=10, pady=10, sticky="nesw")
        self.radiobutton_frame1 = ctk.CTkFrame(self.ConnectionFrame)
        self.radiobutton_frame1.grid(row=2, column=0, padx=(5, 5), pady=(5, 0), sticky="nsew")
        self.radiobutton_frame1.rowconfigure(0, weight=1)
        self.radiobutton_frame1.rowconfigure(1, weight=1)
        self.radiobutton_frame1.columnconfigure(0, weight=1)
        self.radiobutton_frame1.columnconfigure(1, weight=1)

        # self.radio_button_1 = ctk.CTkRadioButton(master=self.radiobutton_frame1, text="Conexión global",
        #                                          variable=self.radio_var1,
        #                                          value=0)
        # self.radio_button_1.grid(row=0, column=0, pady=10, padx=20, sticky="n")
        # self.radio_button_11 = ctk.CTkRadioButton(master=self.radiobutton_frame1, text="Conexión directa",
        #                                          variable=self.radio_var1,
        #                                          value=1)
        # self.radio_button_11.grid(row=0, column=1, pady=10, padx=20, sticky="n")
        self.param_conf1 = ctk.CTkButton(self.radiobutton_frame1, text='Configurar parámetros',
                                              command=self.conf_param1_clicked)
        self.param_conf1.grid(row=1, column=0, columnspan=2,  padx=20, pady=10)



        self.Button2 = ctk.CTkButton(self.ConnectionFrame, text="drone2", fg_color="red", text_color="black",
                                     command=self.Button2Clicked)
        self.Button2.grid(row=1, column=1, padx=10, pady=10, sticky="nesw")
        self.radiobutton_frame2 = ctk.CTkFrame(self.ConnectionFrame)
        self.radiobutton_frame2.grid(row=2, column=1, padx=(5, 5), pady=(5, 0), sticky="nsew")
        self.radiobutton_frame2.rowconfigure(0, weight=1)
        self.radiobutton_frame2.rowconfigure(1, weight=1)
        self.radiobutton_frame2.columnconfigure(0, weight=1)
        self.radiobutton_frame2.columnconfigure(1, weight=1)

        # self.radio_button_2 = ctk.CTkRadioButton(master=self.radiobutton_frame2, text="Conexión global",
        #                                          variable=self.radio_var2,
        #                                          value=0)
        # self.radio_button_2.grid(row=0, column=0, pady=10, padx=20, sticky="n")
        # self.radio_button_22 = ctk.CTkRadioButton(master=self.radiobutton_frame2, text="Conexión directa",
        #                                           variable=self.radio_var2,
        #                                           value=1)
        # self.radio_button_22.grid(row=0, column=1, pady=10, padx=20, sticky="n")
        self.param_conf2 = ctk.CTkButton(self.radiobutton_frame2, text='Configurar parámetros',
                                             command=self.conf_param2_clicked)
        self.param_conf2.grid(row=1, column=0, columnspan=2,  padx=20, pady=10)


        self.Button3 = ctk.CTkButton(self.ConnectionFrame, text="drone3", fg_color="red", text_color="black",
                                     command=self.Button3Clicked)
        self.Button3.grid(row=3, column=0, padx=10, pady=10, sticky="nesw")
        self.radiobutton_frame3 = ctk.CTkFrame(self.ConnectionFrame)
        self.radiobutton_frame3.grid(row=4, column=0, padx=(5, 5), pady=(5, 0), sticky="nsew")
        self.radiobutton_frame3.rowconfigure(0, weight=1)
        self.radiobutton_frame3.rowconfigure(1, weight=1)
        self.radiobutton_frame3.columnconfigure(0, weight=1)
        self.radiobutton_frame3.columnconfigure(1, weight=1)

        # self.radio_button_3 = ctk.CTkRadioButton(master=self.radiobutton_frame3, text="Conexión global",
        #                                          variable=self.radio_var3,
        #                                          value=0)
        # self.radio_button_3.grid(row=0, column=0, pady=10, padx=20, sticky="n")
        # self.radio_button_33 = ctk.CTkRadioButton(master=self.radiobutton_frame3, text="Conexión directa",
        #                                           variable=self.radio_var3,
        #                                           value=1)
        # self.radio_button_33.grid(row=0, column=1, pady=10, padx=20, sticky="n")
        self.param_conf3 = ctk.CTkButton(self.radiobutton_frame3, text='Configurar parámetros',
                                             command=self.conf_param3_clicked)
        self.param_conf3.grid(row=1, column=0, columnspan=2,  padx=20, pady=10)


        self.Button4 = ctk.CTkButton(self.ConnectionFrame, text="drone4", fg_color="red", text_color="black",
                                     command=self.Button4Clicked)
        self.Button4.grid(row=3, column=1, padx=10, pady=10, sticky="nesw")
        self.radiobutton_frame4 = ctk.CTkFrame(self.ConnectionFrame)
        self.radiobutton_frame4.grid(row=4, column=1, padx=(5, 5), pady=(5, 0), sticky="nsew")
        self.radiobutton_frame4.rowconfigure(0, weight=1)
        self.radiobutton_frame4.rowconfigure(1, weight=1)
        self.radiobutton_frame4.columnconfigure(0, weight=1)
        self.radiobutton_frame4.columnconfigure(1, weight=1)
        # self.radio_button_4 = ctk.CTkRadioButton(master=self.radiobutton_frame4, text="Conexión global",
        #                                          variable=self.radio_var4,
        #                                          value=0)
        # self.radio_button_4.grid(row=0, column=0, pady=10, padx=20, sticky="n")
        # self.radio_button_44 = ctk.CTkRadioButton(master=self.radiobutton_frame4, text="Conexión directa",
        #                                           variable=self.radio_var4,
        #                                           value=1)
        # self.radio_button_44.grid(row=0, column=1, pady=10, padx=20, sticky="n")
        self.param_conf4 = ctk.CTkButton(self.radiobutton_frame4, text='Configurar parámetros',
                                             command=self.conf_param4_clicked)
        self.param_conf4.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        return self.ConnectionFrame, Ndrones


    def getStateInfo (self, st, drone):

        global d1connected
        global d2connected
        global d3connected
        global d4connected
        self.state = st
        self.drone = drone
        # print(self.state)

        if self.drone == "d1":
            if d1connected == False:
                if self.state == "conectado":
                    self.Button1.configure(self, fg_color="green")
                    messagebox.showinfo("Information", "Drone 1 conectado")
                    d1connected = True

        if self.drone == "d2":
            if d2connected == False:
                if self.state == "conectado":
                    self.Button2.configure(self, fg_color="green")
                    messagebox.showinfo("Information", "Drone 2 conectado")
                    d2connected = True

        if self.drone == "d3":
            if d3connected == False:
                if self.state == "conectado":
                    self.Button3.configure(self, fg_color="green")
                    messagebox.showinfo("Information", "Drone 3 conectado")
                    d3connected = True

        if self.drone == "d4":
            if d4connected == False:
                if self.state == "conectado":
                    self.Button4.configure(self, fg_color="green")
                    messagebox.showinfo("Information", "Drone 4 conectado")
                    d4connected = True

    def getParameters(self, drone, FENCE_ALT_MAX_valor, FENCE_ENABLE_valor,
                                                         margen_geof_valor, geof_action_valor, RTL_ALT_valor,
                                                         PILOT_SPEED_UP_valor, FLTMODE6_valor):

        global FENCE_ALT_MAXget1
        global FENCE_ENABLEget1
        global margen_geofget1
        global geof_actionget1
        global RTL_ALTget1
        global PILOT_SPEED_UPget1
        global FLTMODE6get1

        global FENCE_ALT_MAXget2
        global FENCE_ENABLEget2
        global margen_geofget2
        global geof_actionget2
        global RTL_ALTget2
        global PILOT_SPEED_UPget2
        global FLTMODE6get2

        global FENCE_ALT_MAXget3
        global FENCE_ENABLEget3
        global margen_geofget3
        global geof_actionget3
        global RTL_ALTget3
        global PILOT_SPEED_UPget3
        global FLTMODE6get3

        global FENCE_ALT_MAXget4
        global FENCE_ENABLEget4
        global margen_geofget4
        global geof_actionget4
        global RTL_ALTget4
        global PILOT_SPEED_UPget4
        global FLTMODE6get4

        if drone == "d1":
            FENCE_ALT_MAXget1= FENCE_ALT_MAX_valor
            FENCE_ENABLEget1= FENCE_ENABLE_valor
            margen_geofget1 = margen_geof_valor
            geof_actionget1 = geof_action_valor
            RTL_ALTget1= RTL_ALT_valor
            PILOT_SPEED_UPget1= PILOT_SPEED_UP_valor
            FLTMODE6get1= FLTMODE6_valor

        if drone == "d2":
            FENCE_ALT_MAXget2= FENCE_ALT_MAX_valor
            FENCE_ENABLEget2= FENCE_ENABLE_valor
            margen_geofget2 = margen_geof_valor
            geof_actionget2 = geof_action_valor
            RTL_ALTget2= RTL_ALT_valor
            PILOT_SPEED_UPget2= PILOT_SPEED_UP_valor
            FLTMODE6get2= FLTMODE6_valor

        if drone == "d3":
            FENCE_ALT_MAXget3= FENCE_ALT_MAX_valor
            FENCE_ENABLEget3= FENCE_ENABLE_valor
            margen_geofget3 = margen_geof_valor
            geof_actionget3 = geof_action_valor
            RTL_ALTget3= RTL_ALT_valor
            PILOT_SPEED_UPget3= PILOT_SPEED_UP_valor
            FLTMODE6get3= FLTMODE6_valor

        if drone == "d4":
            FENCE_ALT_MAXget4= FENCE_ALT_MAX_valor
            FENCE_ENABLEget4= FENCE_ENABLE_valor
            margen_geofget4 = margen_geof_valor
            geof_actionget4 = geof_action_valor
            RTL_ALTget4= RTL_ALT_valor
            PILOT_SPEED_UPget4= PILOT_SPEED_UP_valor
            FLTMODE6get4= FLTMODE6_valor

    def Geofencebuttonclicked(self):

        global geofence
        global Ndrones

        print("Accediendo a Diseño del Geofence")
        newGeofence = ctk.CTkToplevel(self.ConnectionFrame)
        newGeofence.title("Geofence")
        newGeofence.geometry("870x670")
        newGeofence.grab_set()

        self.geofenceDesignObject = GeofenceDesignClass()
        self.geofenceFrame = self.geofenceDesignObject.BuildFrame(newGeofence, self.client, Ndrones)
        self.geofenceFrame.pack(fill="both", expand="yes", padx=10, pady=10)

        geofence = True


    def conf_param1_clicked(self):

        global altura_drone1
        global geofence
        global param1_conf
        global FENCE_ALT_MAXget1
        global FENCE_ENABLEget1
        global margen_geofget1
        global geof_actionget1
        global RTL_ALTget1
        global PILOT_SPEED_UPget1
        global FLTMODE6get1

        if not geofence:

            messagebox.showinfo("Alert", "No se ha configurado Geofence")

        if not d1connected:
            messagebox.showinfo("Alert", "No se ha conectado el dron 1")

        else:

            self.client.publish("miMain/autopilotService/getParameters")

            time.sleep(3)


            self.conf_param = ctk.CTkToplevel(self.ConnectionFrame)
            self.conf_param.title("Configuración parámetros dron 1")
            self.conf_param.geometry("1000x800")
            self.conf_param.grab_set()

            self.conf_param_Frame = ctk.CTkFrame(self.conf_param)
            self.conf_param_Frame.pack(fill="both", expand="yes", padx=10, pady=10)
            self.conf_param_Frame.rowconfigure(0, weight=1)
            self.conf_param_Frame.rowconfigure(1, weight=1)
            self.conf_param_Frame.rowconfigure(2, weight=1)
            self.conf_param_Frame.rowconfigure(3, weight=1)
            self.conf_param_Frame.rowconfigure(4, weight=1)
            self.conf_param_Frame.rowconfigure(5, weight=1)
            self.conf_param_Frame.rowconfigure(6, weight=1)
            self.conf_param_Frame.rowconfigure(7, weight=1)
            self.conf_param_Frame.rowconfigure(8, weight=1)
            self.conf_param_Frame.rowconfigure(9, weight=1)
            self.conf_param_Frame.rowconfigure(10, weight=1)

            self.conf_param_Frame.columnconfigure(0, weight=1)
            self.conf_param_Frame.columnconfigure(1, weight=1)
            self.conf_param_Frame.columnconfigure(2, weight=1)


            self.param_geofence_PILOT_SPEED_UP = ctk.CTkLabel(self.conf_param_Frame, text="PILOT_SPEED_UP (cm/s)",
                                                              font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_PILOT_SPEED_UP.grid(row=0, column=0, padx=20, pady=(20, 10))
            self.PILOT_SPEED_UP1 = PILOT_SPEED_UPget1
            self.slider_PILOT_SPEED_UP = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=200, number_of_steps=4,
                                               command=self.sliding_PILOT_SPEED_UP1)
            self.slider_PILOT_SPEED_UP.grid(row=0, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
            self.slider_PILOT_SPEED_UP.set(PILOT_SPEED_UPget1)
            self.PILOT_SPEED_UP_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(PILOT_SPEED_UPget1))
            self.PILOT_SPEED_UP_valor.grid(row=0, column=2, padx=10, pady=10)

            self.param_geofence_RTL_ALT = ctk.CTkLabel(self.conf_param_Frame, text="RTL_ALT (m)",
                                                              font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_RTL_ALT.grid(row=1, column=0, padx=20, pady=(20, 10))
            self.RTL_ALT_valor1 = RTL_ALTget1
            self.RTL_ALT = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                     values=[str(RTL_ALTget1), "4", "7", "11"],
                                                     command=self.conf_RTL_ALT1)
            self.RTL_ALT.grid(row=1, column=1, padx=20, pady=(1, 1))

            self.param_geofence_FENCE_ENABLE = ctk.CTkLabel(self.conf_param_Frame, text="FENCE_ENABLE",
                                                       font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_FENCE_ENABLE.grid(row=2, column=0, padx=20, pady=(20, 10))
            self.FENCE_ENABLE_valor1 = FENCE_ENABLEget1
            if FENCE_ENABLEget1 == 1:
                fen_val = "Yes"
                self.fence_enable_param1 = "Yes"

            if FENCE_ENABLEget1 == 0:
                fen_val = "No"
                self.fence_enable_param1 = "No"

            self.FENCE_ENABLE = ctk.CTkOptionMenu(self.conf_param_Frame,
                                             values=[fen_val, "Yes", "No"],
                                             command=self.conf_FENCE_ENABLE1)
            self.FENCE_ENABLE.grid(row=2, column=1, padx=20, pady=(1, 1))

            self.param_geofence_margen = ctk.CTkLabel(self.conf_param_Frame, text="Margen del geofence (m)",
                                           font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_margen.grid(row=3, column=0, padx=20, pady=(20, 10))
            self.margen_geof1 = margen_geofget1
            self.slider_margen = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=5,number_of_steps=10,
                                               command=self.sliding_margen1)
            self.slider_margen.grid(row=3, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
            self.slider_margen.set(margen_geofget1)
            self.margen_geofence_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(margen_geofget1))
            self.margen_geofence_valor.grid(row=3, column=2, padx=10, pady=10)

            self.param_geofence_action = ctk.CTkLabel(self.conf_param_Frame, text="Acción del geofence",
                                                      font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_action.grid(row=4, column=0, padx=20, pady=(20, 10))
            self.geof_action1 = geof_actionget1
            if geof_actionget1 == 1:
                gact_val = "RTL or Land"
                self.geof_action_param1= "RTL or Land"
            if geof_actionget1 == 2:
                gact_val = "Always Land"
                self.geof_action_param1= "Always Land"
            if geof_actionget1 == 4:
                gact_val = "Brake or Land"
                self.geof_action_param1= "Brake or Land"


            self.geofence_action = ctk.CTkOptionMenu(self.conf_param_Frame, values=[gact_val, "RTL or Land",
                                                                                    "Always Land", "Brake or Land"],
                                                                           command=self.conf_geof_action1)
            self.geofence_action.grid(row=4, column=1, padx=20, pady=(1, 1))
            self.altura_takeoff_label = ctk.CTkLabel(self.conf_param_Frame, text="Altura Take Off (m)",
                                                      font=ctk.CTkFont(size=20, weight="bold"))
            self.altura_takeoff_label.grid(row=5, column=0, padx=20, pady=(20, 10))
            altura_drone1 = 5
            self.slider_altura_takeoff = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=10, number_of_steps=10,
                                               command=self.sliding_altura1)
            self.slider_altura_takeoff.grid(row=5, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
            self.slider_altura_takeoff.set(5)


            self.altura_takeoff_valor = ctk.CTkLabel(self.conf_param_Frame, text="5")
            self.altura_takeoff_valor.grid(row=5, column=2, padx=10, pady=10)

            self.param_geofence_FENCE_ALT_MAX = ctk.CTkLabel(self.conf_param_Frame, text="FENCE_ALT_MAX (m)",
                                                       font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_FENCE_ALT_MAX.grid(row=6, column=0, padx=20, pady=(20, 10))
            self.FENCE_ALT_MAX_valor1 = FENCE_ALT_MAXget1

            self.FENCE_ALT_MAX = ctk.CTkOptionMenu(self.conf_param_Frame,
                                             values=[str(FENCE_ALT_MAXget1), "5", "8", "12"],
                                             command=self.conf_FENCE_ALT_MAX1)
            self.FENCE_ALT_MAX.grid(row=6, column=1, padx=20, pady=(1, 1))


            self.param_geofence_FLTMODE6 = ctk.CTkLabel(self.conf_param_Frame, text="FLTMODE6",
                                                             font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_FLTMODE6.grid(row=7, column=0, padx=20, pady=(20, 10))
            self.FLTMODE6_valor1 = FLTMODE6get1
            if FLTMODE6get1 == 6:
                FLT_val = "RTL"
                self.FLTMODE_param1= "RTL"

            if FLTMODE6get1 == 9:
                FLT_val = "LAND"
                self.FLTMODE_param1= "LAND"
            if FLTMODE6get1 == 0:
                FLT_val = "None"
                self.FLTMODE_param1 = "None"

            self.FLTMODE6 = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                   values=[FLT_val, "RTL", "LAND"],
                                                   command=self.conf_FLTMODE61)
            self.FLTMODE6.grid(row=7, column=1, padx=20, pady=(1, 1))

            self.param_Modo_conexion = ctk.CTkLabel(self.conf_param_Frame, text="Modo conexión",
                                                            font=ctk.CTkFont(size=20, weight="bold"))
            self.param_Modo_conexion.grid(row=8, column=0, padx=20, pady=(20, 10))
            self.Modo_conexion = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                  values=["", "Global", "Directa"],
                                                  command=self.modo_conexion1)
            self.Modo_conexion.grid(row=8, column=1, padx=20, pady=(1, 1))

            self.param_replica = ctk.CTkLabel(self.conf_param_Frame, text="¿Replicar parámetros?",
                                                    font=ctk.CTkFont(size=20, weight="bold"))
            self.param_replica.grid(row=9, column=0, padx=20, pady=(20, 10))
            self.replica = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                   values=["", "Si", "No"],
                                                   command=self.conf_param_replica)
            self.replica.grid(row=9, column=1, padx=20, pady=(1, 1))

            param1_conf = True

            self.aceptar_param_1 = ctk.CTkButton(self.conf_param_Frame, text='Aceptar',
                                                command=self.aceptar_param_1_clicked)
            self.aceptar_param_1.grid(row=10, column=0, columnspan=3, padx=20, pady=(1, 1))



    def conf_param2_clicked(self):

        global geofence
        global param2_conf
        global replica
        global FENCE_ALT_MAXget2
        global FENCE_ENABLEget2
        global margen_geofget2
        global geof_actionget2
        global RTL_ALTget2
        global PILOT_SPEED_UPget2
        global FLTMODE6get2

        if not geofence:

            messagebox.showinfo("Alert", "No se ha configurado Geofence")

        if not d2connected:
            messagebox.showinfo("Alert", "No se ha conectado el dron 2")

        else:

            self.client.publish("miMain/autopilotService2/getParameters")

            time.sleep(3)

            self.conf_param = ctk.CTkToplevel(self.ConnectionFrame)
            self.conf_param.title("Configuración parámetros dron 2")
            self.conf_param.geometry("1000x600")
            self.conf_param.grab_set()

            self.conf_param_Frame = ctk.CTkFrame(self.conf_param)
            self.conf_param_Frame.pack(fill="both", expand="yes", padx=10, pady=10)
            self.conf_param_Frame.rowconfigure(0, weight=1)
            self.conf_param_Frame.rowconfigure(1, weight=1)
            self.conf_param_Frame.rowconfigure(2, weight=1)
            self.conf_param_Frame.rowconfigure(3, weight=1)
            self.conf_param_Frame.rowconfigure(4, weight=1)
            self.conf_param_Frame.rowconfigure(5, weight=1)
            self.conf_param_Frame.rowconfigure(6, weight=1)
            self.conf_param_Frame.rowconfigure(7, weight=1)
            self.conf_param_Frame.rowconfigure(8, weight=1)
            self.conf_param_Frame.rowconfigure(9, weight=1)

            self.conf_param_Frame.columnconfigure(0, weight=1)
            self.conf_param_Frame.columnconfigure(1, weight=1)
            self.conf_param_Frame.columnconfigure(2, weight=1)


            self.param_geofence_PILOT_SPEED_UP = ctk.CTkLabel(self.conf_param_Frame, text="PILOT_SPEED_UP (cm/s)",
                                                              font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_PILOT_SPEED_UP.grid(row=0, column=0, padx=20, pady=(20, 10))
            self.PILOT_SPEED_UP2 = PILOT_SPEED_UPget2
            self.slider_PILOT_SPEED_UP = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=200, number_of_steps=4,
                                               command=self.sliding_PILOT_SPEED_UP2)
            self.slider_PILOT_SPEED_UP.grid(row=0, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
            if replica:
                self.PILOT_SPEED_UP2 = self.PILOT_SPEED_UP1
                self.slider_PILOT_SPEED_UP.set(float(self.PILOT_SPEED_UP1))
                self.PILOT_SPEED_UP_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(round(self.PILOT_SPEED_UP1, 0)))
                self.PILOT_SPEED_UP_valor.grid(row=0, column=2, padx=10, pady=10)
            else:
                self.slider_PILOT_SPEED_UP.set(PILOT_SPEED_UPget2)
                self.PILOT_SPEED_UP_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(PILOT_SPEED_UPget2))
                self.PILOT_SPEED_UP_valor.grid(row=0, column=2, padx=10, pady=10)


            self.param_geofence_RTL_ALT = ctk.CTkLabel(self.conf_param_Frame, text="RTL_ALT (m)",
                                                              font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_RTL_ALT.grid(row=1, column=0, padx=20, pady=(20, 10))

            self.RTL_ALT_valor2 = RTL_ALTget2

            if replica:
                self.RTL_ALT_valor2 = self.RTL_ALT_valor1
                self.RTL_ALT = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                 values=[str(self.RTL_ALT_valor1)],
                                                 command=self.conf_RTL_ALT2)
                self.RTL_ALT.grid(row=1, column=1, padx=20, pady=(1, 1))
            else:
                self.RTL_ALT = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                         values=[str(RTL_ALTget2), "4", "7", "11"],
                                                         command=self.conf_RTL_ALT2)
                self.RTL_ALT.grid(row=1, column=1, padx=20, pady=(1, 1))

            self.param_geofence_FENCE_ENABLE = ctk.CTkLabel(self.conf_param_Frame, text="FENCE_ENABLE",
                                                       font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_FENCE_ENABLE.grid(row=2, column=0, padx=20, pady=(20, 10))

            self.FENCE_ENABLE_valor2 = FENCE_ENABLEget2
            if FENCE_ENABLEget2 == 1:
                fen_val = "Yes"

            if FENCE_ENABLEget2 == 0:
                fen_val = "No"

            if replica:
                self.FENCE_ENABLE_valor2 = self.FENCE_ENABLE_valor1
                self.FENCE_ENABLE = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                      values=[self.fence_enable_param1],
                                                      command=self.conf_FENCE_ENABLE2)
                self.FENCE_ENABLE.grid(row=2, column=1, padx=20, pady=(1, 1))
            else:

                self.FENCE_ENABLE = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                 values=[fen_val, "Yes", "No"],
                                                 command=self.conf_FENCE_ENABLE2)
                self.FENCE_ENABLE.grid(row=2, column=1, padx=20, pady=(1, 1))

            self.param_geofence_margen = ctk.CTkLabel(self.conf_param_Frame, text="Margen del geofence (m)",
                                           font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_margen.grid(row=3, column=0, padx=20, pady=(20, 10))
            self.margen_geof2 = margen_geofget2
            if replica:
                self.margen_geof2 = self.margen_geof1
                self.slider_margen = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=5, number_of_steps=10,
                                                   command=self.sliding_margen2)
                self.slider_margen.grid(row=3, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
                self.slider_margen.set(float(self.margen_geof1))
                self.margen_geofence_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(round(self.margen_geof1, 1)))
                self.margen_geofence_valor.grid(row=3, column=2, padx=10, pady=10)

            else:
                self.slider_margen = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=5,number_of_steps=10,
                                                   command=self.sliding_margen2)
                self.slider_margen.grid(row=3, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
                self.slider_margen.set(margen_geofget2)
                self.margen_geofence_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(margen_geofget2))
                self.margen_geofence_valor.grid(row=3, column=2, padx=10, pady=10)

            self.param_geofence_action = ctk.CTkLabel(self.conf_param_Frame, text="Acción del geofence",
                                                      font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_action.grid(row=4, column=0, padx=20, pady=(20, 10))

            self.geof_action2 = geof_actionget2
            if geof_actionget2 == 1:
                gact_val = "RTL or Land"
            if geof_actionget2 == 2:
                gact_val = "Always Land"
            if geof_actionget2 == 4:
                gact_val = "Brake or Land"

            if replica:
                self.geof_action2 = self.geof_action1
                self.geofence_action = ctk.CTkOptionMenu(self.conf_param_Frame, values=[self.geof_action_param1],
                                                         command=self.conf_geof_action2)
                self.geofence_action.grid(row=4, column=1, padx=20, pady=(1, 1))
            else:
                self.geofence_action = ctk.CTkOptionMenu(self.conf_param_Frame, values=[gact_val, "RTL or Land",
                                                                                        "Always Land", "Brake or Land"],
                                                                               command=self.conf_geof_action2)
                self.geofence_action.grid(row=4, column=1, padx=20, pady=(1, 1))
            self.altura_takeoff_label = ctk.CTkLabel(self.conf_param_Frame, text="Altura Take Off (m)",
                                                      font=ctk.CTkFont(size=20, weight="bold"))
            self.altura_takeoff_label.grid(row=5, column=0, padx=20, pady=(20, 10))
            if replica:
                self.slider_altura_takeoff = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=10, number_of_steps=10,
                                                           command=self.sliding_altura2)
                self.slider_altura_takeoff.grid(row=5, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
                self.slider_altura_takeoff.set(float(altura_drone1))
                self.altura_takeoff_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(round(altura_drone1,0)))
                self.altura_takeoff_valor.grid(row=5, column=2, padx=10, pady=10)

            else:
                self.slider_altura_takeoff = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=10, number_of_steps=10,
                                                   command=self.sliding_altura2)
                self.slider_altura_takeoff.grid(row=5, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
                self.slider_altura_takeoff.set(5)
                self.altura_takeoff_valor = ctk.CTkLabel(self.conf_param_Frame, text="5")
                self.altura_takeoff_valor.grid(row=5, column=2, padx=10, pady=10)

            self.param_geofence_FENCE_ALT_MAX = ctk.CTkLabel(self.conf_param_Frame, text="FENCE_ALT_MAX (m)",
                                                       font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_FENCE_ALT_MAX.grid(row=6, column=0, padx=20, pady=(20, 10))

            self.FENCE_ALT_MAX_valor2 = FENCE_ALT_MAXget2

            if replica:
                self.FENCE_ALT_MAX_valor2 = self.FENCE_ALT_MAX_valor1
                self.FENCE_ALT_MAX = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                       values=[str(self.FENCE_ALT_MAX_valor1)],
                                                       command=self.conf_FENCE_ALT_MAX2)
                self.FENCE_ALT_MAX.grid(row=6, column=1, padx=20, pady=(1, 1))
            else:
                self.FENCE_ALT_MAX = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                 values=[str(FENCE_ALT_MAXget2), "5", "8", "12"],
                                                 command=self.conf_FENCE_ALT_MAX2)
                self.FENCE_ALT_MAX.grid(row=6, column=1, padx=20, pady=(1, 1))

            self.param_geofence_FLTMODE6 = ctk.CTkLabel(self.conf_param_Frame, text="FLTMODE6",
                                                             font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_FLTMODE6.grid(row=7, column=0, padx=20, pady=(20, 10))

            self.FLTMODE6_valor2 = FLTMODE6get2
            if FLTMODE6get2 == 6:
                FLT_val = "RTL"

            if FLTMODE6get2 == 9:
                FLT_val = "LAND"

            if replica:
                self.FLTMODE6_valor2 = self.FLTMODE6_valor1
                self.FLTMODE6 = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                  values=[self.FLTMODE_param1],
                                                  command=self.conf_FLTMODE62)
                self.FLTMODE6.grid(row=7, column=1, padx=20, pady=(1, 1))
            else:
                self.FLTMODE6 = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                       values=[FLT_val, "RTL", "LAND"],
                                                       command=self.conf_FLTMODE62)
                self.FLTMODE6.grid(row=7, column=1, padx=20, pady=(1, 1))
            self.param_Modo_conexion = ctk.CTkLabel(self.conf_param_Frame, text="Modo conexión",
                                                            font=ctk.CTkFont(size=20, weight="bold"))
            self.param_Modo_conexion.grid(row=8, column=0, padx=20, pady=(20, 10))
            if replica:
                self.Modo_conexion = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                       values=[self.modo_con_param1],
                                                       command=self.modo_conexion2)
                self.Modo_conexion.grid(row=8, column=1, padx=20, pady=(1, 1))
            else:
                self.Modo_conexion = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                      values=["", "Global", "Directa"],
                                                      command=self.modo_conexion2)
                self.Modo_conexion.grid(row=8, column=1, padx=20, pady=(1, 1))

            param2_conf = True

            self.aceptar_param_2 = ctk.CTkButton(self.conf_param_Frame, text='Aceptar',
                                                 command=self.aceptar_param_2_clicked)
            self.aceptar_param_2.grid(row=9, column=0, columnspan=3, padx=20, pady=(1, 1))

    def conf_param3_clicked(self):

        global geofence
        global param3_conf
        global replica
        global FENCE_ALT_MAXget3
        global FENCE_ENABLEget3
        global margen_geofget3
        global geof_actionget3
        global RTL_ALTget3
        global PILOT_SPEED_UPget3
        global FLTMODE6get3

        if not geofence:

            messagebox.showinfo("Alert", "No se ha configurado Geofence")

        if not d3connected:
            messagebox.showinfo("Alert", "No se ha conectado el dron 3")

        else:

            self.client.publish("miMain/autopilotService3/getParameters")

            time.sleep(3)

            self.conf_param = ctk.CTkToplevel(self.ConnectionFrame)
            self.conf_param.title("Configuración parámetros dron 3")
            self.conf_param.geometry("1000x600")
            self.conf_param.grab_set()

            self.conf_param_Frame = ctk.CTkFrame(self.conf_param)
            self.conf_param_Frame.pack(fill="both", expand="yes", padx=10, pady=10)
            self.conf_param_Frame.rowconfigure(0, weight=1)
            self.conf_param_Frame.rowconfigure(1, weight=1)
            self.conf_param_Frame.rowconfigure(2, weight=1)
            self.conf_param_Frame.rowconfigure(3, weight=1)
            self.conf_param_Frame.rowconfigure(4, weight=1)
            self.conf_param_Frame.rowconfigure(5, weight=1)
            self.conf_param_Frame.rowconfigure(6, weight=1)
            self.conf_param_Frame.rowconfigure(7, weight=1)
            self.conf_param_Frame.rowconfigure(8, weight=1)
            self.conf_param_Frame.rowconfigure(9, weight=1)

            self.conf_param_Frame.columnconfigure(0, weight=1)
            self.conf_param_Frame.columnconfigure(1, weight=1)
            self.conf_param_Frame.columnconfigure(2, weight=1)


            self.param_geofence_PILOT_SPEED_UP = ctk.CTkLabel(self.conf_param_Frame, text="PILOT_SPEED_UP (cm/s)",
                                                              font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_PILOT_SPEED_UP.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.PILOT_SPEED_UP3 = PILOT_SPEED_UPget3

            self.slider_PILOT_SPEED_UP = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=200, number_of_steps=4,
                                               command=self.sliding_PILOT_SPEED_UP3)
            self.slider_PILOT_SPEED_UP.grid(row=0, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
            if replica:
                self.PILOT_SPEED_UP3 = self.PILOT_SPEED_UP1
                self.slider_PILOT_SPEED_UP.set(float(self.PILOT_SPEED_UP1))
                self.PILOT_SPEED_UP_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(round(self.PILOT_SPEED_UP1, 0)))
                self.PILOT_SPEED_UP_valor.grid(row=0, column=2, padx=10, pady=10)
            else:
                self.slider_PILOT_SPEED_UP.set(PILOT_SPEED_UPget3)
                self.PILOT_SPEED_UP_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(PILOT_SPEED_UPget3))
                self.PILOT_SPEED_UP_valor.grid(row=0, column=2, padx=10, pady=10)

            self.param_geofence_RTL_ALT = ctk.CTkLabel(self.conf_param_Frame, text="RTL_ALT (m)",
                                                              font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_RTL_ALT.grid(row=1, column=0, padx=20, pady=(20, 10))

            self.RTL_ALT_valor3 = RTL_ALTget3

            if replica:
                self.RTL_ALT_valor3 = self.RTL_ALT_valor1
                self.RTL_ALT = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                 values=[str(self.RTL_ALT_valor1)],
                                                 command=self.conf_RTL_ALT3)
                self.RTL_ALT.grid(row=1, column=1, padx=20, pady=(1, 1))
            else:
                self.RTL_ALT = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                 values=[str(RTL_ALTget3), "4", "7", "11"],
                                                 command=self.conf_RTL_ALT3)
                self.RTL_ALT.grid(row=1, column=1, padx=20, pady=(1, 1))

            self.param_geofence_FENCE_ENABLE = ctk.CTkLabel(self.conf_param_Frame, text="FENCE_ENABLE",
                                                       font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_FENCE_ENABLE.grid(row=2, column=0, padx=20, pady=(20, 10))

            self.FENCE_ENABLE_valor3 = FENCE_ENABLEget3
            if FENCE_ENABLEget3 == 1:
                fen_val = "Yes"

            if FENCE_ENABLEget3 == 0:
                fen_val = "No"

            if replica:
                self.FENCE_ENABLE_valor3 = self.FENCE_ENABLE_valor1
                self.FENCE_ENABLE = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                      values=[self.fence_enable_param1],
                                                      command=self.conf_FENCE_ENABLE3)
                self.FENCE_ENABLE.grid(row=2, column=1, padx=20, pady=(1, 1))
            else:
                self.FENCE_ENABLE = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                 values=[fen_val, "Yes", "No"],
                                                 command=self.conf_FENCE_ENABLE3)
                self.FENCE_ENABLE.grid(row=2, column=1, padx=20, pady=(1, 1))

            self.param_geofence_margen = ctk.CTkLabel(self.conf_param_Frame, text="Margen del geofence (m)",
                                           font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_margen.grid(row=3, column=0, padx=20, pady=(20, 10))
            self.margen_geof3 = margen_geofget3

            if replica:
                self.margen_geof3 = self.margen_geof1
                self.slider_margen = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=5, number_of_steps=10,
                                                   command=self.sliding_margen3)
                self.slider_margen.grid(row=3, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
                self.slider_margen.set(float(self.margen_geof1))
                self.margen_geofence_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(round(self.margen_geof1, 1)))
                self.margen_geofence_valor.grid(row=3, column=2, padx=10, pady=10)

            else:
                self.slider_margen = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=5,number_of_steps=10,
                                                   command=self.sliding_margen3)
                self.slider_margen.grid(row=3, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
                self.slider_margen.set(margen_geofget3)
                self.margen_geofence_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(margen_geofget3))
                self.margen_geofence_valor.grid(row=3, column=2, padx=10, pady=10)


            self.param_geofence_action = ctk.CTkLabel(self.conf_param_Frame, text="Acción del geofence",
                                                      font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_action.grid(row=4, column=0, padx=20, pady=(20, 10))
            self.geof_action3 = geof_actionget3
            if geof_actionget3 == 1:
                gact_val = "RTL or Land"
            if geof_actionget3 == 2:
                gact_val = "Always Land"
            if geof_actionget3 == 4:
                gact_val = "Brake or Land"

            if replica:
                self.geof_action3 = self.geof_action1
                self.geofence_action = ctk.CTkOptionMenu(self.conf_param_Frame, values=[self.geof_action_param1],
                                                         command=self.conf_geof_action3)
                self.geofence_action.grid(row=4, column=1, padx=20, pady=(1, 1))
            else:
                self.geofence_action = ctk.CTkOptionMenu(self.conf_param_Frame, values=[gact_val, "RTL or Land",
                                                                                        "Always Land", "Brake or Land"],
                                                                               command=self.conf_geof_action3)
                self.geofence_action.grid(row=4, column=1, padx=20, pady=(1, 1))
            self.altura_takeoff_label = ctk.CTkLabel(self.conf_param_Frame, text="Altura Take Off (m)",
                                                      font=ctk.CTkFont(size=20, weight="bold"))
            self.altura_takeoff_label.grid(row=5, column=0, padx=20, pady=(20, 10))
            if replica:
                self.slider_altura_takeoff = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=10, number_of_steps=10,
                                                           command=self.sliding_altura3)
                self.slider_altura_takeoff.grid(row=5, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
                self.slider_altura_takeoff.set(float(altura_drone1))
                self.altura_takeoff_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(round(altura_drone1, 0)))
                self.altura_takeoff_valor.grid(row=5, column=2, padx=10, pady=10)

            else:
                self.slider_altura_takeoff = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=10, number_of_steps=10,
                                                   command=self.sliding_altura3)
                self.slider_altura_takeoff.grid(row=5, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
                self.slider_altura_takeoff.set(5)
                self.altura_takeoff_valor = ctk.CTkLabel(self.conf_param_Frame, text="5")
                self.altura_takeoff_valor.grid(row=5, column=2, padx=10, pady=10)

            self.param_geofence_FENCE_ALT_MAX = ctk.CTkLabel(self.conf_param_Frame, text="FENCE_ALT_MAX (m)",
                                                       font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_FENCE_ALT_MAX.grid(row=6, column=0, padx=20, pady=(20, 10))
            self.FENCE_ALT_MAX_valor3 = FENCE_ALT_MAXget3

            if replica:
                self.FENCE_ALT_MAX_valor3 = self.FENCE_ALT_MAX_valor1
                self.FENCE_ALT_MAX = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                       values=[str(self.FENCE_ALT_MAX_valor1)],
                                                       command=self.conf_FENCE_ALT_MAX3)
                self.FENCE_ALT_MAX.grid(row=6, column=1, padx=20, pady=(1, 1))
            else:
                self.FENCE_ALT_MAX = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                 values=[str(FENCE_ENABLEget3), "5", "8", "12"],
                                                 command=self.conf_FENCE_ALT_MAX3)
                self.FENCE_ALT_MAX.grid(row=6, column=1, padx=20, pady=(1, 1))

            self.param_geofence_FLTMODE6 = ctk.CTkLabel(self.conf_param_Frame, text="FLTMODE6",
                                                             font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_FLTMODE6.grid(row=7, column=0, padx=20, pady=(20, 10))
            self.FLTMODE6_valor3 = FLTMODE6get3
            if FLTMODE6get3 == 6:
                FLT_val = "RTL"

            if FLTMODE6get3 == 9:
                FLT_val = "LAND"

            if replica:
                self.FLTMODE6_valor3 = self.FLTMODE6_valor1
                self.FLTMODE6 = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                  values=[self.FLTMODE_param1],
                                                  command=self.conf_FLTMODE63)
                self.FLTMODE6.grid(row=7, column=1, padx=20, pady=(1, 1))
            else:
                self.FLTMODE6 = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                       values=[FLT_val, "RTL", "LAND"],
                                                       command=self.conf_FLTMODE63)
                self.FLTMODE6.grid(row=7, column=1, padx=20, pady=(1, 1))
            self.param_Modo_conexion = ctk.CTkLabel(self.conf_param_Frame, text="Modo conexión",
                                                            font=ctk.CTkFont(size=20, weight="bold"))
            self.param_Modo_conexion.grid(row=8, column=0, padx=20, pady=(20, 10))
            if replica:
                self.Modo_conexion = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                       values=[self.modo_con_param1],
                                                       command=self.modo_conexion3)
                self.Modo_conexion.grid(row=8, column=1, padx=20, pady=(1, 1))
            else:
                self.Modo_conexion = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                      values=["", "Global", "Directa"],
                                                      command=self.modo_conexion3)
                self.Modo_conexion.grid(row=8, column=1, padx=20, pady=(1, 1))

            param3_conf = True

            self.aceptar_param_3 = ctk.CTkButton(self.conf_param_Frame, text='Aceptar',
                                                 command=self.aceptar_param_3_clicked)
            self.aceptar_param_3.grid(row=9, column=0, columnspan=3, padx=20, pady=(1, 1))

    def conf_param4_clicked(self):

        global geofence
        global param4_conf
        global replica
        global FENCE_ALT_MAXget4
        global FENCE_ENABLEget4
        global margen_geofget4
        global geof_actionget4
        global RTL_ALTget4
        global PILOT_SPEED_UPget4
        global FLTMODE6get4
        if not geofence:

            messagebox.showinfo("Alert", "No se ha configurado Geofence")

        if not d4connected:
            messagebox.showinfo("Alert", "No se ha conectado el dron 4")

        else:

            self.client.publish("miMain/autopilotService4/getParameters")

            time.sleep(3)

            self.conf_param = ctk.CTkToplevel(self.ConnectionFrame)
            self.conf_param.title("Configuración parámetros dron 4")
            self.conf_param.geometry("1000x600")
            self.conf_param.grab_set()

            self.conf_param_Frame = ctk.CTkFrame(self.conf_param)
            self.conf_param_Frame.pack(fill="both", expand="yes", padx=10, pady=10)
            self.conf_param_Frame.rowconfigure(0, weight=1)
            self.conf_param_Frame.rowconfigure(1, weight=1)
            self.conf_param_Frame.rowconfigure(2, weight=1)
            self.conf_param_Frame.rowconfigure(3, weight=1)
            self.conf_param_Frame.rowconfigure(4, weight=1)
            self.conf_param_Frame.rowconfigure(5, weight=1)
            self.conf_param_Frame.rowconfigure(6, weight=1)
            self.conf_param_Frame.rowconfigure(7, weight=1)
            self.conf_param_Frame.rowconfigure(8, weight=1)
            self.conf_param_Frame.rowconfigure(9, weight=1)

            self.conf_param_Frame.columnconfigure(0, weight=1)
            self.conf_param_Frame.columnconfigure(1, weight=1)
            self.conf_param_Frame.columnconfigure(2, weight=1)


            self.param_geofence_PILOT_SPEED_UP = ctk.CTkLabel(self.conf_param_Frame, text="PILOT_SPEED_UP (cm/s)",
                                                              font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_PILOT_SPEED_UP.grid(row=0, column=0, padx=20, pady=(20, 10))
            self.PILOT_SPEED_UP4 = PILOT_SPEED_UPget4

            self.slider_PILOT_SPEED_UP = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=200, number_of_steps=4,
                                               command=self.sliding_PILOT_SPEED_UP4)
            self.slider_PILOT_SPEED_UP.grid(row=0, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
            if replica:
                self.PILOT_SPEED_UP4 = self.PILOT_SPEED_UP1
                self.slider_PILOT_SPEED_UP.set(float(self.PILOT_SPEED_UP1))
                self.PILOT_SPEED_UP_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(round(self.PILOT_SPEED_UP1, 0)))
                self.PILOT_SPEED_UP_valor.grid(row=0, column=2, padx=10, pady=10)
            else:
                self.slider_PILOT_SPEED_UP.set(PILOT_SPEED_UPget4)
                self.PILOT_SPEED_UP_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(PILOT_SPEED_UPget4))
                self.PILOT_SPEED_UP_valor.grid(row=0, column=2, padx=10, pady=10)

            self.param_geofence_RTL_ALT = ctk.CTkLabel(self.conf_param_Frame, text="RTL_ALT (m)",
                                                              font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_RTL_ALT.grid(row=1, column=0, padx=20, pady=(20, 10))
            self.RTL_ALT_valor4 = RTL_ALTget4

            if replica:
                self.RTL_ALT_valor4 = self.RTL_ALT_valor1
                self.RTL_ALT = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                 values=[str(self.RTL_ALT_valor1)],
                                                 command=self.conf_RTL_ALT4)
                self.RTL_ALT.grid(row=1, column=1, padx=20, pady=(1, 1))
            else:
                self.RTL_ALT = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                 values=[str(RTL_ALTget4), "4", "7", "11"],
                                                 command=self.conf_RTL_ALT4)
                self.RTL_ALT.grid(row=1, column=1, padx=20, pady=(1, 1))

            self.param_geofence_FENCE_ENABLE = ctk.CTkLabel(self.conf_param_Frame, text="FENCE_ENABLE",
                                                       font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_FENCE_ENABLE.grid(row=2, column=0, padx=20, pady=(20, 10))
            self.FENCE_ENABLE_valor4 = FENCE_ENABLEget4
            if FENCE_ENABLEget4 == 1:
                fen_val = "Yes"

            if FENCE_ENABLEget4 == 0:
                fen_val = "No"
            if replica:
                self.FENCE_ENABLE_valor4 = self.FENCE_ENABLE_valor1
                self.FENCE_ENABLE = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                      values=[self.fence_enable_param1],
                                                      command=self.conf_FENCE_ENABLE4)
                self.FENCE_ENABLE.grid(row=2, column=1, padx=20, pady=(1, 1))
            else:
                self.FENCE_ENABLE = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                 values=[fen_val, "Yes", "No"],
                                                 command=self.conf_FENCE_ENABLE4)
                self.FENCE_ENABLE.grid(row=2, column=1, padx=20, pady=(1, 1))

            self.param_geofence_margen = ctk.CTkLabel(self.conf_param_Frame, text="Margen del geofence (m)",
                                           font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_margen.grid(row=3, column=0, padx=20, pady=(20, 10))
            self.margen_geof4 = margen_geofget4
            if replica:
                self.margen_geof4 = self.margen_geof1
                self.slider_margen = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=5, number_of_steps=10,
                                                   command=self.sliding_margen4)
                self.slider_margen.grid(row=3, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
                self.slider_margen.set(float(self.margen_geof1))
                self.margen_geofence_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(round(self.margen_geof1, 1)))
                self.margen_geofence_valor.grid(row=3, column=2, padx=10, pady=10)

            else:
                self.slider_margen = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=5,number_of_steps=10,
                                                   command=self.sliding_margen4)
                self.slider_margen.grid(row=3, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
                self.slider_margen.set(margen_geofget4)
                self.margen_geofence_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(margen_geofget4))
                self.margen_geofence_valor.grid(row=3, column=2, padx=10, pady=10)

            self.param_geofence_action = ctk.CTkLabel(self.conf_param_Frame, text="Acción del geofence",
                                                      font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_action.grid(row=4, column=0, padx=20, pady=(20, 10))
            self.geof_action4 = geof_actionget4
            if geof_actionget1 == 1:
                gact_val = "RTL or Land"
            if geof_actionget1 == 2:
                gact_val = "Always Land"
            if geof_actionget1 == 4:
                gact_val = "Brake or Land"
            if replica:
                self.geof_action4 = self.geof_action1
                self.geofence_action = ctk.CTkOptionMenu(self.conf_param_Frame, values=[self.geof_action_param1],
                                                         command=self.conf_geof_action4)
                self.geofence_action.grid(row=4, column=1, padx=20, pady=(1, 1))
            else:
                self.geofence_action = ctk.CTkOptionMenu(self.conf_param_Frame, values=[gact_val, "RTL or Land",
                                                                                        "Always Land", "Brake or Land"],
                                                                               command=self.conf_geof_action4)
                self.geofence_action.grid(row=4, column=1, padx=20, pady=(1, 1))
            self.altura_takeoff_label = ctk.CTkLabel(self.conf_param_Frame, text="Altura Take Off (m)",
                                                      font=ctk.CTkFont(size=20, weight="bold"))
            self.altura_takeoff_label.grid(row=5, column=0, padx=20, pady=(20, 10))
            if replica:
                self.slider_altura_takeoff = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=10, number_of_steps=10,
                                                           command=self.sliding_altura4)
                self.slider_altura_takeoff.grid(row=5, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
                self.slider_altura_takeoff.set(float(altura_drone1))
                self.altura_takeoff_valor = ctk.CTkLabel(self.conf_param_Frame, text=str(round(altura_drone1, 0)))
                self.altura_takeoff_valor.grid(row=5, column=2, padx=10, pady=10)

            else:
                self.slider_altura_takeoff = ctk.CTkSlider(self.conf_param_Frame, from_=0, to=10, number_of_steps=10,
                                                   command=self.sliding_altura4)
                self.slider_altura_takeoff.grid(row=5, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")
                self.slider_altura_takeoff.set(5)
                self.altura_takeoff_valor = ctk.CTkLabel(self.conf_param_Frame, text="5")
                self.altura_takeoff_valor.grid(row=5, column=2, padx=10, pady=10)

            self.param_geofence_FENCE_ALT_MAX = ctk.CTkLabel(self.conf_param_Frame, text="FENCE_ALT_MAX (m)",
                                                       font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_FENCE_ALT_MAX.grid(row=6, column=0, padx=20, pady=(20, 10))
            self.FENCE_ALT_MAX_valor4 = FENCE_ALT_MAXget4
            if replica:
                self.FENCE_ALT_MAX_valor4 = self.FENCE_ALT_MAX_valor1
                self.FENCE_ALT_MAX = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                       values=[str(self.FENCE_ALT_MAX_valor1)],
                                                       command=self.conf_FENCE_ALT_MAX4)
                self.FENCE_ALT_MAX.grid(row=6, column=1, padx=20, pady=(1, 1))
            else:
                self.FENCE_ALT_MAX = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                 values=[str(FENCE_ALT_MAXget4), "5", "8", "12"],
                                                 command=self.conf_FENCE_ALT_MAX4)
                self.FENCE_ALT_MAX.grid(row=6, column=1, padx=20, pady=(1, 1))

            self.param_geofence_FLTMODE6 = ctk.CTkLabel(self.conf_param_Frame, text="FLTMODE6",
                                                             font=ctk.CTkFont(size=20, weight="bold"))
            self.param_geofence_FLTMODE6.grid(row=7, column=0, padx=20, pady=(20, 10))
            self.FLTMODE6_valor4 = FLTMODE6get4
            if FLTMODE6get4 == 6:
                FLT_val = "RTL"

            if FLTMODE6get4 == 9:
                FLT_val = "LAND"
            if replica:
                self.FLTMODE6_valor4 = self.FLTMODE6_valor1
                self.FLTMODE6 = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                  values=[self.FLTMODE_param1],
                                                  command=self.conf_FLTMODE64)
                self.FLTMODE6.grid(row=7, column=1, padx=20, pady=(1, 1))
            else:
                self.FLTMODE6 = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                       values=[FLT_val, "RTL", "LAND"],
                                                       command=self.conf_FLTMODE64)
                self.FLTMODE6.grid(row=7, column=1, padx=20, pady=(1, 1))
            self.param_Modo_conexion = ctk.CTkLabel(self.conf_param_Frame, text="Modo conexión",
                                                            font=ctk.CTkFont(size=20, weight="bold"))
            self.param_Modo_conexion.grid(row=8, column=0, padx=20, pady=(20, 10))
            if replica:
                self.Modo_conexion = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                       values=[self.modo_con_param1],
                                                       command=self.modo_conexion4)
                self.Modo_conexion.grid(row=8, column=1, padx=20, pady=(1, 1))
            else:
                self.Modo_conexion = ctk.CTkOptionMenu(self.conf_param_Frame,
                                                      values=["", "Global", "Directa"],
                                                      command=self.modo_conexion4)
                self.Modo_conexion.grid(row=8, column=1, padx=20, pady=(1, 1))

            param4_conf = True

            self.aceptar_param_4 = ctk.CTkButton(self.conf_param_Frame, text='Aceptar',
                                                 command=self.aceptar_param_4_clicked)
            self.aceptar_param_4.grid(row=9, column=0, columnspan=3, padx=20, pady=(1, 1))

    def aceptar_param_1_clicked(self):
        self.geofenceDesignObject.set_Geofence("d1", Ndrones, self.margen_geof1, self.geof_action1,
                                               self.PILOT_SPEED_UP1, self.RTL_ALT_valor1,
                                               self.FENCE_ENABLE_valor1, self.FENCE_ALT_MAX_valor1,
                                               self.FLTMODE6_valor1)
        self.conf_param.destroy()

    def aceptar_param_2_clicked(self):
        self.geofenceDesignObject.set_Geofence("d2", Ndrones, self.margen_geof2, self.geof_action2,
                                               self.PILOT_SPEED_UP2, self.RTL_ALT_valor2,
                                               self.FENCE_ENABLE_valor2, self.FENCE_ALT_MAX_valor2,
                                               self.FLTMODE6_valor2)
        self.conf_param.destroy()

    def aceptar_param_3_clicked(self):
        self.geofenceDesignObject.set_Geofence("d3", Ndrones, self.margen_geof3, self.geof_action3,
                                               self.PILOT_SPEED_UP3, self.RTL_ALT_valor3,
                                               self.FENCE_ENABLE_valor3, self.FENCE_ALT_MAX_valor3,
                                               self.FLTMODE6_valor3)
        self.conf_param.destroy()

    def aceptar_param_4_clicked(self):
        self.geofenceDesignObject.set_Geofence("d4", Ndrones, self.margen_geof4, self.geof_action4,
                                               self.PILOT_SPEED_UP4, self.RTL_ALT_valor4,
                                               self.FENCE_ENABLE_valor4, self.FENCE_ALT_MAX_valor4,
                                               self.FLTMODE6_valor4)
        self.conf_param.destroy()



    def sliding_PILOT_SPEED_UP1(self, PILOT_SPEED_UP):

        self.PILOT_SPEED_UP1 = PILOT_SPEED_UP
        self.PILOT_SPEED_UP_valor.configure(text=str(round(self.PILOT_SPEED_UP1,0)))

    def sliding_PILOT_SPEED_UP2(self, PILOT_SPEED_UP):


        self.PILOT_SPEED_UP2 = PILOT_SPEED_UP
        self.PILOT_SPEED_UP_valor.configure(text=str(round(self.PILOT_SPEED_UP2,0)))

    def sliding_PILOT_SPEED_UP3(self, PILOT_SPEED_UP):

        self.PILOT_SPEED_UP3 = PILOT_SPEED_UP
        self.PILOT_SPEED_UP_valor.configure(text=str(round(self.PILOT_SPEED_UP3,0)))

    def sliding_PILOT_SPEED_UP4(self, PILOT_SPEED_UP):
        self.PILOT_SPEED_UP4 = PILOT_SPEED_UP
        self.PILOT_SPEED_UP_valor.configure(text=str(round(self.PILOT_SPEED_UP4,0)))

    def conf_RTL_ALT1(self, RTL_ALT: str):
        if RTL_ALT == "4":
            self.RTL_ALT_valor1 = 4

        if RTL_ALT == "7":
            self.RTL_ALT_valor1 = 7

        if RTL_ALT == "11":
            self.RTL_ALT_valor1 = 11

    def conf_RTL_ALT2(self, RTL_ALT: str):
        if RTL_ALT == "4":
            self.RTL_ALT_valor2 = 4

        if RTL_ALT == "7":
            self.RTL_ALT_valor2 = 7

        if RTL_ALT == "11":
            self.RTL_ALT_valor2 = 11

    def conf_RTL_ALT3(self, RTL_ALT: str):
        if RTL_ALT == "4":
            self.RTL_ALT_valor3 = 4

        if RTL_ALT == "7":
            self.RTL_ALT_valor3 = 7

        if RTL_ALT == "11":
            self.RTL_ALT_valor3 = 11

    def conf_RTL_ALT4(self, RTL_ALT: str):
        if RTL_ALT == "4":
            self.RTL_ALT_valor4 = 4

        if RTL_ALT == "7":
            self.RTL_ALT_valor4 = 7

        if RTL_ALT == "11":
            self.RTL_ALT_valor4 = 11

    def conf_FENCE_ENABLE1(self, FENCE_ENABLE:str):
        self.fence_enable_param1 = FENCE_ENABLE
        if self.fence_enable_param1 == "No":
            self.FENCE_ENABLE_valor1 = 0


        if self.fence_enable_param1 == "Yes":
            self.FENCE_ENABLE_valor1 = 1

    def conf_FENCE_ENABLE2(self, FENCE_ENABLE:str):
        if FENCE_ENABLE == "No":
            self.FENCE_ENABLE_valor2 = 0


        if FENCE_ENABLE == "Yes":
            self.FENCE_ENABLE_valor2 = 1

    def conf_FENCE_ENABLE3(self, FENCE_ENABLE:str):
        if FENCE_ENABLE == "No":
            self.FENCE_ENABLE_valor3 = 0


        if FENCE_ENABLE == "Yes":
            self.FENCE_ENABLE_valor3 = 1

    def conf_FENCE_ENABLE4(self, FENCE_ENABLE:str):
        if FENCE_ENABLE == "No":
            self.FENCE_ENABLE_valor4 = 0


        if FENCE_ENABLE == "Yes":
            self.FENCE_ENABLE_valor4 = 1


    def sliding_margen1(self, margen_geof):
        self.margen_geof1 = margen_geof
        self.margen_geofence_valor.configure(text=str(round(self.margen_geof1,1)))

    def sliding_margen2(self, margen_geof):
        self.margen_geof2 = margen_geof
        self.margen_geofence_valor.configure(text=str(round(self.margen_geof2,1)))

    def sliding_margen3(self, margen_geof):
        self.margen_geof3 = margen_geof
        self.margen_geofence_valor.configure(text=str(round(self.margen_geof3,1)))

    def sliding_margen4(self, margen_geof):
        self.margen_geof4 = margen_geof
        self.margen_geofence_valor.configure(text=str(round(self.margen_geof4,1)))

    def sliding_altura1(self, altura):
        global altura_drone1
        altura_drone1 = altura
        self.altura_takeoff_valor.configure(text=str(round(altura_drone1,0)))

    def sliding_altura2(self, altura):
        global altura_drone2
        altura_drone2 = altura
        self.altura_takeoff_valor.configure(text=str(round(altura_drone2,0)))

    def sliding_altura3(self, altura):
        global altura_drone3
        altura_drone3 = altura
        self.altura_takeoff_valor.configure(text=str(round(altura_drone3,0)))

    def sliding_altura4(self, altura):
        global altura_drone4
        altura_drone4 = altura
        self.altura_takeoff_valor.configure(text=str(round(altura_drone4,0)))

    def cargarAltura(self):
        global replica
        global Ndrones
        self.altura_return1 = altura_drone1

        if Ndrones == "1":
            if replica:
                self.altura_return2 = altura_drone1
                self.altura_return3 = altura_drone1
                self.altura_return4 = altura_drone1
            else:
                self.altura_return2 = altura_drone1
                self.altura_return3 = altura_drone1
                self.altura_return4 = altura_drone1

        if Ndrones == "2":
            if replica:
                self.altura_return2 = altura_drone1
                self.altura_return3 = altura_drone1
                self.altura_return4 = altura_drone1
            else:
                self.altura_return2 = altura_drone2
                self.altura_return3 = altura_drone1
                self.altura_return4 = altura_drone1

        if Ndrones == "3":
            if replica:
                self.altura_return2 = altura_drone1
                self.altura_return3 = altura_drone1
                self.altura_return4 = altura_drone1
            else:
                self.altura_return2 = altura_drone2
                self.altura_return3 = altura_drone3
                self.altura_return4 = altura_drone1

        if Ndrones == "4":
            if replica:
                self.altura_return2 = altura_drone1
                self.altura_return3 = altura_drone1
                self.altura_return4 = altura_drone1
            else:
                self.altura_return2 = altura_drone2
                self.altura_return3 = altura_drone3
                self.altura_return4 = altura_drone4

        return str(self.altura_return1), str(self.altura_return2), str(self.altura_return3), str(self.altura_return4)


    def conf_geof_action1(self, geof_action: str):

        self.geof_action_param1 = geof_action
        if geof_action == "RTL or Land":
            self.geof_action1 = 1

        if geof_action == "Always Land":
            self.geof_action1 = 2

        if geof_action == "Brake or Land":
            self.geof_action1 = 4

    def conf_geof_action2(self, geof_action: str):

        if geof_action == "RTL or Land":
            self.geof_action2 = 1

        if geof_action == "Always Land":
            self.geof_action2 = 2

        if geof_action == "Brake or Land":
            self.geof_action2 = 4

    def conf_geof_action3(self, geof_action: str):

        if geof_action == "RTL or Land":
            self.geof_action3 = 1

        if geof_action == "Always Land":
            self.geof_action3 = 2

        if geof_action == "Brake or Land":
            self.geof_action3 = 4

    def conf_geof_action4(self, geof_action: str):

        if geof_action == "RTL or Land":
            self.geof_action4 = 1

        if geof_action == "Always Land":
            self.geof_action4 = 2

        if geof_action == "Brake or Land":
            self.geof_action4 = 4

    def conf_FENCE_ALT_MAX1(self, FENCE_ALT_MAX: str):
        if FENCE_ALT_MAX == "5":
            self.FENCE_ALT_MAX_valor1 = 5

        if FENCE_ALT_MAX == "8":
            self.FENCE_ALT_MAX_valor1 = 8

        if FENCE_ALT_MAX == "12":
            self.FENCE_ALT_MAX_valor1 = 12

    def conf_FENCE_ALT_MAX2(self, FENCE_ALT_MAX: str):
        if FENCE_ALT_MAX == "5":
            self.FENCE_ALT_MAX_valor2 = 5

        if FENCE_ALT_MAX == "8":
            self.FENCE_ALT_MAX_valor2 = 8

        if FENCE_ALT_MAX == "12":
            self.FENCE_ALT_MAX_valor2 = 12

    def conf_FENCE_ALT_MAX3(self, FENCE_ALT_MAX: str):
        if FENCE_ALT_MAX == "5":
            self.FENCE_ALT_MAX_valor3 = 5

        if FENCE_ALT_MAX == "8":
            self.FENCE_ALT_MAX_valor3 = 8

        if FENCE_ALT_MAX == "12":
            self.FENCE_ALT_MAX_valor3 = 12

    def conf_FENCE_ALT_MAX4(self, FENCE_ALT_MAX: str):
        if FENCE_ALT_MAX == "5":
            self.FENCE_ALT_MAX_valor4 = 5

        if FENCE_ALT_MAX == "8":
            self.FENCE_ALT_MAX_valor4 = 8

        if FENCE_ALT_MAX == "12":
            self.FENCE_ALT_MAX_valor4 = 12

    def conf_FLTMODE61(self, FLTMODE6: str):
        self.FLTMODE_param1 = FLTMODE6
        if FLTMODE6 == "RTL":
            self.FLTMODE6_valor1 = 6

        if FLTMODE6 == "LAND":
            self.FLTMODE6_valor1 = 9

    def conf_FLTMODE62(self, FLTMODE6: str):
        if FLTMODE6 == "RTL":
            self.FLTMODE6_valor2 = 6

        if FLTMODE6 == "LAND":
            self.FLTMODE6_valor2 = 9

    def conf_FLTMODE63(self, FLTMODE6: str):
        if FLTMODE6 == "RTL":
            self.FLTMODE6_valor3 = 6

        if FLTMODE6 == "LAND":
            self.FLTMODE6_valor3 = 9

    def conf_FLTMODE64(self, FLTMODE6: str):
        if FLTMODE6 == "RTL":
            self.FLTMODE6_valor4 = 6

        if FLTMODE6 == "LAND":
            self.FLTMODE6_valor4 = 9

    def modo_conexion1(self, modo_conexion:str):
        self.modo_con_param1 = modo_conexion
        if modo_conexion == "Global":
            print ("modo conexion global")
        if modo_conexion == "Directa":
            print ("modo conexion directa")

    def modo_conexion2(self, modo_conexion:str):
        if modo_conexion == "Global":
            print ("modo conexion global")
        if modo_conexion == "Directa":
            print ("modo conexion directa")

    def modo_conexion3(self, modo_conexion:str):
        if modo_conexion == "Global":
            print ("modo conexion global")
        if modo_conexion == "Directa":
            print ("modo conexion directa")

    def modo_conexion4(self, modo_conexion:str):
        if modo_conexion == "Global":
            print ("modo conexion global")
        if modo_conexion == "Directa":
            print ("modo conexion directa")

    def conf_param_replica(self, replica_value:str):
        global replica
        if replica_value == "Si":
            replica = True

        if replica_value == "No":
            replica = False


    def Button1Clicked (self):

        global geofence
        global param1_conf
        global Ndrones
        if not geofence:

            messagebox.showinfo("Alert", "No se ha configurado Geofence")

        else:
            global d1connected
            if not d1connected:

                self.Button1.configure(self, fg_color="yellow")
                messagebox.showinfo("Information", "Conectando a Drone 1")
                self.client.publish("miMain/autopilotService/connect")




            else:

                self.Button1.configure(self, fg_color="red")
                d1connected = False
                messagebox.showinfo("Information", "Drone 1 desconectado")
                self.client.publish("miMain/autopilotService/disconnect")

    def Button2Clicked (self):

        global geofence
        global param2_conf
        global Ndrones
        if not geofence:

            messagebox.showinfo("Alert", "No se ha configurado Geofence")

        else:
            global d2connected
            if not d2connected:

                self.Button2.configure(self, fg_color="yellow")
                messagebox.showinfo("Information", "Conectando a Drone 2")
                self.client.publish("miMain/autopilotService2/connect")



            else:

                self.Button2.configure(self, fg_color="red")
                d2connected = False
                messagebox.showinfo("Information", "Drone 2 desconectado")
                self.client.publish("miMain/autopilotService2/disconnect")

    def Button3Clicked (self):

        global geofence
        global param3_conf
        global Ndrones
        if not geofence:

            messagebox.showinfo("Alert", "No se ha configurado Geofence")

        else:
            global d3connected
            if not d3connected:

                self.Button3.configure(self, fg_color="yellow")
                messagebox.showinfo("Information", "Conectando a Drone 3")
                self.client.publish("miMain/autopilotService3/connect")




            else:

                self.Button3.configure(self, fg_color="red")
                d3connected = False
                messagebox.showinfo("Information", "Drone 3 desconectado")
                self.client.publish("miMain/autopilotService3/disconnect")

    def Button4Clicked (self):

        global geofence
        global param4_conf
        global Ndrones
        if not geofence:

            messagebox.showinfo("Alert", "No se ha configurado Geofence")

        else:
            global d4connected
            if not d4connected:

                self.Button4.configure(self, fg_color="yellow")
                messagebox.showinfo("Information", "Conectando a Drone 4")
                self.client.publish("miMain/autopilotService4/connect")


            else:

                self.Button4.configure(self, fg_color="red")
                d4connected = False
                messagebox.showinfo("Information", "Drone 4 desconectado")
                self.client.publish("miMain/autopilotService4/disconnect")


