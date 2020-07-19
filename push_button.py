import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import threading

INPUT_CHANNEL = 17
LED_CHANNEL = 27

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering

# Set GPIO 10to be an input pin and set initial value to be pulled low (off)
GPIO.setup(INPUT_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# SET Channel 27 to high to turn on the LED
GPIO.setup(LED_CHANNEL, GPIO.OUT) 

def register_callback(cb):    
#    cb2 = ButtonHandler(INPUT_CHANNEL, cb, edge='rising', bouncetime=70)
#    cb2.start()
    GPIO.add_event_detect(INPUT_CHANNEL, GPIO.RISING, callback=cb)

