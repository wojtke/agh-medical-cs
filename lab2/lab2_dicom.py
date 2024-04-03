# AGH UST Medical Informatics 03.2021
# Lab 2 : DICOM
from tkinter import Tk, Canvas, NW

import numpy as np
import pydicom
from PIL import Image, ImageTk


class MainWindow:
    ds = pydicom.dcmread("head.dcm")
    data = ds.pixel_array

    def __init__(self, main):
        # print patient name

        print(self.ds.PatientName)

        # DONE: from ds get windowWidth and windowCenter

        self.winWidth = self.ds.WindowCenter
        self.winCenter = self.ds.WindowWidth

        # prepare canvas
        self.canvas = Canvas(main, width=512, height=512)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.init_window)
        self.canvas.bind("<B1-Motion>", self.update_window)
        self.canvas.bind("<Button-2>", self.init_measurement)
        self.canvas.bind("<B2-Motion>", self.update_measurement)
        self.canvas.bind("<ButtonRelease-2>", self.finish_measurement)

        # load image
        # todo: apply transform
        self.array = self.transform_data(self.data, self.winWidth, self.winCenter)
        self.array = self.data
        self.image = Image.fromarray(self.array)
        self.image = self.image.resize((512, 512), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(image=self.image, master=root)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.img)

        self.line = None
        self.text = None

    def transform_data(self, data, window_width, window_center):
        # print(f"Transforming data with window width: {window_width}, window center: {window_center}")
        # DONE: transform data (apply window width and center)
        img_min = window_center - window_width // 2
        img_max = window_center + window_width // 2
        windowed_img = np.clip(data, img_min, img_max)
        windowed_img = ((windowed_img - img_min) / (window_width - 1)) * 255
        return windowed_img.astype(np.uint8)

    def init_window(self, event):
        # print(f"Init window at x: {event.x}, y: {event.y}")
        # Save initial mouse position
        self.orig_mouse_x = event.x
        self.orig_mouse_y = event.y

        # Save the original window width and center for adjustments
        self.init_win_width = self.winWidth
        self.init_win_center = self.winCenter

    def update_window(self, event):
        # print(f"Update window at x: {event.x}, y: {event.y}")
        dx = event.x - self.orig_mouse_x
        dy = event.y - self.orig_mouse_y
        self.winWidth = max(1, self.init_win_width + dx)
        self.winCenter = self.init_win_center + dy

        self.array = self.transform_data(self.data, self.winWidth, self.winCenter)
        self.image = Image.fromarray(self.array).resize((512, 512), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(image=self.image, master=root)
        self.canvas.itemconfig(self.image_on_canvas, image=self.img)

    def init_measurement(self, event):
        # print(f"Init measurement at x: {event.x}, y: {event.y}")
        if self.line:
            self.canvas.delete(self.line)
        if self.text:
            self.canvas.delete(self.text)

        self.measure_start_x = event.x
        self.measure_start_y = event.y
        self.line = self.canvas.create_line(0, 0, 0, 0, fill="red", width=2)

    def update_measurement(self, event):
        # print(f"Update measurement at x: {event.x}, y: {event.y}")
        self.canvas.coords(self.line, self.measure_start_x, self.measure_start_y, event.x, event.y)

    def finish_measurement(self, event):
        # print(f"Finish measurement at x: {event.x}, y: {event.y}")
        dx = event.x - self.measure_start_x
        dy = event.y - self.measure_start_y
        distance_pixels = (dx**2 + dy**2) ** 0.5
        distance_mm = distance_pixels * self.ds.PixelSpacing[0]
        print(f"Measured Length: {distance_mm:.2f} mm")

        # write the measured length on the canvas in the line center
        center_x = (event.x + self.measure_start_x) // 2
        center_y = (event.y + self.measure_start_y) // 2
        self.text = self.canvas.create_text(center_x, center_y, text=f"{distance_mm:.2f} mm", fill="red")


if __name__ == "__main__":
    root = Tk()
    MainWindow(root)
    root.mainloop()
