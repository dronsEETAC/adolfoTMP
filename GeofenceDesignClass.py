import json
import math
from tkinter import messagebox
import time

import customtkinter as ctk
import tkinter as tk
import os
from tkinter import *
from PIL import Image, ImageTk
from geographiclib.geodesic import Geodesic
import ConfiguraciónyConexiónClass
import paho.mqtt.client as mqtt



g1selected = False
g2selected = False
gcustomselected = False
designcount = 0
x_y_coord = []
x_y_coord1 = []
x_y_coord2 = []
x_y_coord3 = []
x_y_coord4 = []

class GeofenceDesignClass:

    def BuildFrame(self, fatherFrame, client, Ndrones):

        self.client = client
        self.conversor = ComputeCoords()
        self.Ndrones = Ndrones
        self.geofenceFrame = ctk.CTkFrame(fatherFrame)
        self.geofenceFrame.rowconfigure(0, weight=1)
        self.geofenceFrame.rowconfigure(1, weight=20)
        self.geofenceFrame.columnconfigure(0, weight=1)
        self.geofenceFrame.columnconfigure(1, weight=1)
        self.geofenceFrame.columnconfigure(2, weight=1)


        self.canvas = Canvas(self.geofenceFrame, height=600, width=800, bg='black')
        self.canvas.grid(row = 1, column = 0, columnspan=3, padx=1, pady=1, sticky="nsew")
        self.image = Image.open("recintoDrone.png")
        # self.image = self.image.resize((1350,700), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0,0, image = self.image, anchor='nw')


        self.startButton = ctk.CTkButton(self.geofenceFrame, text = "Diseñar un Geofence", command = self.startButtonClicked)
        self.startButton.grid(row = 0, column = 0, padx=10, pady=10, sticky="nsew")
        CreateToolTip(self.startButton, text='Funcionamiento:\n'
                                   ' -Click izquierdo para fijar punto. \n'
                                   ' -Click derecho para enlazar con punto incial y terminar diseño.')

        self.guardarButton = ctk.CTkButton(self.geofenceFrame, text="Cargar diseño al dron", command=self.guardartButtonClicked)
        self.guardarButton.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.predeterminadoButton = ctk.CTkButton(self.geofenceFrame, text="Ver Geofence predeterminados", command=self.predeterminadoButtonClicked)
        self.predeterminadoButton.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")



        return self.geofenceFrame



    def startButtonClicked(self):

        self.count = 0
        self.currentPath = None
        self.x_coord_array = []
        self.y_coord_array = []
        # self.x_y_coord = []
        self.lat_lon_coord = [[41.27640942348419, 1.9886658713221552]]
        self.lat_lon_coord_json = [{"lat": 41.27640942348419, "lon": 1.9886658713221552}]
        messagebox.showinfo("Information", "Diseño geofence habilitado")
        if self.Ndrones == "1":
            self.geof_design1 = []

        if self.Ndrones == "2":
            self.geof_design1 = []
            self.geof_design2 = []

        if self.Ndrones == "3":
            self.geof_design1 = []
            self.geof_design2 = []
            self.geof_design3 = []

        if self.Ndrones == "4":
            self.geof_design1 = []
            self.geof_design2 = []
            self.geof_design3 = []
            self.geof_design4 = []
        self.canvas.bind("<Button-1>", self.draw_line)
        self.canvas.bind("<Motion>", self.design_line)
        self.canvas.bind("<Button-3>", self.stop_draw)
        # self.canvas.bind("<B1-Motion>", self.draw_line)


    def guardartButtonClicked(self):

        global gcustomselected

        if self.Ndrones == "1":
            file1 = open('geof_coords_1.txt', 'w')
            file1.write(str(self.geof_design1[0]))
            file1.close()
            # print (str(self.geof_design1[0]))

        if self.Ndrones == "2":
            file1 = open('geof_coords_1.txt', 'w')
            file1.write(str(self.geof_design1[0]))
            file1.close()

            file2 = open('geof_coords_2.txt', 'w')
            file2.write(str(self.geof_design2[0]))
            file2.close()
            # print (str(self.geof_design1))
            # print (str(self.geof_design2))

        if self.Ndrones == "3":
            file1 = open('geof_coords_1.txt', 'w')
            file1.write(str(self.geof_design1[0]))
            file1.close()

            file2 = open('geof_coords_2.txt', 'w')
            file2.write(str(self.geof_design2[0]))
            file2.close()

            file3 = open('geof_coords_3.txt', 'w')
            file3.write(str(self.geof_design3[0]))
            file3.close()

        if self.Ndrones == "4":
            file1 = open('geof_coords_1.txt', 'w')
            file1.write(str(self.geof_design1[0]))
            file1.close()

            file2 = open('geof_coords_2.txt', 'w')
            file2.write(str(self.geof_design2[0]))
            file2.close()

            file3 = open('geof_coords_3.txt', 'w')
            file3.write(str(self.geof_design3[0]))
            file3.close()

            file4 = open('geof_coords_4.txt', 'w')
            file4.write(str(self.geof_design4[0]))
            file4.close()

        gcustomselected = True




    def predeterminadoButtonClicked(self):

        self.geof_predet = ctk.CTkToplevel(self.geofenceFrame)
        self.geof_predet.title("Geofence predeterminados")
        self.geof_predet.geometry("1350x450")
        self.geof_predet.grab_set()


        self.geof_predet_Frame = ctk.CTkFrame(self.geof_predet)
        self.geof_predet_Frame.pack(fill="both", expand="yes", padx=10, pady=10)
        self.geof_predet_Frame.rowconfigure(0, weight=20)
        self.geof_predet_Frame.rowconfigure(1, weight=1)
        self.geof_predet_Frame.columnconfigure(0, weight=1)
        self.geof_predet_Frame.columnconfigure(1, weight=1)



        if self.Ndrones == "1":

            self.image_width = 1000
            self.image_height = 350
            self.image_path = 'G_1d.png'

            self.Geofence_1 = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path)),
                                           size=(self.image_width, self.image_height))
            label = ctk.CTkLabel(self.geof_predet_Frame, image=self.Geofence_1)
            label.grid(row=0, column=0,columnspan = 2, padx=10, pady=10)

            self.selectGeof = ctk.CTkButton(self.geof_predet_Frame, text="Seleccionar Geofence", command=self.G1_selected)
            self.selectGeof.grid(row=1, column=0, columnspan = 2, padx=10, pady=10, sticky="nsew")

        if self.Ndrones == "2":
            self.image_width = 600
            self.image_height = 300
            self.image_path1 = 'G1_2d.png'

            self.Geofence_1 = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path1)),
                                           size=(self.image_width, self.image_height))
            label = ctk.CTkLabel(self.geof_predet_Frame, image=self.Geofence_1)
            label.grid(row=0, column=0, padx=10, pady=10)

            self.image_width = 600
            self.image_height = 300
            self.image_path2 = 'G2_2d.png'

            self.Geofence_2 = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path2)),
                                           size=(self.image_width, self.image_height))
            label = ctk.CTkLabel(self.geof_predet_Frame, image=self.Geofence_2)
            label.grid(row=0, column=1, padx=10, pady=10)

            self.selectG1 = ctk.CTkButton(self.geof_predet_Frame, text="Seleccionar Geofence 1", command=self.G1_selected)
            self.selectG1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

            self.selectG2 = ctk.CTkButton(self.geof_predet_Frame, text="Seleccionar Geofence 2", command=self.G2_selected)
            self.selectG2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        if self.Ndrones == "3":
            self.image_width = 600
            self.image_height = 300
            self.image_path1 = 'G1_3d.png'

            self.Geofence_1 = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path1)),
                                           size=(self.image_width, self.image_height))
            label = ctk.CTkLabel(self.geof_predet_Frame, image=self.Geofence_1)
            label.grid(row=0, column=0, padx=10, pady=10)

            self.image_width = 600
            self.image_height = 300
            self.image_path2 = 'G2_3d.png'

            self.Geofence_2 = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path2)),
                                           size=(self.image_width, self.image_height))
            label = ctk.CTkLabel(self.geof_predet_Frame, image=self.Geofence_2)
            label.grid(row=0, column=1, padx=10, pady=10)

            self.selectG1 = ctk.CTkButton(self.geof_predet_Frame, text="Seleccionar Geofence 1", command=self.G1_selected)
            self.selectG1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

            self.selectG2 = ctk.CTkButton(self.geof_predet_Frame, text="Seleccionar Geofence 2", command=self.G2_selected)
            self.selectG2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        if self.Ndrones == "4":
            self.image_width = 600
            self.image_height = 300
            self.image_path1 = 'G1_4d.png'

            self.Geofence_1 = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path1)),
                                           size=(self.image_width, self.image_height))
            label = ctk.CTkLabel(self.geof_predet_Frame, image=self.Geofence_1)
            label.grid(row=0, column=0, padx=10, pady=10)

            self.image_width = 600
            self.image_height = 300
            self.image_path2 = 'G2_4d.png'

            self.Geofence_2 = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path2)),
                                           size=(self.image_width, self.image_height))
            label = ctk.CTkLabel(self.geof_predet_Frame, image=self.Geofence_2)
            label.grid(row=0, column=1, padx=10, pady=10)

            self.selectG1 = ctk.CTkButton(self.geof_predet_Frame, text="Seleccionar Geofence 1", command=self.G1_selected)
            self.selectG1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

            self.selectG2 = ctk.CTkButton(self.geof_predet_Frame, text="Seleccionar Geofence 2", command=self.G2_selected)
            self.selectG2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")



    def draw_line(self, e):
        global lastx
        global lasty
        global x_y_coord

        if designcount < float(self.Ndrones):

            if self.count >0:
                if designcount == 0:
                    self.fence_draw = self.canvas.create_line(lastx, lasty, e.x, e.y, width=5, fill="red")

                if designcount == 1:
                    self.fence_draw = self.canvas.create_line(lastx, lasty, e.x, e.y, width=5, fill="blue")

                if designcount == 2:
                    self.fence_draw = self.canvas.create_line(lastx, lasty, e.x, e.y, width=5, fill="yellow")

                if designcount == 3:
                    self.fence_draw = self.canvas.create_line(lastx, lasty, e.x, e.y, width=5, fill="green")

            lastx = e.x
            lasty = e.y
            self.x_coord_array.append(lastx)
            self.y_coord_array.append(lasty)

            self.lat_coord, self.lon_coord = self.conversor.convertToPosition([lastx, lasty])
            self.lat_lon_coord.append([self.lat_coord, self.lon_coord])
            self.lat_lon_coord_json.append({"lat": self.lat_coord, "lon": self.lon_coord})
            x_y_coord.append([lastx, lasty])

            print (lastx, lasty)
            print ("vector", x_y_coord)


            self.count = self.count +1

            return self.lat_lon_coord

        else:
            messagebox.showinfo("Information", "No se pueden crear más geofence")

    def design_line(self,e):
        if self.count > 0:
            if self.currentPath:
                self.canvas.delete(self.currentPath)
            self.currentPath = self.canvas.create_line(lastx, lasty, e.x, e.y, width=5, fill="grey")
            # print (e.x, e.y)

    def stop_draw(self, e):

        global designcount
        global x_y_coord
        global x_y_coord1
        global x_y_coord2
        global x_y_coord3
        global x_y_coord4

        if designcount < float(self.Ndrones):
            if designcount == 0:

                self.lat_lon_coord_json.append({"lat": self.lat_lon_coord[1][0], "lon": self.lat_lon_coord[1][1]})
                self.geof_design1.append(self.lat_lon_coord_json)
                print ("g1", self.geof_design1)
                self.lat_lon_coord = [[41.27640942348419, 1.9886658713221552]]
                self.lat_lon_coord_json = [{"lat": 41.27640942348419, "lon": 1.9886658713221552}]
                self.count = 0
                # self.canvas.unbind("<Motion>")
                self.canvas.delete(self.currentPath)
                x_y_coord.append([x_y_coord[0][0], x_y_coord[0][1]])
                self.canvas.create_line(lastx, lasty, x_y_coord[0][0], x_y_coord[0][1], width=5, fill="red")
                x_y_coord1.append(x_y_coord)
                x_y_coord = []
                self.x_y_poligon1 = []
                for n in x_y_coord1:
                    self.x_y_poligon1 += n





                self.canvas.create_polygon(self.x_y_poligon1, fill='red', stipple="gray12")
                messagebox.showinfo("Information", "Diseño geofence 1 guardado")


            if designcount == 1:

                self.lat_lon_coord_json.append({"lat": self.lat_lon_coord[1][0], "lon": self.lat_lon_coord[1][1]})
                self.geof_design2.append(self.lat_lon_coord_json)
                print("g2", self.geof_design2)
                self.lat_lon_coord = [[41.27640942348419, 1.9886658713221552]]
                self.lat_lon_coord_json = [{"lat": 41.27640942348419, "lon": 1.9886658713221552}]
                self.count = 0
                # self.canvas.unbind("<Motion>")
                self.canvas.delete(self.currentPath)
                x_y_coord.append([x_y_coord[0][0], x_y_coord[0][1]])
                self.canvas.create_line(lastx, lasty, x_y_coord[0][0], x_y_coord[0][1], width=5, fill="blue")
                x_y_coord2.append(x_y_coord)
                x_y_coord = []
                self.x_y_poligon2 = []
                for n in x_y_coord2:
                    self.x_y_poligon2 += n

                self.canvas.create_polygon(self.x_y_poligon2, fill='blue', stipple="gray12")
                messagebox.showinfo("Information", "Diseño geofence 2 guardado")



            if designcount == 2:

                self.lat_lon_coord_json.append({"lat": self.lat_lon_coord[1][0], "lon": self.lat_lon_coord[1][1]})
                self.geof_design3.append(self.lat_lon_coord_json)
                print("g3", self.geof_design3)
                self.lat_lon_coord = [[41.27640942348419, 1.9886658713221552]]
                self.lat_lon_coord_json = [{"lat": 41.27640942348419, "lon": 1.9886658713221552}]
                self.count = 0
                # self.canvas.unbind("<Motion>")
                self.canvas.delete(self.currentPath)
                x_y_coord.append([x_y_coord[0][0], x_y_coord[0][1]])
                self.canvas.create_line(lastx, lasty, x_y_coord[0][0], x_y_coord[0][1], width=5, fill="yellow")
                x_y_coord3.append(x_y_coord)
                x_y_coord = []
                self.x_y_poligon3 = []
                for n in x_y_coord3:
                    self.x_y_poligon3 += n


                self.canvas.create_polygon(self.x_y_poligon3, fill='yellow', stipple="gray12")
                messagebox.showinfo("Information", "Diseño geofence 3 guardado")

            if designcount == 3:

                self.lat_lon_coord_json.append({"lat": self.lat_lon_coord[1][0], "lon": self.lat_lon_coord[1][1]})
                self.geof_design4.append(self.lat_lon_coord_json)
                print("g4", self.geof_design4)
                self.lat_lon_coord = [[41.27640942348419, 1.9886658713221552]]
                self.lat_lon_coord_json = [{"lat": 41.27640942348419, "lon": 1.9886658713221552}]
                self.count = 0
                # self.canvas.unbind("<Motion>")
                self.canvas.delete(self.currentPath)
                x_y_coord.append([x_y_coord[0][0], x_y_coord[0][1]])
                self.canvas.create_line(lastx, lasty, x_y_coord[0][0], x_y_coord[0][1], width=5, fill="green")
                x_y_coord4.append(x_y_coord)
                x_y_coord = []
                self.x_y_poligon4 = []
                for n in x_y_coord4:
                    self.x_y_poligon4 += n

                self.canvas.create_polygon(self.x_y_poligon4, fill='green', stipple="gray12")
                messagebox.showinfo("Information", "Diseño geofence 4 guardado")

            designcount = designcount + 1

        else:
            messagebox.showinfo("Information", "No se pueden guardar más geofence")




    def cargarGeofence(self, Ndrones):
        global x_y_coord
        global x_y_coord1
        global x_y_coord2
        global x_y_coord3
        global x_y_coord4
        self.Ndroness = Ndrones

        if g1selected:
            return "g1", 0, 0, 0, 0
        if g2selected:
            return "g2", 0, 0, 0, 0
        if gcustomselected:

            if self.Ndroness == "1":
                return "custom", x_y_coord1[0], 0, 0, 0
            if self.Ndroness == "2":
                return "custom", x_y_coord1[0], x_y_coord2[0], 0, 0
            if self.Ndroness == "3":
                return "custom", x_y_coord1[0], x_y_coord2[0], x_y_coord3[0], 0
            if self.Ndroness == "4":
                return "custom", x_y_coord1[0], x_y_coord2[0], x_y_coord3[0], x_y_coord4[0]



    def G1_selected(self):

        global g1selected
        global g2selected

        self.canvas.delete("all")

        self.image = Image.open("recintoDrone.png")
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.image, anchor='nw')

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
        self.AD1_3c = [((self.AAc[0] - self.DDc[0]) / 3) + self.DDc[0],
                       ((self.DDc[1] - self.AAc[1]) * 2 / 3) + self.AAc[1]]
        self.AD2_3c = [((self.AAc[0] - self.DDc[0]) * 2 / 3) + self.DDc[0],
                       ((self.DDc[1] - self.AAc[1]) / 3) + self.AAc[1]]
        self.BC1c = [((self.BBc[0] - self.CCc[0]) / 2) + self.CCc[0], ((self.CCc[1] - self.BBc[1]) / 2) + self.BBc[1]]
        self.BC1_3c = [((self.BBc[0] - self.CCc[0]) / 3) + self.CCc[0],
                       ((self.CCc[1] - self.BBc[1]) * 2 / 3) + self.BBc[1]]
        self.BC2_3c = [((self.BBc[0] - self.CCc[0]) * 2 / 3) + self.CCc[0],
                       ((self.CCc[1] - self.BBc[1]) / 3) + self.BBc[1]]
        self.MMc = [((self.AB2c[0] - self.DC2c[0]) / 2) + self.DC2c[0],
                    ((self.BC1c[1] - self.AD1c[1]) / 2) + self.AD1c[1]]

        if self.Ndrones == "1":
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.image, anchor='nw')

            self.canvas.create_line(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], width=2, fill="red")
            self.canvas.create_line(self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], width=2, fill="red")
            self.canvas.create_line(self.CCc[1], self.CCc[0], self.DDc[1], self.DDc[0], width=2, fill="red")
            self.canvas.create_line(self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], width=2, fill="red")

            self.canvas.create_polygon(self.AAc[1], self.AAc[0],self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], self.DDc[1], self.DDc[0], fill='red',stipple="gray12")

        if self.Ndrones == "2":
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.image, anchor='nw')

            self.canvas.create_line(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], width=2, fill="red")
            self.canvas.create_line(self.BBc[1], self.BBc[0], self.BC1c[1], self.BC1c[0], width=2, fill="red")
            self.canvas.create_line(self.BC1c[1], self.BC1c[0], self.AD1c[1], self.AD1c[0], width=2, fill="red")
            self.canvas.create_line(self.AD1c[1], self.AD1c[0], self.AAc[1], self.AAc[0], width=2, fill="red")

            self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], self.BC1c[1], self.BC1c[0], self.AD1c[1], self.AD1c[0], self.AAc[1], self.AAc[0], fill='red',stipple="gray12")

            self.canvas.create_line(self.AD1c[1], self.AD1c[0], self.BC1c[1], self.BC1c[0], width=2, fill="blue")
            self.canvas.create_line(self.BC1c[1], self.BC1c[0], self.CCc[1], self.CCc[0], width=2, fill="blue")
            self.canvas.create_line(self.CCc[1], self.CCc[0], self.DDc[1], self.DDc[0], width=2, fill="blue")
            self.canvas.create_line(self.DDc[1], self.DDc[0], self.AD1c[1], self.AD1c[0], width=2, fill="blue")
            self.canvas.create_polygon(self.AD1c[1], self.AD1c[0], self.BC1c[1], self.BC1c[0], self.CCc[1], self.CCc[0], self.DDc[1], self.DDc[0], self.AD1c[1], self.AD1c[0], fill='blue',stipple="gray12")

        if self.Ndrones == "3":
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.image, anchor='nw')

            self.canvas.create_line(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], width=2, fill="red")
            self.canvas.create_line(self.BBc[1], self.BBc[0], self.BC2_3c[1], self.BC2_3c[0], width=2, fill="red")
            self.canvas.create_line(self.BC2_3c[1], self.BC2_3c[0], self.AD2_3c[1], self.AD2_3c[0], width=2, fill="red")
            self.canvas.create_line(self.AD2_3c[1], self.AD2_3c[0], self.AAc[1], self.AAc[0], width=2, fill="red")
            self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], self.BC2_3c[1], self.BC2_3c[0], self.AD2_3c[1], self.AD2_3c[0], self.AAc[1], self.AAc[0], fill='red',stipple="gray12")

            self.canvas.create_line(self.AD1_3c[1], self.AD1_3c[0], self.BC1_3c[1], self.BC1_3c[0], width=2,
                                    fill="blue")
            self.canvas.create_line(self.BC1_3c[1], self.BC1_3c[0], self.BC2_3c[1], self.BC2_3c[0], width=2,
                                    fill="blue")
            self.canvas.create_line(self.BC2_3c[1], self.BC2_3c[0], self.AD2_3c[1], self.AD2_3c[0], width=2,
                                    fill="blue")
            self.canvas.create_line(self.AD2_3c[1], self.AD2_3c[0], self.AD1_3c[1], self.AD1_3c[0], width=2,
                                    fill="blue")
            self.canvas.create_polygon(self.AD1_3c[1], self.AD1_3c[0], self.BC1_3c[1], self.BC1_3c[0], self.BC2_3c[1], self.BC2_3c[0], self.AD2_3c[1], self.AD2_3c[0], self.AD1_3c[1], self.AD1_3c[0], fill='blue',stipple="gray12")

            self.canvas.create_line(self.AD1_3c[1], self.AD1_3c[0], self.BC1_3c[1], self.BC1_3c[0], width=2,
                                    fill="yellow")
            self.canvas.create_line(self.BC1_3c[1], self.BC1_3c[0], self.CCc[1], self.CCc[0], width=2, fill="yellow")
            self.canvas.create_line(self.CCc[1], self.CCc[0], self.DDc[1], self.DDc[0], width=2, fill="yellow")
            self.canvas.create_line(self.DDc[1], self.DDc[0], self.AD1_3c[1], self.AD1_3c[0], width=2, fill="yellow")
            self.canvas.create_polygon(self.AD1_3c[1], self.AD1_3c[0], self.BC1_3c[1], self.BC1_3c[0], self.CCc[1], self.CCc[0], self.DDc[1], self.DDc[0], self.AD1_3c[1], self.AD1_3c[0], fill='yellow',stipple="gray12")

        if self.Ndrones == "4":
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.image, anchor='nw')

            self.canvas.create_line(self.AAc[1], self.AAc[0], self.AB2c[1], self.AB2c[0], width=2, fill="red")
            self.canvas.create_line(self.AB2c[1], self.AB2c[0], self.MMc[1], self.MMc[0], width=2, fill="red")
            self.canvas.create_line(self.MMc[1], self.MMc[0], self.AD1c[1], self.AD1c[0], width=2, fill="red")
            self.canvas.create_line(self.AD1c[1], self.AD1c[0], self.AAc[1], self.AAc[0], width=2, fill="red")
            self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.AB2c[1], self.AB2c[0], self.MMc[1], self.MMc[0], self.AD1c[1], self.AD1c[0], self.AAc[1], self.AAc[0], fill='red',stipple="gray12")

            self.canvas.create_line(self.AB2c[1], self.AB2c[0], self.BBc[1], self.BBc[0], width=2, fill="blue")
            self.canvas.create_line(self.BBc[1], self.BBc[0], self.BC1c[1], self.BC1c[0], width=2, fill="blue")
            self.canvas.create_line(self.BC1c[1], self.BC1c[0], self.MMc[1], self.MMc[0], width=2, fill="blue")
            self.canvas.create_line(self.MMc[1], self.MMc[0], self.AB2c[1], self.AB2c[0], width=2, fill="blue")
            self.canvas.create_polygon(self.AB2c[1], self.AB2c[0], self.BBc[1], self.BBc[0],self.BC1c[1], self.BC1c[0], self.MMc[1], self.MMc[0], self.AB2c[1], self.AB2c[0], fill='blue',stipple="gray12")

            self.canvas.create_line(self.AD1c[1], self.AD1c[0], self.MMc[1], self.MMc[0], width=2, fill="yellow")
            self.canvas.create_line(self.MMc[1], self.MMc[0], self.DC2c[1], self.DC2c[0], width=2, fill="yellow")
            self.canvas.create_line(self.DC2c[1], self.DC2c[0], self.DDc[1], self.DDc[0], width=2, fill="yellow")
            self.canvas.create_line(self.DDc[1], self.DDc[0], self.AD1c[1], self.AD1c[0], width=2, fill="yellow")
            self.canvas.create_polygon(self.AD1c[1], self.AD1c[0], self.MMc[1], self.MMc[0], self.DC2c[1], self.DC2c[0], self.DDc[1], self.DDc[0], self.AD1c[1], self.AD1c[0], fill='yellow',stipple="gray12")

            self.canvas.create_line(self.MMc[1], self.MMc[0], self.BC1c[1], self.BC1c[0], width=2, fill="green")
            self.canvas.create_line(self.BC1c[1], self.BC1c[0], self.CCc[1], self.CCc[0], width=2, fill="green")
            self.canvas.create_line(self.CCc[1], self.CCc[0], self.DC2c[1], self.DC2c[0], width=2, fill="green")
            self.canvas.create_line(self.DC2c[1], self.DC2c[0], self.MMc[1], self.MMc[0], width=2, fill="green")
            self.canvas.create_polygon(self.MMc[1], self.MMc[0], self.BC1c[1], self.BC1c[0], self.CCc[1], self.CCc[0], self.DC2c[1], self.DC2c[0], self.MMc[1], self.MMc[0], fill='green',stipple="gray12")

        g1selected = True
        g2selected = False
        self.geof_predet.destroy()




    def G2_selected(self):

        global g1selected
        global g2selected

        self.canvas.delete("all")

        self.image = Image.open("recintoDrone.png")
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.image, anchor='nw')

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
        self.AD1_3c = [((self.AAc[0] - self.DDc[0]) / 3) + self.DDc[0],
                       ((self.DDc[1] - self.AAc[1]) * 2 / 3) + self.AAc[1]]
        self.AD2_3c = [((self.AAc[0] - self.DDc[0]) * 2 / 3) + self.DDc[0],
                       ((self.DDc[1] - self.AAc[1]) / 3) + self.AAc[1]]
        self.BC1c = [((self.BBc[0] - self.CCc[0]) / 2) + self.CCc[0], ((self.CCc[1] - self.BBc[1]) / 2) + self.BBc[1]]
        self.BC1_3c = [((self.BBc[0] - self.CCc[0]) / 3) + self.CCc[0],
                       ((self.CCc[1] - self.BBc[1]) * 2 / 3) + self.BBc[1]]
        self.BC2_3c = [((self.BBc[0] - self.CCc[0]) * 2 / 3) + self.CCc[0],
                       ((self.CCc[1] - self.BBc[1]) / 3) + self.BBc[1]]
        self.MMc = [((self.AB2c[0] - self.DC2c[0]) / 2) + self.DC2c[0],
                    ((self.BC1c[1] - self.AD1c[1]) / 2) + self.AD1c[1]]

        if self.Ndrones == "1":
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.image, anchor='nw')

            self.canvas.create_line(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], width=2, fill="red")
            self.canvas.create_line(self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], width=2, fill="red")
            self.canvas.create_line(self.CCc[1], self.CCc[0], self.DDc[1], self.DDc[0], width=2, fill="red")
            self.canvas.create_line(self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], width=2, fill="red")
            self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], fill='red',stipple="gray12")

        if self.Ndrones == "2":
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.image, anchor='nw')

            self.canvas.create_line(self.AAc[1], self.AAc[0], self.AB2c[1], self.AB2c[0], width=2, fill="red")
            self.canvas.create_line(self.AB2c[1], self.AB2c[0], self.DC2c[1], self.DC2c[0], width=2, fill="red")
            self.canvas.create_line(self.DC2c[1], self.DC2c[0], self.DDc[1], self.DDc[0], width=2, fill="red")
            self.canvas.create_line(self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], width=2, fill="red")
            self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.AB2c[1], self.AB2c[0], self.DC2c[1], self.DC2c[0], self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], fill='red',stipple="gray12")

            self.canvas.create_line(self.AB2c[1], self.AB2c[0], self.BBc[1], self.BBc[0], width=2, fill="blue")
            self.canvas.create_line(self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], width=2, fill="blue")
            self.canvas.create_line(self.CCc[1], self.CCc[0], self.DC2c[1], self.DC2c[0], width=2, fill="blue")
            self.canvas.create_line(self.DC2c[1], self.DC2c[0], self.AB2c[1], self.AB2c[0], width=2, fill="blue")
            self.canvas.create_polygon(self.AB2c[1], self.AB2c[0], self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], self.DC2c[1], self.DC2c[0], self.AB2c[1], self.AB2c[0], fill='blue',stipple="gray12")

        if self.Ndrones == "3":
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.image, anchor='nw')

            self.canvas.create_line(self.AAc[1], self.AAc[0], self.AB1_3c[1], self.AB1_3c[0], width=2, fill="red")
            self.canvas.create_line(self.AB1_3c[1], self.AB1_3c[0], self.DC1_3c[1], self.DC1_3c[0], width=2, fill="red")
            self.canvas.create_line(self.DC1_3c[1], self.DC1_3c[0], self.DDc[1], self.DDc[0], width=2,
                                    fill="red")
            self.canvas.create_line(self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], width=2, fill="red")
            self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.AB1_3c[1], self.AB1_3c[0], self.DC1_3c[1], self.DC1_3c[0], self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], fill='red',stipple="gray12")

            self.canvas.create_line(self.AB1_3c[1], self.AB1_3c[0], self.AB2_3c[1], self.AB2_3c[0], width=2,
                                    fill="blue")
            self.canvas.create_line(self.AB2_3c[1], self.AB2_3c[0], self.DC2_3c[1], self.DC2_3c[0], width=2,
                                    fill="blue")
            self.canvas.create_line(self.DC2_3c[1], self.DC2_3c[0], self.DC1_3c[1], self.DC1_3c[0], width=2,
                                    fill="blue")
            self.canvas.create_line(self.DC1_3c[1], self.DC1_3c[0], self.AB1_3c[1], self.AB1_3c[0], width=2,
                                    fill="blue")
            self.canvas.create_polygon(self.AB1_3c[1], self.AB1_3c[0], self.AB2_3c[1], self.AB2_3c[0], self.DC2_3c[1], self.DC2_3c[0], self.DC1_3c[1], self.DC1_3c[0], self.AB1_3c[1], self.AB1_3c[0], fill='blue',stipple="gray12")

            self.canvas.create_line(self.AB2_3c[1], self.AB2_3c[0], self.BBc[1], self.BBc[0], width=2,
                                    fill="yellow")
            self.canvas.create_line(self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], width=2,
                                    fill="yellow")
            self.canvas.create_line(self.CCc[1], self.CCc[0], self.DC2_3c[1], self.DC2_3c[0], width=2, fill="yellow")
            self.canvas.create_line(self.DC2_3c[1], self.DC2_3c[0], self.AB2_3c[1], self.AB2_3c[0], width=2,
                                    fill="yellow")
            self.canvas.create_polygon(self.AB2_3c[1], self.AB2_3c[0], self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], self.DC2_3c[1], self.DC2_3c[0], self.AB2_3c[1], self.AB2_3c[0], fill='yellow',stipple="gray12")

        if self.Ndrones == "4":
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.image, anchor='nw')

            self.canvas.create_line(self.AAc[1], self.AAc[0], self.AB1c[1], self.AB1c[0], width=2, fill="red")
            self.canvas.create_line(self.AB1c[1], self.AB1c[0], self.DC1c[1], self.DC1c[0], width=2, fill="red")
            self.canvas.create_line(self.DC1c[1], self.DC1c[0], self.DDc[1], self.DDc[0], width=2, fill="red")
            self.canvas.create_line(self.DDc[1], self.DDc[0], self.AAc[1], self.AAc[0], width=2, fill="red")
            self.canvas.create_polygon(self.AAc[1], self.AAc[0], self.AB1c[1], self.AB1c[0], self.DC1c[1], self.DC1c[0], self.DDc[1], self.DDc[0],self.AAc[1], self.AAc[0], fill='red',stipple="gray12")

            self.canvas.create_line(self.AB1c[1], self.AB1c[0], self.AB2c[1], self.AB2c[0], width=2, fill="blue")
            self.canvas.create_line(self.AB2c[1], self.AB2c[0], self.DC2c[1], self.DC2c[0], width=2, fill="blue")
            self.canvas.create_line(self.DC2c[1], self.DC2c[0], self.DC1c[1], self.DC1c[0], width=2, fill="blue")
            self.canvas.create_line(self.DC1c[1], self.DC1c[0], self.AB1c[1], self.AB1c[0], width=2, fill="blue")
            self.canvas.create_polygon(self.AB1c[1], self.AB1c[0], self.AB2c[1], self.AB2c[0], self.DC2c[1], self.DC2c[0], self.DC1c[1], self.DC1c[0], self.AB1c[1], self.AB1c[0], fill='blue',stipple="gray12")

            self.canvas.create_line(self.AB2c[1], self.AB2c[0], self.AB3c[1], self.AB3c[0], width=2, fill="yellow")
            self.canvas.create_line(self.AB3c[1], self.AB3c[0], self.DC3c[1], self.DC3c[0], width=2, fill="yellow")
            self.canvas.create_line(self.DC3c[1], self.DC3c[0], self.DC2c[1], self.DC2c[0], width=2, fill="yellow")
            self.canvas.create_line(self.DC2c[1], self.DC2c[0], self.AB2c[1], self.AB2c[0], width=2, fill="yellow")
            self.canvas.create_polygon(self.AB2c[1], self.AB2c[0], self.AB3c[1], self.AB3c[0], self.DC3c[1], self.DC3c[0], self.DC2c[1], self.DC2c[0], self.AB2c[1], self.AB2c[0], fill='yellow',stipple="gray12")

            self.canvas.create_line(self.AB3c[1], self.AB3c[0], self.BBc[1], self.BBc[0], width=2, fill="green")
            self.canvas.create_line(self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], width=2, fill="green")
            self.canvas.create_line(self.CCc[1], self.CCc[0], self.DC3c[1], self.DC3c[0], width=2, fill="green")
            self.canvas.create_line(self.DC3c[1], self.DC3c[0], self.AB3c[1], self.AB3c[0], width=2, fill="green")
            self.canvas.create_polygon(self.AB3c[1], self.AB3c[0], self.BBc[1], self.BBc[0], self.CCc[1], self.CCc[0], self.DC3c[1], self.DC3c[0], self.AB3c[1], self.AB3c[0], fill='green',stipple="gray12")

        g2selected = True
        g1selected = False
        self.geof_predet.destroy()



    def set_Geofence(self, drone, Ndrones, margen_geof, geof_action, PILOT_SPEED_UP_valor, RTL_ALT_valor, FENCE_ENABLE_valor, FENCE_ALT_MAX_valor, FLTMODE6_valor):

        self.Ndrones = Ndrones
        self.margen_geof = margen_geof
        self.geof_action = geof_action
        self.PILOT_SPEED_UP_valor = PILOT_SPEED_UP_valor
        self.RTL_ALT_valor = RTL_ALT_valor
        self.FENCE_ENABLE_valor = FENCE_ENABLE_valor
        self.FENCE_ALT_MAX_valor = FENCE_ALT_MAX_valor
        self.FLTMODE6_valor = FLTMODE6_valor

        self.paramList = [{'FENCE_ALT_MAX': self.FENCE_ALT_MAX_valor, 'FENCE_ENABLE': self.FENCE_ENABLE_valor,
                          'FENCE_MARGIN': self.margen_geof, 'FENCE_ACTION': self.geof_action,
                          'PILOT_SPEED_UP': self.PILOT_SPEED_UP_valor, 'RTL_ALT': self.RTL_ALT_valor,
                          'FLTMODE6': self.FLTMODE6_valor}]


        self.OO = [41.27640942348419, 1.9886658713221552]
        # self.AA = [41.27643361279337, 1.988196484744549]
        # self.BB = [41.27663317425185, 1.9890118762850764]
        # self.CC = [41.27635096595008, 1.9891352578997614]
        # self.DD = [41.27615341941283, 1.9883145019412043]

        self.AA = [41.2764267, 1.9882317]
        self.BB = [41.2766066, 1.9890182]
        self.CC = [41.2763652, 1.98911288]
        self.DD = [41.2761717, 1.9883336]
        self.AB1 = [((self.BB[0] - self.AA[0])/4) + self.AA[0], ((self.BB[1] - self.AA[1])/4) + self.AA[1]]
        self.AB2 = [((self.BB[0] - self.AA[0])/2) + self.AA[0], ((self.BB[1] - self.AA[1])/2) + self.AA[1]]
        self.AB3 = [((self.BB[0] - self.AA[0])*3/4) + self.AA[0], ((self.BB[1] - self.AA[1])*3/4) + self.AA[1]]
        self.AB1_3 = [((self.BB[0] - self.AA[0]) / 3) + self.AA[0], ((self.BB[1] - self.AA[1]) / 3) + self.AA[1]]
        self.AB2_3 = [((self.BB[0] - self.AA[0]) * 2 / 3) + self.AA[0],
                       ((self.BB[1] - self.AA[1]) * 2 / 3) + self.AA[1]]
        self.DC1 = [((self.CC[0] - self.DD[0]) / 4) + self.DD[0], ((self.CC[1] - self.DD[1]) / 4) + self.DD[1]]
        self.DC2 = [((self.CC[0] - self.DD[0])/2) + self.DD[0], ((self.CC[1] - self.DD[1])/2) + self.DD[1]]
        self.DC3 = [((self.CC[0] - self.DD[0])*3/4) + self.DD[0], ((self.CC[1] - self.DD[1])*3/4) + self.DD[1]]
        self.DC1_3 = [((self.CC[0] - self.DD[0]) / 3) + self.DD[0], ((self.CC[1] - self.DD[1]) / 3) + self.DD[1]]
        self.DC2_3 = [((self.CC[0] - self.DD[0]) * 2 / 3) + self.DD[0],
                       ((self.CC[1] - self.DD[1]) * 2 / 3) + self.DD[1]]
        self.AD1 = [((self.AA[0] - self.DD[0])/2) + self.DD[0], ((self.DD[1] - self.AA[1])/2) + self.AA[1]]
        self.AD1_3 = [((self.AA[0] - self.DD[0]) / 3) + self.DD[0],
                       ((self.DD[1] - self.AA[1]) * 2 / 3) + self.AA[1]]
        self.AD2_3 = [((self.AA[0] - self.DD[0]) * 2 / 3) + self.DD[0],
                       ((self.DD[1] - self.AA[1]) / 3) + self.AA[1]]
        self.BC1 = [((self.BB[0] - self.CC[0]) / 2) + self.CC[0], ((self.CC[1] - self.BB[1]) / 2) + self.BB[1]]
        self.BC1_3 = [((self.BB[0] - self.CC[0]) / 3) + self.CC[0],
                       ((self.CC[1] - self.BB[1]) * 2 / 3) + self.BB[1]]
        self.BC2_3 = [((self.BB[0] - self.CC[0]) * 2 / 3) + self.CC[0],
                       ((self.CC[1] - self.BB[1]) / 3) + self.BB[1]]
        self.MM =  [((self.AB2[0] - self.DC2[0]) / 2) + self.DC2[0], ((self.BC1[1] - self.AD1[1]) / 2) + self.AD1[1]]

        # self.fencelist0 = [self.OO, self.AA, self.BB, self.CC, self.DD, self.AA]
        # self.fencelist0 = [self.AA, self.BB, self.CC, self.DD, self.AA]

        self.fencelist0 = [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AA[0], "lon": self.AA[1]},
    {"lat": self.BB[0], "lon": self.BB[1]},
    {"lat": self.CC[0], "lon": self.CC[1]},
    {"lat": self.DD[0], "lon": self.DD[1]},
    {"lat": self.AA[0], "lon": self.AA[1]}]

        # self.fencelist1_2_g1 = [self.OO, self.AA, self.BB, self.BC1, self.AD1, self.AA]

        self.fencelist1_2_g1 = [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AA[0], "lon": self.AA[1]},
    {"lat": self.BB[0], "lon": self.BB[1]},
    {"lat": self.BC1[0], "lon": self.BC1[1]},
    {"lat": self.AD1[0], "lon": self.AD1[1]},
    {"lat": self.AA[0], "lon": self.AA[1]}]

        # self.fencelist2_2_g1 = [self.OO, self.AD1, self.BC1, self.CC, self.DD, self.AD1]

        self.fencelist2_2_g1 = [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AD1[0], "lon": self.AD1[1]},
    {"lat": self.BC1[0], "lon": self.BC1[1]},
    {"lat": self.CC[0], "lon": self.CC[1]},
    {"lat": self.DD[0], "lon": self.DD[1]},
    {"lat": self.AD1[0], "lon": self.AD1[1]}]

        # self.fencelist1_2_g2 = [self.OO, self.AA, self.AB2, self.DC2, self.DD, self.AA]

        self.fencelist1_2_g2 = [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AA[0], "lon": self.AA[1]},
    {"lat": self.AB2[0], "lon": self.AB2[1]},
    {"lat": self.DC2[0], "lon": self.DC2[1]},
    {"lat": self.DD[0], "lon": self.DD[1]},
    {"lat": self.AA[0], "lon": self.AA[1]}]

        # self.fencelist2_2_g2 = [self.OO, self.AB2, self.BB, self.CC, self.DC2, self.AB2]

        self.fencelist2_2_g2 =  [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AB2[0], "lon": self.AB2[1]},
    {"lat": self.BB[0], "lon": self.BB[1]},
    {"lat": self.CC[0], "lon": self.CC[1]},
    {"lat": self.DC2[0], "lon": self.DC2[1]},
    {"lat": self.AB2[0], "lon": self.AB2[1]}]

        # self.fencelist1_3_g1 = [self.OO, self.AA,  self.BB,  self.BC2_3,  self.AD2_3,  self.AA]

        self.fencelist1_3_g1 =  [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AA[0], "lon": self.AA[1]},
    {"lat": self.BB[0], "lon": self.BB[1]},
    {"lat": self.BC2_3[0], "lon": self.BC2_3[1]},
    {"lat": self.AD2_3[0], "lon": self.AD2_3[1]},
    {"lat": self.AA[0], "lon": self.AA[1]}]

        # self.fencelist2_3_g1 = [self.OO, self.AD1_3, self.BC1_3, self.BC2_3, self.AD2_3, self.AD1_3]

        self.fencelist2_3_g1 =  [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AD1_3[0], "lon": self.AD1_3[1]},
    {"lat": self.BC1_3[0], "lon": self.BC1_3[1]},
    {"lat": self.BC2_3[0], "lon": self.BC2_3[1]},
    {"lat": self.AD2_3[0], "lon": self.AD2_3[1]},
    {"lat": self.AD1_3[0], "lon": self.AD1_3[1]}]

        # self.fencelist3_3_g1 = [self.OO, self.AD1_3, self.BC1_3, self.CC, self.DD, self.AD1_3]

        self.fencelist3_3_g1 =  [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AD1_3[0], "lon": self.AD1_3[1]},
    {"lat": self.BC1_3[0], "lon": self.BC1_3[1]},
    {"lat": self.CC[0], "lon": self.CC[1]},
    {"lat": self.DD[0], "lon": self.DD[1]},
    {"lat": self.AD1_3[0], "lon": self.AD1_3[1]}]

        # self.fencelist1_3_g2 = [self.OO, self.AA, self.AB1_3, self.DC1_3, self.DD, self.AA]

        self.fencelist1_3_g2 =  [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AA[0], "lon": self.AA[1]},
    {"lat": self.AB1_3[0], "lon": self.AB1_3[1]},
    {"lat": self.DC1_3[0], "lon": self.DC1_3[1]},
    {"lat": self.DD[0], "lon": self.DD[1]},
    {"lat": self.AA[0], "lon": self.AA[1]}]

        # self.fencelist2_3_g2 = [self.OO, self.AB1_3, self.AB2_3, self.DC2_3, self.DC1_3, self.AB1_3]

        self.fencelist2_3_g2 =  [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AB1_3[0], "lon": self.AB1_3[1]},
    {"lat": self.AB2_3[0], "lon": self.AB2_3[1]},
    {"lat": self.DC2_3[0], "lon": self.DC2_3[1]},
    {"lat": self.DC1_3[0], "lon": self.DC1_3[1]},
    {"lat": self.AB1_3[0], "lon": self.AB1_3[1]}]

        # self.fencelist3_3_g2 = [self.OO, self.AB2_3, self.BB, self.CC, self.DC2_3, self.AB2_3]

        self.fencelist3_3_g2 = [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AB2_3[0], "lon": self.AB2_3[1]},
    {"lat": self.BB[0], "lon": self.BB[1]},
    {"lat": self.CC[0], "lon": self.CC[1]},
    {"lat": self.DC2_3[0], "lon": self.DC2_3[1]},
    {"lat": self.AB2_3[0], "lon": self.AB2_3[1]}]

        # self.fencelist1_4_g1 = [self.OO, self.AA, self.AB2, self.MM, self.AD1, self.AA]

        self.fencelist1_4_g1 = [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AA[0], "lon": self.AA[1]},
    {"lat": self.AB2[0], "lon": self.AB2[1]},
    {"lat": self.MM[0], "lon": self.MM[1]},
    {"lat": self.AD1[0], "lon": self.AD1[1]},
    {"lat": self.AA[0], "lon": self.AA[1]}]

        # self.fencelist1_4_g2 = [self.OO, self.AA, self.AB1, self.DC1, self.DD, self.AA]

        self.fencelist1_4_g2 = [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AA[0], "lon": self.AA[1]},
    {"lat": self.AB1[0], "lon": self.AB1[1]},
    {"lat": self.DC1[0], "lon": self.DC1[1]},
    {"lat": self.DD[0], "lon": self.DD[1]},
    {"lat": self.AA[0], "lon": self.AA[1]}]

        # self.fencelist2_4_g1 = [self.OO, self.AB2, self.BB, self.BC1, self.MM, self.AB2]

        self.fencelist2_4_g1 = [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AB2[0], "lon": self.AB2[1]},
    {"lat": self.BB[0], "lon": self.BB[1]},
    {"lat": self.BC1[0], "lon": self.BC1[1]},
    {"lat": self.MM[0], "lon": self.MM[1]},
    {"lat": self.AB2[0], "lon": self.AB2[1]}]

        # self.fencelist2_4_g2 = [self.OO, self.AB1, self.AB2, self.DC2, self.DC1, self.AB1]

        self.fencelist2_4_g2 = [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AB1[0], "lon": self.AB1[1]},
    {"lat": self.AB2[0], "lon": self.AB2[1]},
    {"lat": self.DC2[0], "lon": self.DC2[1]},
    {"lat": self.DC1[0], "lon": self.DC1[1]},
    {"lat": self.AB1[0], "lon": self.AB1[1]}]

        # self.fencelist3_4_g1 = [self.OO, self.AD1, self.MM, self.DC2, self.DD, self.AD1]

        self.fencelist3_4_g1 = [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AD1[0], "lon": self.AD1[1]},
    {"lat": self.MM[0], "lon": self.MM[1]},
    {"lat": self.DC2[0], "lon": self.DC2[1]},
    {"lat": self.DD[0], "lon": self.DD[1]},
    {"lat": self.AD1[0], "lon": self.AD1[1]}]

        # self.fencelist3_4_g2 = [self.OO, self.AB2, self.AB3, self.DC3, self.DC2, self.AB2]

        self.fencelist3_4_g2 = [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AB2[0], "lon": self.AB2[1]},
    {"lat": self.AB3[0], "lon": self.AB3[1]},
    {"lat": self.DC3[0], "lon": self.DC3[1]},
    {"lat": self.DC2[0], "lon": self.DC2[1]},
    {"lat": self.AB2[0], "lon": self.AB2[1]}]

        # self.fencelist4_4_g1 = [self.OO, self.MM, self.BC1, self.CC, self.DC2, self.MM]

        self.fencelist4_4_g1 = [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.MM[0], "lon": self.MM[1]},
    {"lat": self.BC1[0], "lon": self.BC1[1]},
    {"lat": self.CC[0], "lon": self.CC[1]},
    {"lat": self.DC2[0], "lon": self.DC2[1]},
    {"lat": self.MM[0], "lon": self.MM[1]}]

        # self.fencelist4_4_g2 = [self.OO, self.AB3, self.BB, self.CC, self.DC3, self.AB3]

        self.fencelist4_4_g2 = [
    {"lat": self.OO[0], "lon": self.OO[1]},
    {"lat": self.AB3[0], "lon": self.AB3[1]},
    {"lat": self.BB[0], "lon": self.BB[1]},
    {"lat": self.CC[0], "lon": self.CC[1]},
    {"lat": self.DC3[0], "lon": self.DC3[1]},
    {"lat": self.AB3[0], "lon": self.AB3[1]}]


        if drone == "d1":
            # self.drone1 = dronev
            if g1selected:
                if self.Ndrones == "1":
                    self.fencelist_d1 = self.fencelist0

                if self.Ndrones == "2":
                    self.fencelist_d1 = self.fencelist1_2_g1

                if self.Ndrones == "3":
                    self.fencelist_d1 = self.fencelist1_3_g1

                if self.Ndrones == "4":
                    self.fencelist_d1 = self.fencelist1_4_g1


                self.client.publish("miMain/autopilotService/setGeofence", payload=json.dumps(self.fencelist_d1))
                self.client.publish("miMain/autopilotService/setParameters", payload=json.dumps(self.paramList))




            if g2selected:

                if self.Ndrones == "1":
                    self.fencelist_d1 = self.fencelist0

                if self.Ndrones == "2":
                    self.fencelist_d1 = self.fencelist1_2_g2

                if self.Ndrones == "3":
                    self.fencelist_d1 = self.fencelist1_3_g2

                if self.Ndrones == "4":
                    self.fencelist_d1 = self.fencelist1_4_g2


                self.client.publish("miMain/autopilotService/setGeofence", payload=json.dumps(self.fencelist_d1))
                self.client.publish("miMain/autopilotService/setParameters", payload=json.dumps(self.paramList))


            if gcustomselected:
                self.client.publish("miMain/autopilotService/setGeofence", payload=json.dumps(self.geof_design1[0]))
                self.client.publish("miMain/autopilotService/setParameters", payload=json.dumps(self.paramList))



        if drone == "d2":
            # self.drone2 = dronev

            if g1selected:

                if self.Ndrones == "1":
                    self.fencelist_d2 = self.fencelist0

                if self.Ndrones == "2":
                    self.fencelist_d2 = self.fencelist2_2_g1

                if self.Ndrones == "3":
                    self.fencelist_d2 = self.fencelist2_3_g1

                if self.Ndrones == "4":
                    self.fencelist_d2 = self.fencelist2_4_g1


                self.client.publish("miMain/autopilotService2/setGeofence", payload=json.dumps(self.fencelist_d2))
                self.client.publish("miMain/autopilotService2/setParameters", payload=json.dumps(self.paramList))


            if g2selected:
                if self.Ndrones == "1":
                    self.fencelist_d2 = self.fencelist0

                if self.Ndrones == "2":
                    self.fencelist_d2 = self.fencelist2_2_g2

                if self.Ndrones == "3":
                    self.fencelist_d2 = self.fencelist2_3_g2

                if self.Ndrones == "4":
                    self.fencelist_d2 = self.fencelist2_4_g2


                self.client.publish("miMain/autopilotService2/setGeofence", payload=json.dumps(self.fencelist_d2))
                self.client.publish("miMain/autopilotService2/setParameters", payload=json.dumps(self.paramList))


            if gcustomselected:
                self.client.publish("miMain/autopilotService2/setGeofence", payload=json.dumps(self.geof_design2[0]))
                self.client.publish("miMain/autopilotService2/setParameters", payload=json.dumps(self.paramList))


        if drone == "d3":
            # self.drone3 = dronev

            if g1selected:

                if self.Ndrones == "1":
                    self.fencelist_d3 = self.fencelist0

                if self.Ndrones == "3":
                    self.fencelist_d3 = self.fencelist3_3_g1

                if self.Ndrones == "4":
                    self.fencelist_d3 = self.fencelist3_4_g1


                self.client.publish("miMain/autopilotService3/setGeofence", payload=json.dumps(self.fencelist_d3))
                self.client.publish("miMain/autopilotService3/setParameters", payload=json.dumps(self.paramList))


            if g2selected:

                if self.Ndrones == "1":
                    self.fencelist_d3 = self.fencelist0

                if self.Ndrones == "3":
                    self.fencelist_d3 = self.fencelist3_3_g2

                if self.Ndrones == "4":
                    self.fencelist_d3 = self.fencelist3_4_g2


                self.client.publish("miMain/autopilotService3/setGeofence", payload=json.dumps(self.fencelist_d3))
                self.client.publish("miMain/autopilotService3/setParameters", payload=json.dumps(self.paramList))
                #

            if gcustomselected:
                self.client.publish("miMain/autopilotService3/setGeofence", payload=json.dumps(self.geof_design3[0]))
                self.client.publish("miMain/autopilotService3/setParameters", payload=json.dumps(self.paramList))




        if drone == "d4":
            # self.drone4 = dronev
            if g1selected:

                if self.Ndrones == "1":
                    self.fencelist_d4 = self.fencelist0

                if self.Ndrones == "4":
                    self.fencelist_d4 = self.fencelist4_4_g1


                self.client.publish("miMain/autopilotService4/setGeofence", payload=json.dumps(self.fencelist_d4))
                self.client.publish("miMain/autopilotService4/setParameters", payload=json.dumps(self.paramList))


            if g2selected:

                if self.Ndrones == "1":
                    self.fencelist_d4 = self.fencelist0

                if self.Ndrones == "4":
                    self.fencelist_d4 = self.fencelist4_4_g2


                self.client.publish("miMain/autopilotService4/setGeofence", payload=json.dumps(self.fencelist_d4))
                self.client.publish("miMain/autopilotService4/setParameters", payload=json.dumps(self.paramList))


            if gcustomselected:
                self.client.publish("miMain/autopilotService4/setGeofence", payload=json.dumps(self.geof_design4[0]))
                self.client.publish("miMain/autopilotService4/setParameters", payload=json.dumps(self.paramList))



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

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)










