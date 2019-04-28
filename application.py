#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import gi, os, sys, time
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk, GLib, Gdk, Gio, GObject, WebKit
from gpiozero import LED
from sense_hat import SenseHat
from datetime import datetime
from gps import *
from time import *
import time
import threading

# Name of the module "Digital to Analog" : MCP3008

GLADE_FILE = "interface.glade"

# pin definitions
ledPin = 20
ventPin = 21
#batteryPin = UNDEFINED

# setup GPIO: BCM
GPIO.setmode(GPIO.BCM) # Broadcom numbering system
GPIO.setwarnings(False)

# setup GPIO input / output
GPIO.setup(ledPin, GPIO.OUT)
#GPIO.setup(ventPin, GPIO.OUT)
#GPIO.setup(batteryPin, GPIO.IN)

# Initialise outputs as LOW
#GPIO.output(ledPin, GPIO.LOW)
#GPIO.output(ventPin, GPIO.LOW)

# Global variables definition
state_LED = "OFF"
state_vent = "OFF"

gpsd = None #seting the global variable

global temperature
global pressure
global humidity
global altitude
global speed

language = "EN"

def map(x, inLo, inHi, outLo, outHi):
    inRange = inHi - inLo
    outRange = outHi - outLo
    inScale = (x - inLo) / inRange
    return outLo + (inScale * outRange)

class Handler:
    def on_button_led_clicked(self, button):
        global state_LED

        # If we have clicked the button AND the LED was switched OFF
        if state_LED == "OFF":
            GPIO.output(ledPin, GPIO.HIGH)
            state_LED = "ON"
            print("LED:", state_LED)
            
            button.set_label("LED: ON")
            image = Gtk.Image()
            image.set_from_file("on.png")
            button.set_image(image)                       
        else:
            GPIO.output(ledPin, GPIO.LOW)
            state_LED = "OFF"
            print("LED:", state_LED)
            
            button.set_label("LED: OFF")
            image = Gtk.Image()
            image.set_from_file("off.png")
            button.set_image(image)
            
    def on_button_vent_clicked(self, button):
        global state_vent
        
        if state_vent == "OFF":
            #GPIO.output(ventPin, GPIO.HIGH)
            state_vent = "ON"
            print("Ventilation:", state_vent)
            
            button.set_label("Ventilation: ON")
            image = Gtk.Image()
            image.set_from_file("on.png")
            button.set_image(image)
            #image.set_from_stock(Gtk.STOCK_NO, Gtk.IconSize.BUTTON)
        else:
            #GPIO.output(ventPin, GPIO.LOW)
            state_vent = "OFF"
            print("Ventilation:", state_vent)
            
            button.set_label("Ventilation: OFF")
            image = Gtk.Image()
            image.set_from_file("off.png")
            button.set_image(image)
            #image.set_from_stock(Gtk.STOCK_YES, Gtk.IconSize.BUTTON)
    
    def on_button_settings_clicked(self, button):
        #settings = setting()
        print("Setting")
    
    def on_interface_destroy(self, *args):
        print("Exit application")
        gpsp.running = False
        gpsp.join() # wait for the thread to finish what it's doing
        GPIO.cleanup()

class GpsPoller(threading.Thread):
    def __init__(self):
        try:
            threading.Thread.__init__(self)
        
            global gpsd #bring it in scope
            
            gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
            self.current_value = None
            self.running = True #setting the thread running to true
        except:
            print("Problem with the GPS. Error #1: GpsPoller init")

    def run(self):
        try:
            global gpsd
            
            while gpsp.running:
                gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
        except:
            print("Problem with the GPS. Error #2: GpsPoller run")
      
class Application:
    def __init__(self):
        global gpsp
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(GLADE_FILE)
        self.builder.connect_signals(Handler())
        
        #self.viewer = self.builder.get_object("panel_window_gps")
        #self.webview = WebKit.WebView()
        #self.viewer.add(self.webview)
        #self.webview.show()  
        #self.webview.open("https://maps.google.com")
        
        #self.viewer = self.builder.get_object("panel_window_youtube")
        #self.webview = WebKit.WebView()
        #self.viewer.add(self.webview)
        #self.webview.show()  
        #self.webview.open("https://www.youtube.com")
        
        try:
            gpsp = GpsPoller() # create the thread
            gpsp.start() # start it up
        except:
            print("Problem with the GPS. Error #3: Application init")
            
        window = self.builder.get_object("interface")
        window.show_all()
        window.connect("destroy", Gtk.main_quit)
        self.startRoutine_1sec()
        self.startRoutine_1min()
        
    def routine_1sec(self):
        global speed
        global altitude
        
        global day
        global month
        global year
        global hour
        global minute
        global second
        
        global text_time
        global text_speed
        global text_altitude
        
        label_time = self.builder.get_object('label_time')
        label_speed = self.builder.get_object('label_speed')
        label_altitude = self.builder.get_object('label_altitude')
        
        # UPDATING THE TIME FROM THE OS
        
        datetimenow = datetime.now()
        day = datetimenow.strftime("%d")
        month = datetimenow.strftime("%m")
        year = datetimenow.strftime("%Y")
        hour = datetimenow.strftime("%H")
        minute = datetimenow.strftime("%M")
        second = datetimenow.strftime("%S")
        
        text_time = day + "/" + month + "/" + year + "\n" + hour + ":" + minute + ":" + second
        
        label_time.set_label(text_time)
        
        # RECEIVING DATA FROM GPS
        try:        
            #It may take a second or two to get good GPS data

            #print (' GPS reading')
            #print ('----------------------------------------')
            #print ('latitude    ' , gpsd.fix.latitude)
            #print ('longitude   ' , gpsd.fix.longitude)
            #print ('time utc    ' , gpsd.utc,' + ', gpsd.fix.time)
            #print ('altitude    ' , gpsd.fix.altitude)
            ##print ('eps         ' , gpsd.fix.eps)
            ##print ('epx         ' , gpsd.fix.epx)
            ##print ('epv         ' , gpsd.fix.epv)
            ##print ('ept         ' , gpsd.fix.ept)
            #print ('speed        ' , gpsd.fix.speed)
            ##print ('climb       ' , gpsd.fix.climb)
            ##print ('track       ' , gpsd.fix.track)
            ##print ('mode        ' , gpsd.fix.mode)
            ##print ('sats        ' , gpsd.satellites)
            
            #print("GPS data OK")
            
            # UPLOAD TIME WITH GPS
            
            # 2019-04-28T02:26:27.000Z
            #time = gpsd.fix.time
            
            #day = time[8:10]
            #month = time[5:7]
            #year = time[0:4]
            #hour = time[11:13]
            #minute = time[14:16]
            #second = time[17:19]
            
            #text_time = day + "/" + month + "/" + year + "\n" + hour + ":" + minute + ":" + second
            
            speed = gpsd.fix.speed
            altitude = gpsd.fix.altitude
            
            text_speed = "Speed:\n" + str(round(speed)) + " km/h"
            text_altitude = "Altitude:\n" + str(round(altitude)) + " m"
            
        except:
            print("Problem with the GPS. Error #4: Application routine_1s")
            
            #label_time.set_label("--/--/----\n--:--:--")
            
            text_speed = "Speed:\n-- km/h"
            text_altitude = "Altitude:\n-- m"
        
        label_speed.set_label(text_speed)
        label_altitude.set_label(text_altitude)
        
        #  Return "True" to ensure the timer continues to run, otherwise it will only run once.
        return True
    
    def routine_1min(self):
        global temperature
        global pressure
        global humidity
        
        global text_temperature
        global text_pressure
        global text_humidity
        
        label_temperature = self.builder.get_object('label_temperature')
        label_pressure = self.builder.get_object('label_pressure')
        label_humidity = self.builder.get_object('label_humidity')
        
        try:
            sense = SenseHat()
            sense.clear()
        
            temperature = sense.get_temperature()
            pressure = sense.get_pressure()
            humidity = sense.get_humidity()
            
            text_temperature = "Temperature:\n" + str(round(temperature, 1)) + "°C"
            text_pressure = "Pressure:\n" + str(int(round(pressure))) + " hPa"
            text_humidity = "Humidity:\n" + str(int(round(humidity))) + "%"
            
        except:
            print("Sense HAT and Raspberry are not communicating")
            text_temperature = "Temperature:\n--°C"
            text_pressure = "Pressure:\n---- hPa"
            text_humidity = "Humidity:\n--%"
        
        label_temperature.set_label(text_temperature)
        label_pressure.set_label(text_pressure)
        label_humidity.set_label(text_humidity)
            
        #Return "True" to ensure the timer continues to run, otherwise it will only run once.
        return True

    # Initialize a routine
    def startRoutine_1sec(self):
        #  this takes 2 args: (how often to update in millisec, the method to run)
        self.routine_1sec()
        GObject.timeout_add(1000, self.routine_1sec)
        
    # Initialize a routine
    def startRoutine_1min(self):
        #  this takes 2 args: (how often to update in millisec, the method to run)
        self.routine_1min()
        GObject.timeout_add(60000, self.routine_1min)

    def main(self):
        Gtk.main()

        
app = Application()
app.main()