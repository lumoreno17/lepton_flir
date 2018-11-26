#!/usr/bin/env python
#PKG = 'numpy_tutorial'
#import roslib; roslib.load_manifest(PKG)
import serial
import numpy 
import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats

com = serial.Serial('/dev/stmf4',baudrate = 921600)

frame_data = numpy.zeros(4800,dtype=numpy.float32)

def get_frame():
    pub = rospy.Publisher('lepton', numpy_msg(Floats), queue_size = 10)
    rospy.init_node('ir_camera', anonymous=True)
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        frame_aquisition_flag = 0
        while(frame_aquisition_flag !=1):
            if( int(com.read(1).encode('hex'),16) == 222):
                if( int(com.read(1).encode('hex'),16) == 173):
                    if( int(com.read(1).encode('hex'),16) == 190):
                        if( int(com.read(1).encode('hex'),16) == 239):

                            for i in range (0,4800):    
                                    frame_data[i] = int(com.read(2).encode('hex'),16)

                            frame_aquisition_flag = 1
        pub.publish(frame_data)
        r.sleep()

if __name__ == '__main__':
    try:
        get_frame()
    except rospy.ROSInterruptException:
        pass
