# coding: utf-8

import sys
import time
from threading import Lock, Thread

import cv2
import numpy as np

#import pyrealsense2 as rs
import urx
from kivy.clock import Clock
from kivy.graphics import *
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
#from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
import os
from kivy.config import Config
# to use buttons:
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen



class ManualInterface(FloatLayout):
    # runs on initialization
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
       
        self.screenSwitchButton = Button(text="Switch to Supervisory", font_size=14, size_hint=(None, None), size=(180, 100), pos=(1510, 150))
        self.screenSwitchButton.bind(on_press=self.on_press_screenSwitchButton)
        self.add_widget(self.screenSwitchButton)
       
        self.cameraSwitchButton = Button(text="Switch Camera Views", font_size=14, size_hint=(None, None), size=(180, 100), pos=(1210, 150))
        self.cameraSwitchButton.bind(on_press=self.on_press_cameraSwitchButton)
        self.add_widget(self.cameraSwitchButton)
       
        self.HomeButton = Button(text="Home", font_size=14, size_hint=(None, None), size=(180, 100), pos=(200, 150))
        self.HomeButton.bind(on_press=self.on_press_HomeButton)
        self.add_widget(self.HomeButton)

        self.stopButton = Button(text="Stop", font_size=14, size_hint=(None, None), size=(180, 100), pos=(1600, 500))
        self.stopButton.bind(on_press=self.on_press_stopButton)
        self.add_widget(self.stopButton)

        self.startButton = Button(text="Start", font_size=14, size_hint=(None, None), size=(180, 100), pos=(1600, 325))
        self.startButton.bind(on_press=self.on_press_startButton)
        self.add_widget(self.startButton)

        self.gripperButton = Button(text="Open Gripper", font_size=14, size_hint=(None, None), size=(180, 100), pos=(1600, 850))
        self.gripperButton.bind(on_press=self.on_press_gripperButton)
        self.add_widget(self.gripperButton)
       
        self.upButton = Button(background_normal="up.png", size_hint=(None, None), pos=(167, 930), border=(0, 0, 0, 0))
        self.upButton.bind(on_press=self.on_press_upButton)
        self.add_widget(self.upButton)

        self.downButton = Button(background_normal="down.png", size_hint=(None, None), pos=(300, 930), border=(0, 0, 0, 0))
        self.downButton.bind(on_press=self.on_press_downButton)
        self.add_widget(self.downButton)

        self.leftButton = Button(background_normal="left.png", size_hint=(None, None), size=(110, 70), pos=(150, 785), border=(0, 0, 0, 0))
        self.leftButton.bind(on_press=self.on_press_leftButton)
        self.add_widget(self.leftButton)

        self.rightButton = Button(background_normal="right.png", size_hint=(None, None), size=(110, 70), pos=(310, 785), border=(0, 0, 0, 0))
        self.rightButton.bind(on_press=self.on_press_rightButton)
        self.add_widget(self.rightButton)

        self.backwardButton = Button(background_normal="backward.png", size_hint=(None, None), size=(100, 50), pos=(235, 840), border=(0, 0, 0, 0))
        self.backwardButton.bind(on_press=self.on_press_backwardButton)
        self.add_widget(self.backwardButton)

        self.forwardButton = Button(background_normal="forward.png", size_hint=(None, None), size=(135, 91), pos=(216, 718), border=(0, 0, 0, 0))
        self.forwardButton.bind(on_press=self.on_press_forwardButton)
        self.add_widget(self.forwardButton)


        self.rzPlusButton = Button(background_normal="rz+.png", size_hint=(None, None), pos=(140, 500), size=(160, 120), border=(0, 0, 0, 0))
        self.rzPlusButton.bind(on_press=self.on_press_rzPlusButton)
        self.add_widget(self.rzPlusButton)
 
        self.rzMinusButton = Button(background_normal="rz-.png", size_hint=(None, None), pos=(290, 505), size=(160, 120), border=(0, 0, 0, 0))
        self.rzMinusButton.bind(on_press=self.on_press_rzMinusButton)
        self.add_widget(self.rzMinusButton)


        self.rxPlusButton = Button(background_normal="rx+.png", size_hint=(None, None), pos=(193, 382), size=(85, 85), border=(0, 0, 0, 0))
        self.rxPlusButton.bind(on_press=self.on_press_rxPlusButton)
        self.add_widget(self.rxPlusButton)


        self.rxMinusButton = Button(background_normal="rx-.png", size_hint=(None, None), pos=(313, 382), size=(90, 90), border=(0, 0, 0, 0))
        self.rxMinusButton.bind(on_press=self.on_press_rxMinusButton)
        self.add_widget(self.rxMinusButton)


        self.ryMinusButton = Button(background_normal="ry-.png", size_hint=(None, None), pos=(250, 445), size=(90, 90), border=(0, 0, 0, 0))
        self.ryMinusButton.bind(on_press=self.on_press_ryMinusButton)
        self.add_widget(self.ryMinusButton)


        self.ryPlusButton = Button(background_normal="ry+.png", size_hint=(None, None), pos=(252, 315), size=(90, 90), border=(0, 0, 0, 0))
        self.ryPlusButton.bind(on_press=self.on_press_ryPlusButton)
        self.add_widget(self.ryPlusButton)

       
    def on_press_screenSwitchButton(self, instance):
       
        ur_app.screen_manager.current = 'supervisory'
   
    def on_press_cameraSwitchButton(self, instance):
        time.sleep(0.1)


    def camera_thread(self, instance):
        time.sleep(0.1)


    def on_press_stopButton(self, instance):
        time.sleep(0.1)
       
    def on_press_startButton(self, instance):
        time.sleep(0.1)

    def pause_thread(self, instance):
        time.sleep(0.1)

    def on_press_startButton(self, instance):
        time.sleep(0.1)
       
    def on_press_HomeButton(self, instance):
        time.sleep(0.1)

    def home_thread(self, instance):
        #rob.movel((0.5, 0.4, 0.3, 3, -1, 0), a, v)
        time.sleep(0.1)


    def on_press_gripperButton(self, instance):
        time.sleep(0.1)

    def gripper_thread(self):
        Thread(target=self.gripper_thread).start()
        if self.gripperButton.text == "Open Gripper":
            self.gripperButton.text = "Close Gripper"
            #robotiqgrip = Robotiq_Two_Finger_Gripper(rob)
            #robotiqgrip.open_gripper()
        elif self.gripperButton.text == "Close Gripper":
            self.gripperButton.text = "Open Gripper"
            #robotiqgrip = Robotiq_Two_Finger_Gripper(rob)
            #robotiqgrip.close_gripper()

    def on_press_upButton(self, instance):
        time.sleep(0.1)

    def on_press_downButton(self, instance):
        time.sleep(0.1)

    def on_press_leftButton(self, instance):
        time.sleep(0.1)

    def on_press_rightButton(self, instance):
        time.sleep(0.1)

    def on_press_backwardButton(self, instance):
        time.sleep(0.1)

    def on_press_forwardButton(self, instance):
        time.sleep(0.1)

    def on_press_rzPlusButton(self, instance):
        time.sleep(0.1)

    def on_press_rzMinusButton(self, instance):
        time.sleep(0.1)

    def on_press_rxPlusButton(self, instance):
        time.sleep(0.1)

    def on_press_rxMinusButton(self, instance):
        time.sleep(0.1)

    def on_press_ryPlusButton(self, instance):
        time.sleep(0.1)

    def on_press_ryMinusButton(self, instance):
        time.sleep(0.1)        
       


# Simple information/error page
class SupervisoryInterface(FloatLayout):
    # runs on initialization
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.join = Button(text="go back", font_size=14, size_hint=(None, None), size=(180, 100), pos=(1010, 550))
        self.join.bind(on_press=self.join_button)
        self.add_widget(Label())  # just take up the spot.
        self.add_widget(self.join)

    def join_button(self, instance):
       
        ur_app.screen_manager.current = 'manual'

class EpicApp(App):
    def build(self):
   
        self.screen_manager = ScreenManager()
       
        self.manual_interface = ManualInterface()
        screen = Screen(name='manual')
        screen.add_widget(self.manual_interface)
        self.screen_manager.add_widget(screen)
       
       

        self.supervisory_interface = SupervisoryInterface()
        screen = Screen(name='supervisory')
        screen.add_widget(self.supervisory_interface)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

os.environ['KIVY_GL_BACKEND'] = 'sdl2'

 
# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', '0')
 
# fix the width of the window  
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')

if __name__ == "__main__":
    ur_app = EpicApp()
    ur_app.run()