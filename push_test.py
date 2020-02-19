import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import threading

INPUT_CHANNEL = 17
LED_CHANNEL = 27

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering

# Set GPIO 10to be an input pin and set initial value to be pulled low (off)
GPIO.setup(INPUT_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

# SET Channel 27 to high to turn on the LED
GPIO.setup(LED_CHANNEL, GPIO.OUT) 


#This is to fix the inproper debouncing of the GPIO event
# See https://raspberrypi.stackexchange.com/questions/76667/debouncing-buttons-with-rpi-gpio-too-many-events-detected
class ButtonHandler(threading.Thread):
    def __init__(self, pin, func, edge='both', bouncetime=200):
        super().__init__(daemon=True)

        self.edge = edge
        self.func = func
        self.pin = pin
        self.bouncetime = float(bouncetime)/1000

        self.lastpinval = GPIO.input(self.pin)
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = GPIO.input(self.pin)

        if (
                ((pinval == 0 and self.lastpinval == 1) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval == 1 and self.lastpinval == 0) and
                 (self.edge in ['rising', 'both']))
        ):
            self.func(*args)

        self.lastpinval = pinval
        self.lock.release()

def register_callback(cb):    
    cb2 = ButtonHandler(INPUT_CHANNEL, cb, edge='rising', bouncetime=100)
    cb2.start()
    GPIO.add_event_detect(INPUT_CHANNEL, GPIO.RISING, callback=cb2)

def clicked(channel):
    print(" Button cliecked")
    
register_callback(clicked)
message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup()    
