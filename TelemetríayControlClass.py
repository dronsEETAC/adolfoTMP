from tkinter import messagebox

import customtkinter as ctk
from functools import partial
import paho.mqtt.client as mqtt
import json
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative

d1buttonClicked = False
d2buttonClicked = False
d3buttonClicked = False
d4buttonClicked = False
d1Toff_LandButtonClicked = False
d2Toff_LandButtonClicked = False
d3Toff_LandButtonClicked = False
d4Toff_LandButtonClicked = False
d1Arm_Disarm_ButtonClicked = False
d2Arm_Disarm_ButtonClicked = False
d3Arm_Disarm_ButtonClicked = False
d4Arm_Disarm_ButtonClicked = False
parameterFrame1Creado = False
parameterFrame2Creado = False
parameterFrame3Creado = False
parameterFrame4Creado = False


class TelemetríayControlClass:



    def BuildFrame(self, fatherFrame,BorrarRastro,client, altura1, altura2, altura3, altura4):

        # self.creado = False
        self.BorrarRastro = BorrarRastro

        self.client = client
        self.altura_toff1 = altura1
        self.altura_toff2 = altura2
        self.altura_toff3 = altura3
        self.altura_toff4 = altura4

        self.TCFrame = ctk.CTkFrame(fatherFrame)
        self.TCFrame.rowconfigure(0, weight=1)
        self.TCFrame.columnconfigure(0, weight=1)
        self.TCFrame.columnconfigure(1, weight=1)

        self.TelemetriaFrame =ctk.CTkFrame(self.TCFrame)

        self.TelemetriaFrame.grid(row=0, column=0, padx=0, pady=0, sticky="nesw")
        #self.TelemetriaFrame.rowconfigure(0, weight=1)
        #self.TelemetriaFrame.rowconfigure(1, weight=1)
        self.telemetria_label = ctk.CTkLabel(self.TelemetriaFrame, text="Datos Telemetría",
                                        font=ctk.CTkFont(size=20, weight="bold"))
        self.telemetria_label.grid(row=0, column=0, padx=10, pady=10)

        self.droneselectionframe = ctk.CTkFrame(self.TelemetriaFrame)
        self.droneselectionframe.grid(row=1, column=0, padx=1, pady=1)
        # self.droneselectionframe.columnconfigure(0, weight=1)
        # self.droneselectionframe.columnconfigure(1, weight=1)
        # self.droneselectionframe.columnconfigure(2, weight=1)
        # self.droneselectionframe.columnconfigure(3, weight=1)
        self.d1button = ctk.CTkButton(self.droneselectionframe, width=10, height=10,  text="d1", text_color= "black", fg_color="lightcoral",
                                      command=self.d1buttonClicked)
                                      # command = partial(self.d1buttonClicked, self.vel, self.alt))
        self.d1button.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
        self.d2button = ctk.CTkButton(self.droneselectionframe, width=10, height=10, text="d2", text_color= "black", fg_color="turquoise",
                                     command=self.d2buttonClicked)
        self.d2button.grid(row=0, column=1, padx=10, pady=10, sticky="nesw")
        self.d3button = ctk.CTkButton(self.droneselectionframe, width=10, height=10,  text="d3", text_color= "black", fg_color="khaki",
                                     command=self.d3buttonClicked)
        self.d3button.grid(row=0, column=2, padx=10, pady=10, sticky="nesw")
        self.d4button = ctk.CTkButton(self.droneselectionframe, width=10, height=10,  text="d4", text_color= "black", fg_color="limegreen",
                                      command=self.d4buttonClicked)
        self.d4button.grid(row=0, column=3, padx=10, pady=10, sticky="nesw")





        self.dronesRTLframe = ctk.CTkFrame(self.TelemetriaFrame)
        self.dronesRTLframe.grid(row=3, column=0, padx=10, pady=1)
        self.d1RTLbutton = ctk.CTkButton(self.dronesRTLframe, width=10, height=10, text="d1RTL", text_color="black", fg_color="red",
                                         command=self.d1RTLbuttonClicked)
        self.d1RTLbutton.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
        self.d2RTLbutton = ctk.CTkButton(self.dronesRTLframe, width=10, height=10, text="d2RTL", text_color="black", fg_color="blue",
                                         command=self.d2RTLbuttonClicked)
        self.d2RTLbutton.grid(row=0, column=1, padx=10, pady=10, sticky="nesw")
        self.d3RTLbutton = ctk.CTkButton(self.dronesRTLframe, width=10, height=10, text="d3RTL", text_color="black", fg_color="yellow",
                                         command=self.d3RTLbuttonClicked)
        self.d3RTLbutton.grid(row=0, column=2, padx=10, pady=10, sticky="nesw")
        self.d4RTLbutton = ctk.CTkButton(self.dronesRTLframe, width=10, height=10, text="d4RTL", text_color="black", fg_color="green",
                                         command=self.d4RTLbuttonClicked)
        self.d4RTLbutton.grid(row=0, column=3, padx=10, pady=10, sticky="nesw")



        self.ControlFrame = ctk.CTkFrame(self.TCFrame)
        self.ControlFrame.grid(row=0, column=1, padx=0, pady=0, sticky="nesw")
        # self.ControlFrame.rowconfigure(0, weight=1)
        # self.ControlFrame.rowconfigure(1, weight=1)
        self.Ndirectionbutton = ctk.CTkButton(self.ControlFrame, text = 'N', width=60, height=60,
                                         command=self.NdirectionbuttonClicked)
        self.Ndirectionbutton.grid(row=5, column=5, padx=10, pady=10, sticky="nesw")
        self.Sdirectionbutton = ctk.CTkButton(self.ControlFrame, text = 'S', width=60, height=60,
                                              command=self.SdirectionbuttonClicked)
        self.Sdirectionbutton.grid(row=7, column=5, padx=10, pady=10, sticky="nesw")
        self.Edirectionbutton = ctk.CTkButton(self.ControlFrame, text = 'E', width=60, height=60,
                                              command=self.EdirectionbuttonClicked)
        self.Edirectionbutton.grid(row=6, column=6, padx=10, pady=10, sticky="nesw")
        self.Wdirectionbutton = ctk.CTkButton(self.ControlFrame, text = 'W', width=60, height=60,
                                              command=self.WdirectionbuttonClicked)
        self.Wdirectionbutton.grid(row=6, column=4, padx=10, pady=10, sticky="nesw")
        self.NEdirectionbutton = ctk.CTkButton(self.ControlFrame, text = 'NE', width=60, height=60,
                                              command=self.NEdirectionbuttonClicked)
        self.NEdirectionbutton.grid(row=5, column=6, padx=10, pady=10, sticky="nesw")
        self.NWdirectionbutton = ctk.CTkButton(self.ControlFrame, text = 'NW', width=60, height=60,
                                              command=self.NWdirectionbuttonClicked)
        self.NWdirectionbutton.grid(row=5, column=4, padx=10, pady=10, sticky="nesw")
        self.SEdirectionbutton = ctk.CTkButton(self.ControlFrame, text = 'SE', width=60, height=60,
                                              command=self.SEdirectionbuttonClicked)
        self.SEdirectionbutton.grid(row=7, column=6, padx=10, pady=10, sticky="nesw")
        self.SWdirectionbutton = ctk.CTkButton(self.ControlFrame, text = 'SW', width=60, height=60,
                                              command=self.SWdirectionbuttonClicked)
        self.SWdirectionbutton.grid(row=7, column=4, padx=10, pady=10, sticky="nesw")

        self.Arm_Disarm_Button = ctk.CTkButton(self.ControlFrame, text="ARM",  width=60, height=60,
                                             fg_color="grey", command=self.Arm_Disarm_ButtonClicked)
        self.Arm_Disarm_Button.grid(row=8, column=4, padx=10, pady=10, sticky="nesw")
        self.TOffButton = ctk.CTkButton(self.ControlFrame, text="TAKE OFF", width=60, height=60,
                                             fg_color="grey", command=self.TOffButtonClicked)
        self.TOffButton.grid(row=8, column=5, padx=10, pady=10, sticky="nesw")
        self.StopButton = ctk.CTkButton(self.ControlFrame, text="STOP", width=60, height=60,
                                             fg_color="grey", command=self.StopbuttonClicked)
        self.StopButton.grid(row=6, column=5, padx=10, pady=10, sticky="nesw")
        self.LandButton = ctk.CTkButton(self.ControlFrame, text="LAND", width=60, height=60,
                                             fg_color="grey", command=self.LandButtonClicked)
        self.LandButton.grid(row=8, column=6, padx=10, pady=10, sticky="nesw")


        return self.TCFrame





    def setTelemetryInfo (self, vel, alt, drone):
        global velocity
        global altitude
        global parameterFrame1Creado
        global parameterFrame2Creado
        global parameterFrame3Creado
        global parameterFrame4Creado
        # global d1buttonClicked
        velocity = vel
        altitude = alt


        if drone == "d1":

            if parameterFrame1Creado:
                # print("vel1", velocity)
                # print("alt1", altitude)
                self.velocityround = str(round(velocity,2))
                self.altituderound = str(round(altitude,2))
                self.textvel = "Velocidad = {} m/s \n\n".format(self.velocityround)
                self.textalt = "Altitud = {} m \n\n".format(self.altituderound)
                self.velocidadText1.delete("1.0", ctk.END)
                self.velocidadText1.insert("0.0", self.textvel + self.textalt)

        if drone == "d2":

            if parameterFrame2Creado:
                # print("vel2", velocity)
                # print("alt2", altitude)
                self.velocityround = str(round(velocity, 2))
                self.altituderound = str(round(altitude, 2))
                self.textvel = "Velocidad = {} m/s \n\n".format(self.velocityround)
                self.textalt = "Altitud = {} m \n\n".format(self.altituderound)
                self.velocidadText2.delete("1.0", ctk.END)
                self.velocidadText2.insert("0.0", self.textvel + self.textalt)

        if drone == "d3":

            if parameterFrame3Creado:
                # print("vel2", velocity)
                # print("alt2", altitude)
                self.velocityround = str(round(velocity, 2))
                self.altituderound = str(round(altitude, 2))
                self.textvel = "Velocidad = {} m/s \n\n".format(self.velocityround)
                self.textalt = "Altitud = {} m \n\n".format(self.altituderound)
                self.velocidadText3.delete("1.0", ctk.END)
                self.velocidadText3.insert("0.0", self.textvel + self.textalt)

        if drone == "d4":

            if parameterFrame4Creado:
                # print("vel2", velocity)
                # print("alt2", altitude)
                self.velocityround = str(round(velocity, 2))
                self.altituderound = str(round(altitude, 2))
                self.textvel = "Velocidad = {} m/s \n\n".format(self.velocityround)
                self.textalt = "Altitud = {} m \n\n".format(self.altituderound)
                self.velocidadText4.delete("1.0", ctk.END)
                self.velocidadText4.insert("0.0", self.textvel + self.textalt)


    def d1buttonClicked(self):


        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked
        global d1Toff_LandButtonClicked
        global d1Arm_Disarm_ButtonClicked
        global d2Toff_LandButtonClicked
        global d2Arm_Disarm_ButtonClicked
        global parameterFrame1Creado
        if not d1buttonClicked:


            self.d1button.configure(self, fg_color="red")
            self.d2button.configure(self, fg_color="turquoise")
            self.d3button.configure(self, fg_color="khaki")
            self.d4button.configure(self, fg_color="limegreen")
            d1buttonClicked = True
            d2buttonClicked = False
            d3buttonClicked = False
            d4buttonClicked = False
            parameterFrame1Creado = True


        else:

            self.d1button.configure(self, fg_color="lightcoral")
            d1buttonClicked = False


        self.parametersframe1 = ctk.CTkFrame(self.TelemetriaFrame)
        self.parametersframe1.grid(row=2, column=0, padx=1, pady=10)
        self.velocidadText1 = ctk.CTkTextbox(self.parametersframe1, width=250, height=140,
                                            font=ctk.CTkFont(size=20, weight="bold"))
        self.velocidadText1.grid(row=0, column=0)

    def d2buttonClicked(self):

        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked
        global d1Toff_LandButtonClicked
        global d1Arm_Disarm_ButtonClicked
        global d2Toff_LandButtonClicked
        global d2Arm_Disarm_ButtonClicked
        global parameterFrame2Creado
        if not d2buttonClicked:

            self.d2button.configure(self, fg_color="blue")
            self.d1button.configure(self, fg_color="lightcoral")
            self.d3button.configure(self, fg_color="khaki")
            self.d4button.configure(self, fg_color="limegreen")
            d1buttonClicked = False
            d2buttonClicked = True
            d3buttonClicked = False
            d4buttonClicked = False
            parameterFrame2Creado = True


        else:

            self.d2button.configure(self, fg_color="turquoise")
            d2buttonClicked = False

        self.parametersframe2 = ctk.CTkFrame(self.TelemetriaFrame)
        self.parametersframe2.grid(row=2, column=0, padx=1, pady=10)
        self.velocidadText2 = ctk.CTkTextbox(self.parametersframe2, width=250, height=140,
                                                 font=ctk.CTkFont(size=20, weight="bold"))
        self.velocidadText2.grid(row=0, column=0)

    def d3buttonClicked(self):

        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked
        global d1Toff_LandButtonClicked
        global d1Arm_Disarm_ButtonClicked
        global d2Toff_LandButtonClicked
        global d2Arm_Disarm_ButtonClicked
        global parameterFrame3Creado
        if not d3buttonClicked:

            self.d3button.configure(self, fg_color="yellow")
            self.d2button.configure(self, fg_color="turquoise")
            self.d1button.configure(self, fg_color="lightcoral")
            self.d4button.configure(self, fg_color="limegreen")
            d1buttonClicked = False
            d2buttonClicked = False
            d3buttonClicked = True
            d4buttonClicked = False
            parameterFrame3Creado = True

        else:

            self.d3button.configure(self, fg_color="khaki")
            d3buttonClicked = False

        self.parametersframe3 = ctk.CTkFrame(self.TelemetriaFrame)
        self.parametersframe3.grid(row=2, column=0, padx=1, pady=10)
        self.velocidadText3 = ctk.CTkTextbox(self.parametersframe3, width=250, height=140,
                                             font=ctk.CTkFont(size=20, weight="bold"))
        self.velocidadText3.grid(row=0, column=0)

    def d4buttonClicked(self):

        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked
        global d1Toff_LandButtonClicked
        global d1Arm_Disarm_ButtonClicked
        global d2Toff_LandButtonClicked
        global d2Arm_Disarm_ButtonClicked
        global parameterFrame4Creado
        if not d4buttonClicked:

            self.d4button.configure(self, fg_color="green")
            self.d2button.configure(self, fg_color="turquoise")
            self.d3button.configure(self, fg_color="khaki")
            self.d1button.configure(self, fg_color="lightcoral")
            d1buttonClicked = False
            d2buttonClicked = False
            d3buttonClicked = False
            d4buttonClicked = True
            parameterFrame4Creado = True


        else:

            self.d4button.configure(self, fg_color="limegreen")
            d4buttonClicked = False

        self.parametersframe4 = ctk.CTkFrame(self.TelemetriaFrame)
        self.parametersframe4.grid(row=2, column=0, padx=1, pady=10)
        self.velocidadText4 = ctk.CTkTextbox(self.parametersframe4, width=250, height=140,
                                             font=ctk.CTkFont(size=20, weight="bold"))
        self.velocidadText4.grid(row=0, column=0)



    def TOffButtonClicked(self):

        global Toff_LandButtonClicked
        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked
        global d1Toff_LandButtonClicked
        global d2Toff_LandButtonClicked
        global d3Toff_LandButtonClicked
        global d4Toff_LandButtonClicked
        if d1buttonClicked:

            # if not d1Toff_LandButtonClicked:
                # self.TOff_LandButton.configure(self, text='LAND', fg_color="green")
            self.client.publish("miMain/autopilotService/takeOff", payload=self.altura_toff1)
                # d1Toff_LandButtonClicked = True

            # else:
            #
            #     # self.TOff_LandButton.configure(self, text = 'TAKE OFF', fg_color="grey")
            #     self.client.publish("miMain/autopilotService/land")
            #     d1Toff_LandButtonClicked = False

        if d2buttonClicked:

            # if not d2Toff_LandButtonClicked:
                # self.TOff_LandButton.configure(self, text='LAND', fg_color="green")
            self.client.publish("miMain/autopilotService2/takeOff", payload=self.altura_toff2)
                # d2Toff_LandButtonClicked = True

            # else:
            #
            #     # self.TOff_LandButton.configure(self, text='TAKE OFF', fg_color="grey")
            #     self.client.publish("miMain/autopilotService2/land")
            #     d2Toff_LandButtonClicked = False

        if d3buttonClicked:

            # if not d3Toff_LandButtonClicked:
                # self.TOff_LandButton.configure(self, text='LAND', fg_color="green")
            self.client.publish("miMain/autopilotService3/takeOff", payload=self.altura_toff3)
                # d3Toff_LandButtonClicked = True

            # else:
            #
            #     # self.TOff_LandButton.configure(self, text='TAKE OFF', fg_color="grey")
            #     self.client.publish("miMain/autopilotService3/land")
            #     d3Toff_LandButtonClicked = False

        if d4buttonClicked:

            # if not d4Toff_LandButtonClicked:
                # self.TOff_LandButton.configure(self, text='LAND', fg_color="green")
            self.client.publish("miMain/autopilotService4/takeOff", payload=self.altura_toff4)
                # d4Toff_LandButtonClicked = True

            # else:
            #
            #     # self.TOff_LandButton.configure(self, text='TAKE OFF', fg_color="grey")
            #     self.client.publish("miMain/autopilotService4/land")
            #     d4Toff_LandButtonClicked = False

    def LandButtonClicked(self):
        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked

        if d1buttonClicked:

            self.client.publish("miMain/autopilotService/land")


        if d2buttonClicked:

            self.client.publish("miMain/autopilotService2/land")


        if d3buttonClicked:

            self.client.publish("miMain/autopilotService3/land")


        if d4buttonClicked:

            self.client.publish("miMain/autopilotService4/land")



    def Arm_Disarm_ButtonClicked(self):
        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked
        global d1Arm_Disarm_ButtonClicked
        global d2Arm_Disarm_ButtonClicked
        global d3Arm_Disarm_ButtonClicked
        global d4Arm_Disarm_ButtonClicked

        if d1buttonClicked:
            # if not d1Arm_Disarm_ButtonClicked:

                # self.Arm_Disarm_Button.configure(self, text = 'DISARM', fg_color="green")
            self.client.publish("miMain/autopilotService/armDrone")
                # d1Arm_Disarm_ButtonClicked = True


            # else:
            #
            #     # self.Arm_Disarm_Button.configure(self, text = 'ARM', fg_color="grey")
            #     self.client.publish("miMain/autopilotService/disarmDrone")
            #     d1Arm_Disarm_ButtonClicked = False

        if d2buttonClicked:
            # if not d2Arm_Disarm_ButtonClicked:

                # self.Arm_Disarm_Button.configure(self, text='DISARM', fg_color="green")
            self.client.publish("miMain/autopilotService2/armDrone")
                # d2Arm_Disarm_ButtonClicked = True


            # else:
            #
            #     # self.Arm_Disarm_Button.configure(self, text='ARM', fg_color="grey")
            #     self.client.publish("miMain/autopilotService2/disarmDrone")
            #     d2Arm_Disarm_ButtonClicked = False

        if d3buttonClicked:
            # if not d3Arm_Disarm_ButtonClicked:

                # self.Arm_Disarm_Button.configure(self, text='DISARM', fg_color="green")
            self.client.publish("miMain/autopilotService3/armDrone")
                # d3Arm_Disarm_ButtonClicked = True


            # else:
            #
            #     # self.Arm_Disarm_Button.configure(self, text='ARM', fg_color="grey")
            #     self.client.publish("miMain/autopilotService3/disarmDrone")
            #     d3Arm_Disarm_ButtonClicked = False

        if d4buttonClicked:
            # if not d4Arm_Disarm_ButtonClicked:

                # self.Arm_Disarm_Button.configure(self, text='DISARM', fg_color="green")
            self.client.publish("miMain/autopilotService4/armDrone")
                # d4Arm_Disarm_ButtonClicked = True


            # else:
            #
            #     # self.Arm_Disarm_Button.configure(self, text='ARM', fg_color="grey")
            #     self.client.publish("miMain/autopilotService4/disarmDrone")
            #     d4Arm_Disarm_ButtonClicked = False

    def d1RTLbuttonClicked(self):

        self.client.publish("miMain/autopilotService/returnToLaunch")
    def d2RTLbuttonClicked(self):
        self.client.publish("miMain/autopilotService2/returnToLaunch")
    def d3RTLbuttonClicked(self):
        self.client.publish("miMain/autopilotService3/returnToLaunch")
    def d4RTLbuttonClicked(self):
        self.client.publish("miMain/autopilotService4/returnToLaunch")

    def NdirectionbuttonClicked(self):
        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked
        if d1buttonClicked:
            self.client.publish("miMain/autopilotService/go", payload = 'North')
        if d2buttonClicked:
            self.client.publish("miMain/autopilotService2/go", payload='North')
        if d3buttonClicked:
            self.client.publish("miMain/autopilotService3/go", payload='North')
        if d4buttonClicked:
            self.client.publish("miMain/autopilotService4/go", payload='North')


    def SdirectionbuttonClicked(self):
        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked
        if d1buttonClicked:
            self.client.publish("miMain/autopilotService/go", payload = 'South')
        if d2buttonClicked:
            self.client.publish("miMain/autopilotService2/go", payload='South')
        if d3buttonClicked:
            self.client.publish("miMain/autopilotService3/go", payload='South')
        if d4buttonClicked:
            self.client.publish("miMain/autopilotService4/go", payload='South')


    def EdirectionbuttonClicked(self):
        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked
        if d1buttonClicked:
            self.client.publish("miMain/autopilotService/go", payload = 'East')
        if d2buttonClicked:
            self.client.publish("miMain/autopilotService2/go", payload='East')
        if d3buttonClicked:
            self.client.publish("miMain/autopilotService3/go", payload='East')
        if d4buttonClicked:
            self.client.publish("miMain/autopilotService4/go", payload='East')


    def WdirectionbuttonClicked(self):
        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked
        if d1buttonClicked:
            self.client.publish("miMain/autopilotService/go", payload = 'West')
        if d2buttonClicked:
            self.client.publish("miMain/autopilotService2/go", payload='West')
        if d3buttonClicked:
            self.client.publish("miMain/autopilotService3/go", payload='West')
        if d4buttonClicked:
            self.client.publish("miMain/autopilotService4/go", payload='West')


    def NEdirectionbuttonClicked (self):
        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked
        if d1buttonClicked:
            self.client.publish("miMain/autopilotService/go", payload='NorthEast')
        if d2buttonClicked:
            self.client.publish("miMain/autopilotService2/go", payload='NorthEast')
        if d3buttonClicked:
            self.client.publish("miMain/autopilotService3/go", payload='NorthEast')
        if d4buttonClicked:
            self.client.publish("miMain/autopilotService4/go", payload='NorthEast')

    def NWdirectionbuttonClicked (self):
        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked
        if d1buttonClicked:
            self.client.publish("miMain/autopilotService/go", payload='NorthWest')
        if d2buttonClicked:
            self.client.publish("miMain/autopilotService2/go", payload='NorthWest')
        if d3buttonClicked:
            self.client.publish("miMain/autopilotService3/go", payload='NorthWest')
        if d4buttonClicked:
            self.client.publish("miMain/autopilotService4/go", payload='NorthWest')

    def SEdirectionbuttonClicked (self):
        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked
        if d1buttonClicked:
            self.client.publish("miMain/autopilotService/go", payload='SouthEast')
        if d2buttonClicked:
            self.client.publish("miMain/autopilotService2/go", payload='SouthEast')
        if d3buttonClicked:
            self.client.publish("miMain/autopilotService3/go", payload='SouthEast')
        if d4buttonClicked:
            self.client.publish("miMain/autopilotService4/go", payload='SouthEast')

    def SWdirectionbuttonClicked (self):
        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked
        if d1buttonClicked:
            self.client.publish("miMain/autopilotService/go", payload='SouthWest')
        if d2buttonClicked:
            self.client.publish("miMain/autopilotService2/go", payload='SouthWest')
        if d3buttonClicked:
            self.client.publish("miMain/autopilotService3/go", payload='SouthWest')
        if d4buttonClicked:
            self.client.publish("miMain/autopilotService4/go", payload='SouthWest')

    def StopbuttonClicked (self):
        global d1buttonClicked
        global d2buttonClicked
        global d3buttonClicked
        global d4buttonClicked

        self.BorrarRastro()


        if d1buttonClicked:
            self.client.publish("miMain/autopilotService/go", payload='Stop')
        if d2buttonClicked:
            self.client.publish("miMain/autopilotService2/go", payload='Stop')
        if d3buttonClicked:
            self.client.publish("miMain/autopilotService3/go", payload='Stop')
        if d4buttonClicked:
            self.client.publish("miMain/autopilotService4/go", payload='Stop')









