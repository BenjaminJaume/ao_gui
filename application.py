import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio

#import RPi.GPIO as GPIO
#RPi.GPIO.setmore(RPi.GPIO.BCM)

from gpiozero import LED
import time

# setup GPIO
#GPIO.setmode(GPIO.BCM) # Broadcom numbering system
#GPIO.setup(ledPin, GPIO.OUT)
#GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#GPIO.output(ledPin, GPIO.LOW)
#pwm.start(duty)

# pin definitions
ledPin = 23

# Constants
brightness = 75 # percent
        
class Handler:        
    def on_button_on_clicked(self):
        #GPIO.output(ledPin, GPIO.HIGH)
        print("The LED is now ON")
        
    def on_button_off_clicked(self):
        #GPIO.output(ledPin, GPIO.LOW)
        print("The LED is now OFF")
    
    ## Close the application
    def onDestroy(self, *a, **kv):
        Gtk.main_quit()
        sys.exit(0)
        
    def onQuit(self, *a, **kv):
        Gtk.main_quit()
        sys.exit(0)    

## Creating / invoking the application's window
builder = Gtk.Builder()
builder.add_from_file("interface.glade")
builder.connect_signals(Handler)

window = builder.get_object("AO_Skylys")
window.show_all()
#window.maximize()

Gtk.main()