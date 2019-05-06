#!/usr/bin/python
# -*- coding: utf-8 -*-

#import RPi.GPIO as GPIO
import gi, os, sys, time
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk, GLib, Gdk, Gio, GObject, WebKit
from gpiozero import LED
#from sense_hat import SenseHat
from datetime import datetime
#from gps import *
from time import *
import time
import threading

i = 0
GLADE_FILE = "test.glade"

class Handler:
    #NOTHING IN HERE
    print()

class Application:
    def __init__(self):
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(GLADE_FILE)
        self.builder.connect_signals(Handler())
        
        window = self.builder.get_object("interface")
        window.show_all()
        window.connect("destroy", Gtk.main_quit)

    def main(self):
        Gtk.main()
        
app = Application()
app.main()
