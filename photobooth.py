import lcddriver
from picamera import PiCamera
from time import sleep
from apa102_pi.colorschemes import colorschemes
import logging
import boto3
import time
from botocore.exceptions import ClientError
import push_button
import flash

#Light strip
NUM_LED = 60

#AWS
bucket = "photobooth-write-s3-object"
s3_client = boto3.client("s3")

# CAMERA
camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15

#LCD
lcd = lcddriver.lcd()
lcd.lcd_clear()

def output_lcd(text1, text2):
    print(text1)
    print(text2)
    lcd.lcd_display_string(text1, 1)
    lcd.lcd_display_string(text2, 2)

def upload(filename):
#    return True
    key = "rawImages/capture/" + time.strftime("%Y/%m/%d/capture-%H%M%S.jpg") 
    try:
        response = s3_client.upload_file(filename, bucket, key)
    except ClientError as e:
        logging.error(e)
        
        return False
    return True

#The channel param is not really used, but required when used as a callback to GPIO
def take_picture(channel):
    lcd.lcd_clear()    
    camera.start_preview()
    camera.annotate_text_size = 150
    for i in range(5):
        camera.annotate_text = "Ready %d" % (5-i)
        output_lcd("#### READY! ####", "        %d" % (5-i))
        MY_CYCLE = colorschemes.RoundAndRound(num_led=NUM_LED, pause_value=1/NUM_LED,
                                              num_steps_per_cycle=NUM_LED, num_cycles=1)
        MY_CYCLE.start()        
#        sleep(1)

    
    thread1 = flash.Flash(2,70)
    thread1.start()

    output_lcd("##### SMIL! #####", "################")

    camera.annotate_text = ""
    filename = '/home/pi/Desktop/capture.jpg'
    camera.capture(filename)
    camera.stop_preview()
    output_lcd("  Uploader... ", "-!-!-!-!-!-!-!-!")
    res = upload(filename)
    if res:
        output_lcd(" Billede klar!", "---------------")
    else:
        output_lcd("!!!!! FEJL !!!!!", "!!!!!!!!!!!!!!!!")
    sleep(2)
    output_lcd(" - Photobooth - ", "Tryk pa knappen")



#Main control loop
output_lcd(" - Photobooth - ", "Tryk pa knappen")
push_button.register_callback(take_picture)
message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() 
