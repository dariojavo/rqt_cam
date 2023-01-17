#! /usr/bin/env python

# Code for requesting and publishing data for available cameras generated by cam_v4l2_node
import rospy
from ecam_v4l2.srv import *
from sensor_msgs.msg import Image
from ecam_v4l2.msg import image
import numpy as np
import cv2
from cv_bridge import CvBridge
import v4l2

if __name__ == '__main__':

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('cameras_parameters', anonymous=True)
    
    # # wait for this sevice to be running
    rospy.wait_for_service('SetControl')

    # Create the connection to the service. Remember it's a Trigger service
    set_camera_parameters = rospy.ServiceProxy('SetControl', set_control)

    A = set_controlRequest()

    A.cam_name = 'See3CAM_24CUG_062B930B'
    A.id = 9963777
    A.value = 25

    set_camera_parameters(A)

    # Create the connection to the service. Remember it's a Trigger service
    camera_parameters = rospy.ServiceProxy('QueryControl', query_control, persistent= True)
    
    # wait for this sevice to be running
    rospy.wait_for_service('QueryControl')
    
    # Create an object of the type TriggerRequest. We nned a TriggerRequest for a Trigger service
    req = query_controlRequest()

    topics = rospy.get_published_topics()

    cameras = []
    for topic in topics:
        for words in topic:
            if  'See3CAM' in words:
                cameras.append(words)

    print('Detected cameras: ')
    print(cameras)



    #while not rospy.is_shutdown(): 
    i=0
    while i < 15:
        i +=1   
        req.cam_name = 'See3CAM_24CUG_062B930B'
        req.id = 2147483648
        req.reqtype = 7
        req.index = 5
        a = camera_parameters.call(req)

        print(a)
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()