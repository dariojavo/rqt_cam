#! /usr/bin/env python

# Code for requesting and publishing data for available cameras generated by cam_v4l2_node
import rospy
from ecam_v4l2.srv import *
from sensor_msgs.msg import Image
from ecam_v4l2.msg import image
import numpy as np
import cv2
from cv_bridge import CvBridge

def callback(data):

    #### direct conversion to CV2 ####
    np_arr = np.frombuffer(data.data, np.uint8).reshape(data.height, data.width, -1)
    im = cv2.cvtColor(np_arr, cv2.COLOR_YUV2BGR_UYVY) #COLOR_YUV2BGRA_UYVY (?) 
    
    #if im is not None:
        #print("Image successfully read")
        #print(im.shape)
        #cv2.imwrite('Example.png', im)
    br = CvBridge()
    pub.publish(br.cv2_to_imgmsg(im))

def callback1(data):

    #### direct conversion to CV2 ####
    np_arr = np.frombuffer(data.data, np.uint8).reshape(data.height, data.width, -1)
    im = cv2.cvtColor(np_arr, cv2.COLOR_YUV2BGR_UYVY) #COLOR_YUV2BGRA_UYVY (?) 
    
    #if im is not None:
        #print("Image successfully read")
        #print(im.shape)
        #cv2.imwrite('Example.png', im)
    br = CvBridge()
    pub1.publish(br.cv2_to_imgmsg(im))

def callback2(data):

    #### direct conversion to CV2 ####
    np_arr = np.frombuffer(data.data, np.uint8).reshape(data.height, data.width, -1)
    im = cv2.cvtColor(np_arr, cv2.COLOR_YUV2BGR_UYVY) #COLOR_YUV2BGRA_UYVY (?) 
    
    #if im is not None:
        #print("Image successfully read")
        #print(im.shape)
        #cv2.imwrite('Example.png', im)
    br = CvBridge()
    pub2.publish(br.cv2_to_imgmsg(im))

if __name__ == '__main__':

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('cameras_listener', anonymous=True)

    # wait for this sevice to be running
    rospy.wait_for_service('ChooseDevice')

    # Create the connection to the service. Remember it's a Trigger service
    camera_service = rospy.ServiceProxy('ChooseDevice', camera)

    # Create an object of the type TriggerRequest. We nned a TriggerRequest for a Trigger service
    req = cameraRequest()

    topics = rospy.get_published_topics()

    cameras = []
    for topic in topics:
        for words in topic:
            if  'See3CAM' in words:
                cameras.append(words)

    print('Detected cameras: ')
    print(cameras)

    # req.cam_name = 'See3CAM_24CUG_3C22940B'
    # req.shutdown = 0 # Flase for activation / True for shutdown

    # # Now send the request through the connection
    # camera_service(req)

    # Assuming 3 cameras of the same type See3CAM
    cont = 0
    for cam in cameras:
        req.cam_name = cam.replace('/','')
        req.shutdown = 0 # Flase for activation / True for shutdown
        # Now send the request through the connection
        camera_service(req)
        cont += 1
        if cont == 1:
            rospy.Subscriber(cam, image, callback)
            # This topic is created only for visualization purposes on field by using rqt_image_view
            pub = rospy.Publisher(cam.replace('/','') + '_view', Image, queue_size=10)
        elif cont ==2:
            rospy.Subscriber(cam, image, callback1)
            # This topic is created only for visualization purposes on field by using rqt_image_view
            pub1 = rospy.Publisher(cam.replace('/','') + '_view', Image, queue_size=10)
        elif cont == 3:
            rospy.Subscriber(cam, image, callback2)
            # This topic is created only for visualization purposes on field by using rqt_image_view
            pub2 = rospy.Publisher(cam.replace('/','') + '_view', Image, queue_size=10)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()