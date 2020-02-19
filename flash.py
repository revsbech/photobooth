from apa102_pi.driver import apa102
import time
NUM_LED = 40

class Flash():
  def __init__(self):

      self.strip = apa102.APA102(num_led=NUM_LED,
                global_brightness=255,
                mosi=10, sclk=11,
                order='rgb')  # Initialize the strip
  def on(self, brightness = 50):

      self.strip.clear_strip()
      for led in range(0, NUM_LED):
        self.strip.set_pixel_rgb(led, 0xFFFFFF, brightness)
      self.strip.show()

  def off(self):
      self.strip.clear_strip()

  def cleanup(self):   
      self.strip.cleanup();


#f = Flash()
#f.on(5)
#time.sleep(2)
#f.off()
#f.cleanup()
#print("Test")

      
