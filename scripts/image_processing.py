#!/usr/bin/env python

import rospy
import numpy 
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import Int32
#from matplotlib import pyplot as plt
import cv2

pub = rospy.Publisher('processed_image', numpy_msg(Floats), queue_size = 10)
pub2 = rospy.Publisher('hotspot_count', Int32, queue_size = 10)
rospy.init_node('image_processing')
array_data = numpy.zeros(360000,dtype=numpy.float32)
hotspot_detection = Int32()

def callback(data):
	frame_data = numpy.zeros((60,80), dtype= numpy.uint8)
	count=0
	vmax = 8400
	vmin = 7600
	for i in range (0,60):
		for j in range (0,80):
			frame_data[i, j] = (data.data[count]-vmin)*120/(vmax-vmin)
			count = count + 1
	print numpy.size(frame_data,1)
	print numpy.size(frame_data,0)
	print frame_data[0,0]

	#Redimensiona a imagem para ser melhor visualizada
	frame_data = cv2.resize(frame_data,(5*80,5*60), interpolation = cv2.INTER_CUBIC)
	
	#Realiza um blur na imagem para remover alta frequencia
	blurred = cv2.GaussianBlur(frame_data, (15, 15), 0)

	#Realiza um threshold para revelar os pontos quentes
	thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)[1]

	# Realiza uma serie de erosoes e dilatacoes para remover ruido da imagem binarizada
	thresh = cv2.erode(thresh, None, iterations=1)
	thresh = cv2.dilate(thresh, None, iterations=9)
	
	#Procura os contornos brancos na imagem binarizada e printa a quantidade
	im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	print (len(contours))
	hotspot_detection = len(contours)	
	frame_data = cv2.cvtColor(frame_data, cv2.COLOR_GRAY2RGB)

	print(len(frame_data[:]))
	print(len(frame_data[1,:]))

	#Desenha os contornos na imagem original
	#cv2.drawContours(frame_data, contours, -1, (255,0,0), 2)

	for c in contours:
		if cv2.contourArea(c) < 3000:
			continue

		## BEGIN - draw rotated rectangle
		rect = cv2.minAreaRect(c)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		cv2.drawContours(frame_data,[box],0,(0,191,255),2)
	
	count = 0
	for k in range (0,300):
		for i in range (0,400):
			for j in range (0,3):
				array_data[count] = frame_data[k,i,j]
				count = count+1
	
	print array_data
	pub.publish(array_data)
	pub2.publish(hotspot_detection)
	#plt.imshow(frame_data)
	#plt.show()	

def image_processing():
	rospy.Subscriber("lepton", numpy_msg(Floats), callback)
	rate = rospy.Rate(10) # 10hz
	rospy.spin()

if __name__ == '__main__':
    image_processing()
