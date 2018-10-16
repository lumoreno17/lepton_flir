#!/usr/bin/env python

import rospy
import numpy 
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
import cv2
import PIL.Image, PIL.ImageTk
import Tkinter as tkinter

class GUI:
    def __init__(self, window, window_title):
        self.window = window
        self.window.geometry("1500x800")
        self.window.title(window_title)

        self.frame = tkinter.Frame(self.window, width=6*120, height=6*80+50)
        self.frame.pack()

        self.canvas_image = tkinter.Canvas(self.window, bg = 'green' , width = 5*80, height = 14*60)
        self.canvas_image.create_window((0,0), window=self.frame)
        self.canvas_image.place(relx=0.2, rely=0.5, anchor="c")

        tkinter.Label(self.canvas_image,text = "IR Camera", font=("Helvetica", 16)).place(relx = 0.5, rely = 0.15, anchor="c")
        tkinter.Label(self.canvas_image,text = "Binarized Image", font=("Helvetica", 16)).place(relx = 0.5, rely = 0.565, anchor="c")

        self.frame_data = numpy.zeros((300,400,3), dtype= numpy.uint8)

         
        rospy.Subscriber("processed_image", numpy_msg(Floats), self.image)
        rospy.init_node('teste_imagem')
        #rate = rospy.Rate(10) # 10hz
	#self.window.after(1, self.image)
	print "luciana"
	self.window.mainloop()

    def image(self,data):
        count = 0
        for k in range (0,300):
            for i in range (0,400):
                for j in range (0,3):
                    self.frame_data[k,i,j] = data.data[count]
                    count = count + 1

        self.im_detect = PIL.Image.frombytes('RGB', (self.frame_data.shape[1],self.frame_data.shape[0]), self.frame_data.astype('b').tostring())
        self.photo_detect = PIL.ImageTk.PhotoImage(image=self.im_detect)
        self.canvas_image.create_image(0, 150, image=self.photo_detect, anchor=tkinter.NW)
        #self.window.update()
	#self.window.after(1, self.image)

if __name__ == '__main__':
    GUI(tkinter.Tk(), "CAMERA")
    #rospy.spin()
