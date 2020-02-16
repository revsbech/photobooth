import lcddriver
from time import *

lcd = lcddriver.lcd()
lcd.lcd_clear()

lcd.lcd_display_string(' sebastian 2.a', 1)
lcd.lcd_display_string(' 2020@', 2)

