# AGH UST Medical Informatics 03.2021
# Lab 2 : DICOM

import pydicom
from tkinter import *
from PIL import Image, ImageTk

class MainWindow():

    ds = pydicom.dcmread("head.dcm")
    data = ds.pixel_array

    def __init__(self, main):
        # print patient name
        print(self.ds.PatientName)

        #todo: from ds get windowWidth and windowCenter

        # prepare canvas
        self.canvas = Canvas(main, width=512, height=512)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.init_window)
        self.canvas.bind("<B1-Motion>", self.update_window)
        self.canvas.bind("<Button-3>", self.init_measurement)
        self.canvas.bind("<B3-Motion>", self.update_measurement)
        self.canvas.bind("<ButtonRelease-3>", self.finish_measurement)

        # load image
        # todo: apply transform
        #self.array = self.transform_data(self.data, self.winWidth, self.winCenter)
        self.array = self.data
        self.image = Image.fromarray(self.array)
        self.image = self.image.resize((512, 512), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(image=self.image, master=root)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.img)

    def transform_data(self, data, window_width, window_center):
        # todo: transform data (apply window width and center)
        return data

    def init_window(self, event):
        # todo: save mouse position
        print("x: " + str(event.x) + " y: " + str(event.y))

    def update_window(self, event):
        # todo: modify window width and center
        print("x: " + str(event.x) + " y: " + str(event.y))
        #self.array2 = self.transform_data(self.data, self.winWidth, self.winCenter)
        #self.image2 = Image.fromarray(self.array2)
        #self.image2 = self.image2.resize((512, 512), Image.ANTIALIAS)
        #self.img2 = ImageTk.PhotoImage(image=self.image2, master=root)
        #self.canvas.itemconfig(self.image_on_canvas, image = self.img2)

    def init_measurement(self, event):
        # todo: save mouse position
        # todo: create line
        # hint: self.canvas.create_line(...)
        print("x: " + str(event.x) + " y: " + str(event.y))

    def update_measurement(self, event):
        # todo: update line
        # hint: self.canvas.coords(...)
        print("x: " + str(event.x) + " y: " + str(event.y))

    def finish_measurement(self, event):
        # todo: print measured length in mm
        print("x: " + str(event.x) + " y: " + str(event.y))



#----------------------------------------------------------------------

root = Tk()
MainWindow(root)
root.mainloop()
