# coding: utf-8

import os
import sys
import time
from threading import Lock, Thread

import cv2
import numpy as np

#import pyrealsense2 as rs
import urx
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
# from kivy.graphics import *
# from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
#from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper


class KinectView(App):

    def build(self):
        
        self.img1=Image(on_touch_down = self.on_press_image)
        self.root = layout = FloatLayout()
        layout.bind(size=self._update_rect, pos=self._update_rect)
        layout.add_widget(self.img1)
        Clock.schedule_interval(self.update_img1, 1/50)

        self.cameraSwitchButton = Button(text="Switch Camera Views", font_size=14, size_hint=(None, None), size=(180, 100), pos=(810, 200))
        self.cameraSwitchButton.bind(on_press=lambda x:self.on_press_cameraSwitchButton())
        layout.add_widget(self.cameraSwitchButton)

        self.pauseButton = Button(text="Stop", font_size=14, size_hint=(None, None), size=(180, 100), pos=(1100, 700))
        self.pauseButton.bind(on_press=lambda x:self.on_press_pauseButton())
        layout.add_widget(self.pauseButton)

        self.homeButton = Button(text="Home Position", font_size=14, size_hint=(None, None), size=(180, 100), pos=(1100, 525))
        self.homeButton.bind(on_press=lambda x:self.on_press_homeButton())
        layout.add_widget(self.homeButton)

        self.gripperButton = Button(text="Open Gripper", font_size=14, size_hint=(None, None), size=(180, 100), pos=(1100, 350))
        self.gripperButton.bind(on_press=lambda x:self.on_press_gripperButton())
        layout.add_widget(self.gripperButton)


        self.upButton = Button(background_normal="up.png", size_hint=(None, None), pos=(167, 530), border=(0, 0, 0, 0))
        self.upButton.bind(on_press=lambda x:self.on_press_upButton())
        layout.add_widget(self.upButton)

        self.downButton = Button(background_normal="down.png", size_hint=(None, None), pos=(300, 530), border=(0, 0, 0, 0))
        self.downButton.bind(on_press=lambda x:self.on_press_downButton())
        layout.add_widget(self.downButton)

        self.leftButton = Button(background_normal="left.png", size_hint=(None, None), size=(110, 70), pos=(150, 385), border=(0, 0, 0, 0))
        self.leftButton.bind(on_press=lambda x:self.on_press_leftButton())
        layout.add_widget(self.leftButton)

        self.rightButton = Button(background_normal="right.png", size_hint=(None, None), size=(110, 70), pos=(310, 385), border=(0, 0, 0, 0))
        self.rightButton.bind(on_press=lambda x:self.on_press_rightButton())
        layout.add_widget(self.rightButton)

        self.backwardButton = Button(background_normal="backward.png", size_hint=(None, None), size=(100, 50), pos=(235, 340), border=(0, 0, 0, 0))
        self.backwardButton.bind(on_press=lambda x:self.on_press_backwardButton())
        layout.add_widget(self.backwardButton)

        self.forwardButton = Button(background_normal="forward.png", size_hint=(None, None), size=(135, 91), pos=(216, 318), border=(0, 0, 0, 0))
        self.forwardButton.bind(on_press=lambda x:self.on_press_forwardButton())
        layout.add_widget(self.forwardButton)


        self.rzPlusButton = Button(background_normal="rz+.png", size_hint=(None, None), pos=(140, 300), size=(160, 120), border=(0, 0, 0, 0))
        self.rzPlusButton.bind(on_press=lambda x:self.on_press_rzPlusButton())
        layout.add_widget(self.rzPlusButton)
 
        self.rzMinusButton = Button(background_normal="rz-.png", size_hint=(None, None), pos=(290, 305), size=(160, 120), border=(0, 0, 0, 0))
        self.rzMinusButton.bind(on_press=lambda x:self.on_press_rzMinusButton())
        layout.add_widget(self.rzMinusButton)


        self.rxPlusButton = Button(background_normal="rx+.png", size_hint=(None, None), pos=(193, 182), size=(85, 85), border=(0, 0, 0, 0))
        self.rxPlusButton.bind(on_press=lambda x:self.on_press_rxPlusButton())
        layout.add_widget(self.rxPlusButton)


        self.rxMinusButton = Button(background_normal="rx-.png", size_hint=(None, None), pos=(313, 182), size=(90, 90), border=(0, 0, 0, 0))
        self.rxMinusButton.bind(on_press=lambda x:self.on_press_rxMinusButton())
        layout.add_widget(self.rxMinusButton)


        self.ryMinusButton = Button(background_normal="ry-.png", size_hint=(None, None), pos=(250, 245), size=(90, 90), border=(0, 0, 0, 0))
        self.ryMinusButton.bind(on_press=lambda x:self.on_press_ryMinusButton())
        layout.add_widget(self.ryMinusButton)


        self.ryPlusButton = Button(background_normal="ry+.png", size_hint=(None, None), pos=(252, 115), size=(90, 90), border=(0, 0, 0, 0))
        self.ryPlusButton.bind(on_press=lambda x:self.on_press_ryPlusButton())
        layout.add_widget(self.ryPlusButton)


        with layout.canvas.before:
            #Color(1, 1, 1, 1)
            #self.rect = Rectangle(size=layout.size, pos=layout.pos)
            time.sleep(1)
      
        return layout


    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


    def on_press_image(self, instance, touch):
        mouseX, mouseY = self.img1.to_widget(*touch.pos)
        print("Mouse Click: ", mouseX, mouseY)

        if IMAGE_X < mouseX < IMAGE_X+640 and IMAGE_Y < mouseY < IMAGE_Y+480:
            Thread(target=self.waypoint_thread, args=[mouseX, mouseY]).start()
        else:
            print("Mouse click out of range")

    def waypoint_thread(self, mouseX, mouseY):
        c, r = mouseX-IMAGE_X, 480-(mouseY-IMAGE_Y)
        print("$$$$$$$$$", c, r)
        #depth_value = depth_image[r][c]*depth_scale
        #depth_point = rs.rs2_deproject_pixel_to_point(aligned_depth_intrinsics, [c, r], depth_value)
        #camera_coordinates = np.array(depth_point)
        # robot_coordinates = np.dot(R, camera_coordinates.T).T+t
        # r_x, r_y, r_z = robot_coordinates[0], robot_coordinates[1], robot_coordinates[2]

        # rob.movel((r_x, r_y, r_z, 3, -1, 0), a, v) 
        
        time.sleep(0.2)


    def on_stop(self):
        #without this, app will not exit even if the window is closed
        #rob.close()
	    sys.exit()

    def on_press_cameraSwitchButton(self):
        Thread(target=self.camera_thread).start()


    def camera_thread(self):
        if self.cameraSwitchButton.text == "Open RGB-D Camera":
            self.cameraSwitchButton.text = "Close RGB-D Camera"
            Clock.schedule_interval(self.update_img1, 1/50)
        elif self.cameraSwitchButton.text == "Close RGB-D Camera":
            self.cameraSwitchButton.text = "Open RGB-D Camera"
            Clock.unschedule(self.update_img1)


    def on_press_pauseButton(self):
        Thread(target=self.pause_thread).start()

    def pause_thread(self):
        time.sleep(1)
        #rob.stopl()

    def on_press_homeButton(self):
        Thread(target=self.home_thread).start()

    def home_thread(self):
        #rob.movel((0.5, 0.4, 0.3, 3, -1, 0), a, v) 
        time.sleep(0.2)


    def on_press_gripperButton(self):
        Thread(target=self.gripper_thread).start()

    def gripper_thread(self):
        if self.gripperButton.text == "Open Gripper":
            self.gripperButton.text = "Close Gripper"
            #robotiqgrip = Robotiq_Two_Finger_Gripper(rob)
            #robotiqgrip.open_gripper()
        elif self.gripperButton.text == "Close Gripper":
            self.gripperButton.text = "Open Gripper"
            #robotiqgrip = Robotiq_Two_Finger_Gripper(rob)
            #robotiqgrip.close_gripper()

    def on_press_upButton(self):
        self.upButton.disabled=True
        Thread(target=self.move_thread, args=["up"]).start()

    def on_press_downButton(self):
        self.downButton.disabled=True
        Thread(target=self.move_thread, args=["down"]).start()

    def on_press_leftButton(self):
        self.leftButton.disabled=True
        Thread(target=self.move_thread, args=["left"]).start()

    def on_press_rightButton(self):
        self.rightButton.disabled=True
        Thread(target=self.move_thread, args=["right"]).start()

    def on_press_backwardButton(self):
        self.backwardButton.disabled=True
        Thread(target=self.move_thread, args=["backward"]).start()

    def on_press_forwardButton(self):
        self.forwardButton.disabled=True
        Thread(target=self.move_thread, args=["forward"]).start()

    def on_press_rzPlusButton(self):
        self.rzPlusButton.disabled=True
        Thread(target=self.rotate_thread, args=["rz+"]).start()

    def on_press_rzMinusButton(self):
        self.rzMinusButton.disabled=True
        Thread(target=self.rotate_thread, args=["rz-"]).start() 

    def on_press_rxPlusButton(self):
        self.rxPlusButton.disabled=True
        Thread(target=self.rotate_thread, args=["rx+"]).start() 

    def on_press_rxMinusButton(self):
        self.rxMinusButton.disabled=True
        Thread(target=self.rotate_thread, args=["rx-"]).start() 

    def on_press_ryPlusButton(self):
        self.ryPlusButton.disabled=True
        Thread(target=self.rotate_thread, args=["ry+"]).start() 

    def on_press_ryMinusButton(self):
        self.ryMinusButton.disabled=True
        Thread(target=self.rotate_thread, args=["ry-"]).start() 


    def move_thread(self, direction):
    #     rob_pos = rob.getl()
        
    #     rob_x, rob_y, rob_z = rob_pos[0], rob_pos[1], rob_pos[2]
    #     rob_pos = np.array([rob_x, rob_y, rob_z])
    #     camera_pos = np.dot(inversed_R, rob_pos.T).T + inversed_t
     
    #     cam_x, cam_y, cam_z = camera_pos[0], camera_pos[1], camera_pos[2]

    #     if direction == "up":
    #         camera_pos = np.array([cam_x, cam_y-MOVE_UNIT, cam_z])
    #         rob_pos = np.dot(R, camera_pos.T).T + t
    #         r_x, r_y, r_z = rob_pos[0], rob_pos[1], rob_pos[2]
            
            
    #     if direction == "down":
    #         camera_pos = np.array([cam_x, cam_y+MOVE_UNIT, cam_z])
    #         rob_pos = np.dot(R, camera_pos.T).T + t
    #         r_x, r_y, r_z = rob_pos[0], rob_pos[1], rob_pos[2]

    #     if direction == "left":
    #         camera_pos = np.array([cam_x-MOVE_UNIT, cam_y, cam_z])
    #         rob_pos = np.dot(R, camera_pos.T).T + t
    #         r_x, r_y, r_z = rob_pos[0], rob_pos[1], rob_pos[2]

    #     if direction == "right":
    #         camera_pos = np.array([cam_x+MOVE_UNIT, cam_y, cam_z])
    #         rob_pos = np.dot(R, camera_pos.T).T + t
    #         r_x, r_y, r_z = rob_pos[0], rob_pos[1], rob_pos[2]

    #     if direction == "forward":
    #         camera_pos = np.array([cam_x, cam_y, cam_z-MOVE_UNIT])
    #         rob_pos = np.dot(R, camera_pos.T).T + t
    #         r_x, r_y, r_z = rob_pos[0], rob_pos[1], rob_pos[2]

    #     if direction == "backward":
    #         camera_pos = np.array([cam_x, cam_y, cam_z+MOVE_UNIT])
    #         rob_pos = np.dot(R, camera_pos.T).T + t
    #         r_x, r_y, r_z = rob_pos[0], rob_pos[1], rob_pos[2]
            

    #     rob.movel((r_x, r_y, r_z, 3, -1, 0), a, v)
 
        self.upButton.disabled=False
        self.downButton.disabled=False
        self.leftButton.disabled=False
        self.rightButton.disabled=False
        self.backwardButton.disabled=False
        self.forwardButton.disabled=False


    def rotate_thread(self, direction):
        # rob_o = rob.get_orientation()
        # rob_pos = rob.getl()
        # rob_rx, rob_ry, rob_rz = rob_pos[3], rob_pos[4], rob_pos[5]

        if direction == "rz+":
            # rob_o.rotate_zb(rob_rz+ROTATE_UNIT)
            # rob.set_orientation(rob_o)
            print('rz+')

        elif direction == "rz-":
            # rob_o.rotate_zb(rob_rz-ROTATE_UNIT)
            # rob.set_orientation(rob_o)
            print('rz-')

        else:
            print("TBD")

        self.rzPlusButton.disabled=False
        self.rzMinusButton.disabled=False
        self.rxPlusButton.disabled=False    
        self.rxMinusButton.disabled=False
        self.ryPlusButton.disabled=False
        self.ryMinusButton.disabled=False

    
    def update_img1(self, dt):
        # global aligned_depth_intrinsics, depth_image

        # # Get frameset of color and depth
        # frames = pipeline.wait_for_frames()
        # # frames.get_depth_frame() is a 640x360 depth image

        # # Align the depth frame to color frame
        # aligned_frames = align.process(frames)

        # # Get aligned frames
        # aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        # color_frame = aligned_frames.get_color_frame()

        # aligned_depth_intrinsics = rs.video_stream_profile(aligned_depth_frame.profile).get_intrinsics()

        # depth_image = np.asanyarray(aligned_depth_frame.get_data())
        # color_image = np.asanyarray(color_frame.get_data())

        # colors = cv2.cvtColor(color_image, cv2.COLOR_BGRA2RGB)
   
        # #convert it to texture
        # texture1 = Texture.create(size=(colors.shape[1], colors.shape[0]), colorfmt='rgb')
        # texture1.flip_vertical()
        # #texture1.flip_horizontal()

        # texture1.blit_buffer(colors.tostring(), colorfmt='rgb', bufferfmt='ubyte')
        # # display image from the texture
        # #self.img1.texture = texture1

        with self.img1.canvas:
            time.sleep(1)
            # Rectangle(pos=(IMAGE_X,IMAGE_Y), size=(640, 480), texture=texture1)

        
         
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

  
# 0 being off 1 being on as in true / false 
# you can use 0 or 1 && True or False 
Config.set('graphics', 'resizable', '0') 
  
# fix the width of the window  
Config.set('graphics', 'width', '1500') 
Config.set('graphics', 'height', '600') 

v = 0.05
a = 0.01
#rob = urx.Robot("192.168.1.105")
#rob.set_tcp((0, 0, 0.18, 0, 0, 0))
time.sleep(0.2)

# Create a pipeline
# pipeline = rs.pipeline()

# #Create a config and configure the pipeline to stream
# #  different resolutions of color and depth streams
# config = rs.config()
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# # Start streaming
# profile = pipeline.start(config)
# aligned_depth_intrinsics = None
# depth_image=None

# # Getting the depth sensor's depth scale (see rs-align example for explanation)
# depth_sensor = profile.get_device().first_depth_sensor()
# depth_scale = depth_sensor.get_depth_scale()
# print("Depth Scale is: " , depth_scale)

# # Create an align object
# # rs.align allows us to perform alignment of depth frames to others frames
# # The "align_to" is the stream type to which we plan to align depth frames.
# align_to = rs.stream.color
# align = rs.align(align_to)


R = np.array([[0.4729613, -0.02498102, 0.88072899],
       [-0.88017677, 0.03193417, 0.47357054],
       [-0.03995563, -0.99917774, -0.00688409]])
t = np.array([-0.43179749, 0.24159906, 0.15602798])


inversed_R = np.array([[0.4729613, -0.88017677, -0.03995563],
       [-0.02498102, 0.03193417, -0.99917774],
       [0.88072899, 0.47357054, -0.00688409]])
inversed_t = np.array([0.42310757,  0.13739768,  0.26695648])

MOVE_UNIT = 0.01
ROTATE_UNIT = 0.08
IMAGE_X = 444
IMAGE_Y = 150

KinectView().run()
#cv2.destroyAllWindows()
