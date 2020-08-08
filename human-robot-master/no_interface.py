# coding: utf-8


import numpy as np
import cv2
import urx
import time
import sys
from threading import Thread, Lock

import pyrealsense2 as rs



def draw_circle(event, x, y, flags, param):
    global mouseX, mouseY, r_x, r_y, r_z, flag
    
    if event == cv2.EVENT_LBUTTONDBLCLK:
        mouseX, mouseY = x, y
        print("mouseX", mouseX, "mouseY", mouseY)
        depth_value = depth_image[mouseY][mouseX]*depth_scale
        print("Depth at the mouse click: ", depth_value)
        depth_point = rs.rs2_deproject_pixel_to_point(aligned_depth_intrinsics, [mouseX, mouseY], depth_value)
        print("3D depth point: ", depth_point)
        camera_coordinates = np.array(depth_point)
        robot_coordinates = np.dot(R, camera_coordinates.T).T+t
        r_x, r_y, r_z = robot_coordinates[0], robot_coordinates[1], robot_coordinates[2]
        print("robot coordinates: ", r_x, r_y, r_z)
        flag = True


def robot():
    global flag

    while True:
        if mouseY != -10000 and mouseX != -10000 and flag:
            rob.movel((0.5, 0.4, 0.3, 3, -1, 0), a, v)
            rob.movel((r_x, r_y, r_z, 3, -1, 0), a, v) 
            rob.movel((0.5, 0.4, 0.3, 3, -1, 0), a, v) 
            flag = False      

            


def video():
    while True:
        global aligned_depth_intrinsics, depth_image

        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        color_frame = aligned_frames.get_color_frame()
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image


        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        aligned_depth_intrinsics = rs.video_stream_profile(aligned_depth_frame.profile).get_intrinsics()

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        cv2.imshow('color image', color_image)
        cv2.setMouseCallback("color image",  draw_circle)

        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break



v = 0.05
a = 0.01
rob = urx.Robot("192.168.1.105")
rob.set_tcp((0, 0, 0.18, 0, 0, 0))

# Create a pipeline
pipeline = rs.pipeline()

#Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)



mouseX = -10000
mouseY = -10000
flag = False
depth_image = None
aligned_depth_intrinsics = None
r_x, r_y, r_z = None, None, None

R = np.array([[0.4729613, -0.02498102, 0.88072899],
       [-0.88017677, 0.03193417, 0.47357054],
       [-0.03995563, -0.99917774, -0.00688409]])
t = np.array([-0.43179749, 0.24159906, 0.15602798])

time.sleep(0.2)


t1 = Thread(target=video)
t1.start()
t2 = Thread(target=robot)
t2.start()


#('mouseX', 422, 'mouseY', 277)
#('Depth at the mouse click: ', 0.9570000454550609)
#('3D depth point: ', [0.1449321210384369, 0.053613416850566864, 0.9570000171661377])
#('robot coordinates: ', 0.47826813508819932, 0.56895228871250347, 0.090079718866072453)



