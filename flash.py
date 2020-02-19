import threading
from time import sleep
#from apa102_pi.colorschemes import colorschemes
from apa102_pi.driver import apa102

NUM_LED = 40

class Flash(threading.Thread):
  def __init__(self, seconds, brightness=50):
      threading.Thread.__init__(self)

      self.seconds = seconds
      self.brightness = brightness
  def run(self):
      print("Flash for seconds: ", self.seconds)

      strip = apa102.APA102(num_led=NUM_LED,
                global_brightness=255,
                mosi=10, sclk=11,
                order='rgb')  # Initialize the strip
      strip.clear_strip()
      for led in range(0, NUM_LED):
        strip.set_pixel_rgb(led, 0xFFFFFF, self.brightness)

      strip.show()
      sleep(self.seconds)
      strip.clear_strip()

      strip.cleanup();
      print("Done! with flash")

#thread1 = Flash(2,70)
#thread1.start()
#print("Test")

      
