import threading
from time import sleep
from apa102_pi.colorschemes import colorschemes

NUM_LED = 40

class LightController(threading.Thread):
  def __init__(self, i):
      threading.Thread.__init__(self)
      self.h = i
  def run(self):
      print("Value send", self.h)
      MY_CYCLE = colorschemes.Solid(num_led=NUM_LED, pause_value=3,
                                    
                              num_steps_per_cycle=1, num_cycles=1)
      # One slow trip through the rainbow
      #MY_CYCLE = colorschemes.Rainbow(num_led=NUM_LED, pause_value=0.03,
                                      num_steps_per_cycle=34, num_cycles=5)
      #MY_CYCLE.start()      
      print("Done! with falsh")

thread1 = LightController(1)
thread1.start()
print("Test")

      
