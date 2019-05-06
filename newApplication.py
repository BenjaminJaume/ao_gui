#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk, Gio, GObject
from datetime import datetime
from os.path import abspath, dirname, join

i = 0
GLADE_FILE = "newInterface.glade"

# Global variables definition
state_LED = "OFF"
state_vent = "OFF"
WHERE_AM_I = abspath(dirname(__file__))

class Handler:
    def on_button_LED_clicked(self, button):
        global state_LED

        # If we have clicked the button AND the LED was switched OFF
        if state_LED == "OFF":
            state_LED = "ON"
            print("LED TEST:", state_LED)
            
            button.set_label("LED: ON")
            image = Gtk.Image()
            image.set_from_file("rsz_led_on.png")
            button.set_image(image)                       
        else:
            state_LED = "OFF"
            print("LED TEST:", state_LED)
            
            button.set_label("LED: OFF")
            image = Gtk.Image()
            image.set_from_file("rsz_led_off.png")
            button.set_image(image)
            
    def on_button_vent_clicked(self, button):
        global state_vent
        
        if state_vent == "OFF":
            state_vent = "ON"
            print("Ventilation TEST:", state_vent)
            
            button.set_label("Ventilation: ON")
            image = Gtk.Image()
            image.set_from_file("on.png")
            button.set_image(image)
        else:
            state_vent = "OFF"
            print("Ventilation TEST:", state_vent)
            
            button.set_label("Ventilation: OFF")
            image = Gtk.Image()
            image.set_from_file("off.png")
            button.set_image(image)
    
    def on_button_settings_clicked(self, button):
        #settings = setting()
        print("Setting TEST")
    
    def on_interface_destroy(self, *args):
        print("Exit application")

class Application:
    def __init__(self):
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(GLADE_FILE)
        self.builder.connect_signals(Handler())
            
        window = self.builder.get_object("interface")
        window.show_all()
        window.connect("destroy", Gtk.main_quit)
        self.set_style()
        self.startRoutine_1sec()
    
    def set_style(self):
        """
        Change Gtk+ Style
        """
        provider = Gtk.CssProvider()
        # Demo CSS kindly provided by Numix project
        provider.load_from_path(join(WHERE_AM_I, 'style.css'))
        screen = Gdk.Display.get_default_screen(Gdk.Display.get_default())
        # I was unable to found instrospected version of this
        GTK_STYLE_PROVIDER_PRIORITY_APPLICATION = 600
        Gtk.StyleContext.add_provider_for_screen(
            screen, provider,
            GTK_STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        
    def routine_1sec(self):
        label_time = self.builder.get_object('label_time')

        # UPDATING TIME FROM THE OS
        
        datetimenow = datetime.now()
        day = datetimenow.strftime("%d")
        month = datetimenow.strftime("%m")
        year = datetimenow.strftime("%Y")
        hour = datetimenow.strftime("%H")
        minute = datetimenow.strftime("%M")
        second = datetimenow.strftime("%S")
        
        text_time = day + "/" + month + "/" + year + "\n" + hour + ":" + minute + ":" + second
        
        label_time.set_label(text_time)

        #  Return "True" to ensure the timer continues to run, otherwise it will only run once.
        return True

    # Initialize a routine
    def startRoutine_1sec(self):
        #  this takes 2 args: (how often to update in millisec, the method to run)
        self.routine_1sec()
        GObject.timeout_add(1000, self.routine_1sec)
        
    def main(self):
        Gtk.main()
        
app = Application()
app.main()
