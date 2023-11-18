# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 09:32:39 2023

@author: L.Lentz@umwelt-campus.de
"""


import tkinter as tk 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2 as cv2
import PIL.Image, PIL.ImageTk
from tkinter import filedialog as fd



class Application(tk.Frame):
    #
    #
    def __init__(self, master=None):
        #
        tk.Frame.__init__(self,master)
        #
        #
        self.get_image()
        self.create_widgets()
        self.update_image()
        #
         #
    #
    def create_canvas(self):
        #
        self.canvas = tk.Canvas(master=self.fig_frame, width = self.img_width, height = self.img_height)
        self.canvas.grid(row=0,column=0) 
    #
    #
    def create_widgets(self):
        #
        self.create_frames()
        self.create_canvas()
        self.create_hsv_buttons()
        self.create_hc_buttons()
        self.create_radios()
    #
    #
    def create_frames(self):
        #
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=0,column=0,padx=(30,25))
        #
        self.fig_frame = tk.Frame(root)
        self.fig_frame.grid(row=0,column=1, padx = 10)
        #
        self.right_button_frame = tk.Frame(root)
        self.right_button_frame.grid(row=0,column=2, padx = 10)
        #
        self.bottom_button_frame = tk.Frame(root)
        self.bottom_button_frame.grid(row=1,column=1, padx = 10, pady = 10)
    #
    #
    def create_hsv_buttons(self):
        #
        vals= (0,0,0,255,0,255)
        #Sliders
        self.myslider_1 = MySlider(self.button_frame,0,179,1,'H_min')
        self.myslider_1.set(vals[0])
        self.myslider_1.scale.bind("<ButtonRelease-1>", lambda x: self.update_mask())
        self.myslider_1.frame.grid(row=0)
        #
        self.myslider_2 = MySlider(self.button_frame,0,179,1,'H_max')
        self.myslider_2.set(vals[1])
        self.myslider_2.scale.bind("<ButtonRelease-1>", lambda x: self.update_mask())
        self.myslider_2 .frame.grid(row=1,pady=(0,10))
        #
        self.myslider_3 = MySlider(self.button_frame,0,255,1,'S_min')
        self.myslider_3.set(vals[2])
        self.myslider_3.scale.bind("<ButtonRelease-1>", lambda x: self.update_mask())
        self.myslider_3.frame.grid(row=2)
        #
        self.myslider_4 = MySlider(self.button_frame,0,255,1,'S_max')
        self.myslider_4.set(vals[3])
        self.myslider_4.scale.bind("<ButtonRelease-1>", lambda x: self.update_mask())
        self.myslider_4.frame.grid(row=3)
        #
        self.myslider_5 = MySlider(self.button_frame,0,255,1,'V_min')
        self.myslider_5.set(vals[4])
        self.myslider_5.scale.bind("<ButtonRelease-1>", lambda x: self.update_mask())
        self.myslider_5.frame.grid(row=4)
        #
        self.myslider_6 = MySlider(self.button_frame,0,255,1,'V_max')
        self.myslider_6.set(vals[5])
        self.myslider_6.scale.bind("<ButtonRelease-1>", lambda x: self.update_mask())
        self.myslider_6.frame.grid(row=5)
        #
    #
    #
    def create_hc_buttons(self):
        #
        vals= (3,10,150,90,0,300)
        #Sliders
        self.myslider_7 = MySlider(self.right_button_frame,0,20,1,'ratio')
        self.myslider_7.set(vals[0])
        self.myslider_7.scale.bind("<ButtonRelease-1>", lambda x: self.update_circles())
        self.myslider_7.frame.grid(row=0)
        #
        self.myslider_8 = MySlider(self.right_button_frame,0,100,1,'dist')
        self.myslider_8.set(vals[1])
        self.myslider_8.scale.bind("<ButtonRelease-1>", lambda x: self.update_circles())
        self.myslider_8.frame.grid(row=1,pady=(0,10))
        #
        self.myslider_9 = MySlider(self.right_button_frame,0,200,1,'Parameter 1')
        self.myslider_9.set(vals[2])
        self.myslider_9.scale.bind("<ButtonRelease-1>", lambda x: self.update_circles())
        self.myslider_9.frame.grid(row=2)
        #
        self.myslider_10 = MySlider(self.right_button_frame,0,200,1,'Parameter 2')
        self.myslider_10.set(vals[3])
        self.myslider_10.scale.bind("<ButtonRelease-1>", lambda x: self.update_circles())
        self.myslider_10.frame.grid(row=3)
        #
        self.myslider_11 = MySlider(self.right_button_frame,0,200,1,'r min')
        self.myslider_11.set(vals[4])
        self.myslider_11.scale.bind("<ButtonRelease-1>", lambda x: self.update_circles())
        self.myslider_11.frame.grid(row=4)
        #
        self.myslider_12 = MySlider(self.right_button_frame,0,1000,1,'r max')
        self.myslider_12.set(vals[5])
        self.myslider_12.scale.bind("<ButtonRelease-1>", lambda x: self.update_circles())
        self.myslider_12.frame.grid(row=5)
        #
        #
    #
    #
    def create_radios(self):
        #
        self.radiobutton_variable = tk.IntVar()
        self.radiobutton_variable.set(2)
        #
        self.radio_1 = tk.Radiobutton(self.bottom_button_frame,text="Maske",variable = self.radiobutton_variable, value = 1)
        self.radio_1.grid(row=0,column=0,padx=(10,10))
        #
        self.radio_2 = tk.Radiobutton(self.bottom_button_frame,text="Original",variable = self.radiobutton_variable, value = 2)
        self.radio_2.grid(row=0,column=1,padx=(10,10))
        #
        self.checkbutton_variable = tk.IntVar()
        self.checkbutton_variable.set(0)
        #
        self.check_1 = tk.Checkbutton(self.bottom_button_frame,text="Update Circles",variable = self.checkbutton_variable,offvalue=0,onvalue=1)
        self.check_1.grid(row=0,column=2,padx=(10,10))
        #
        self.imgbutton = tk.Button(self.bottom_button_frame,text="Change Image",width=15)
        self.imgbutton.bind("<ButtonRelease-1>", lambda x: self.change_image())
        self.imgbutton.grid(row=0,column=3,padx=(10,10))
        #
        self.imgsavebutton = tk.Button(self.bottom_button_frame,text="Save Image",width=15)
        self.imgsavebutton.bind("<ButtonRelease-1>", lambda x: self.save_image())
        self.imgsavebutton.grid(row=1,column=3,padx=(10,10))
        #
        #
        self.restorebutton = tk.Button(self.bottom_button_frame,text="Restore Parameter",width=15)
        self.restorebutton.bind("<ButtonRelease-1>", lambda x: self.restore_parameter())
        self.restorebutton.grid(row=0,column=4,padx=(10,10))
        #
        self.savebutton = tk.Button(self.bottom_button_frame,text="Save Parameter",width=15)
        self.savebutton.bind("<ButtonRelease-1>", lambda x: self.save_parameter())
        self.savebutton.grid(row=1,column=4,padx=(10,10))
        #
        #
        #
    #
    #
    def get_image(self):
        img_file_name = fd.askopenfilename()
        #init_dir = "C:\SeafileContainer\Seafile\Meine Bibliothek\Fritsch\Fritsch_Lentz_PK\Videos Fritsch Versuche\Bild_Analyse"
        #img_file_name = tk.filedialog.askopenfilename(initialdir = init_dir, filetypes = [('pictures' , '*.png')])
        img = cv2.cvtColor(cv2.imread(img_file_name), cv2.COLOR_BGR2RGB)
        img_height, img_width, self.img_no_channels = img.shape
        self.img_width = 500
        self.img_height = int(img_height*self.img_width/img_width)
        self.original_img = cv2.resize(img, (self.img_width, self.img_height))  
        self.img = self.original_img.copy()    
    #
    #
    def show_image(self,this_img):   
        pil_img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(this_img)) 
        self.canvas.create_image(0, 0, image = pil_img, anchor=tk.NW)
        self.canvas.image = pil_img
    #
    #
    def update_image(self):
        self.show_image(self.img)  
    #
    #
    def change_image(self):
        self.get_image()  
        self.update_mask()
    #
    #
    def save_image(self):
        file_name = fd.asksaveasfilename(filetypes=[("png file", ".png")],defaultextension=".png")  
        cv2.imwrite(file_name,self.img)
    #
    #
    def update_display(self):
        if self.radiobutton_variable.get() == 1:
            self.img =  cv2.cvtColor(self.mask.copy(), cv2.COLOR_GRAY2RGB) 
        elif self.radiobutton_variable.get() == 2:
            self.img = cv2.bitwise_and(self.original_img ,self.original_img , mask= self.mask)
    #
    #
    def update_mask(self):
        self.mask = self.get_mask(self.original_img)
        if self.checkbutton_variable.get() == 1:
            self.update_circles()
        else:
            self.update_display() 
            self.update_image()  
    #
    #
    def get_mask(self, this_img):
        low = (self.myslider_1.get(),self.myslider_3.get(),self.myslider_5.get())
        high = (self.myslider_2.get(),self.myslider_4.get(),self.myslider_6.get()) 
        img_hsv = cv2.cvtColor(this_img, cv2.COLOR_RGB2HSV)
        return cv2.inRange(img_hsv,low,high) 
    #
    #
    def update_circles(self):
        circles = self.get_circles()
        if circles is not None:
            self.update_display()
            self.draw_circles(self.img, circles)
            self.update_image()
    #
    #
    def get_circles(self):
        rmin = int(self.myslider_11.get())
        rmax = int(self.myslider_12.get())
        #
        circles = cv2.HoughCircles(self.mask, cv2.HOUGH_GRADIENT, self.myslider_7.get(), self.myslider_8.get(), param1=self.myslider_9.get(), param2=self.myslider_10.get(), minRadius=rmin, maxRadius=rmax)
        if circles is None:
            print("no circles found")
            self.update_display() 
            self.update_image() 
        else:
            circles = [np.uint16(np.around(circle)) for circle in circles[0, :] if rmin < circle[2] < rmax]
            print( str(len(circles)) + " circle(s) found")
            if len(circles)==1:
                print(circles)
        return circles
    #
    #
    def draw_circles(self, this_img, circles):
        for circle in circles:
            center = (circle[0], circle[1])
            radius = circle[2]
            cv2.circle(this_img, center, 1, (0, 100, 100), 3)
            cv2.circle(this_img, center, radius, (255, 0, 255), 3)
        #cv2.circle(this_img, (100,100), 100, (0, 100, 100), 5)
    #
    #
    def save_parameter(self):
        parameter_file_name = fd.asksaveasfilename(filetypes=[("txt file", ".txt")],defaultextension=".txt")
        parameter_file = open(parameter_file_name,"w")
        for i in range(1,13):
            parameter_file.write(str(int(eval("self.myslider_"+str(i)+".get()")))+"\n")
        parameter_file.close()
    #
    #
    def restore_parameter(self):
        parameter_file_name = fd.askopenfilename(filetypes=[("txt file", ".txt")],defaultextension=".txt")
        parameter_file = open(parameter_file_name,"r")
        for i in range(1,13):
            eval("self.myslider_"+str(i)+".set(parameter_file.readline())") 
        parameter_file.close()
        self.update_circles()
    #
    #
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # 
class MySlider():
    #
    def __init__(self,master,t_min,t_max,res,text):
        #
        #
        self.t_min = t_min
        self.t_max = t_max
        self.res = res
        #
        self.value = tk.DoubleVar()
        #  
        self.frame = tk.Frame(master)
        #
        tk.Label(self.frame, text = text).grid(row=0, column=1, sticky="W")
        tk.Button(self.frame, text = u"\u25C0", command = self.decrement).grid(row = 1, column = 0)
        tk.Button(self.frame, text = u"\u25B6", command = self.increment).grid(row = 1, column = 2)
        #
        self.scale = tk.Scale(master=self.frame, from_ = self.t_min, to=self.t_max, resolution = self.res, orient = tk.HORIZONTAL, variable = self.value)
        self.scale.grid(row = 1, column = 1, pady = (0,0), padx = (0,0))
        #
    #
    #
    def get(self):
        return self.value.get()   
     #
    #
    def set(self,value):
        self.value.set(value) 
    #
    #
    def increment(self):
        self.value.set(self.value.get()+self.res)
    #
    #    
    def decrement(self):
        self.value.set(self.value.get()-self.res)
    #
    #
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #
root=tk.Tk()
root.title("HSV-Filter")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
app=Application(master=root)
app.mainloop()