import lcddriver
from picamera import PiCamera
from time import sleep
import logging
import boto3
import time
from botocore.exceptions import ClientError

#AWS
#bucket = "jer-photobooth"
bucket = "photobooth-write-s3-object"
s3_client = boto3.client("s3")

# CAMERA
camera = PiCamera()
camera.resolution = (2592, 1944)
#camera.resolution = (800, 600)
camera.framerate = 15

#LCD
lcd = lcddriver.lcd()
lcd.lcd_clear()


def output_lcd(text1, text2):
    lcd.lcd_display_string(text1, 1)
    lcd.lcd_display_string(text2, 2)

def upload(filename):
    key = "rawImages/capture/" + time.strftime("%Y/%m/%d/capture-%H%M%S.jpg") 
    try:
        response = s3_client.upload_file(filename, bucket, key)
    except ClientError as e:
        logging.error(e)
        
        return False
    return True

camera.start_preview()
camera.annotate_text_size = 150
for i in range(5):
  camera.annotate_text = "Ready %d" % (5-i)
  output_lcd("#### READY! ####", "        %d" % (5-i))
  sleep(1)
  
  
output_lcd("##### SMIL! #####", "################")
    
camera.annotate_text = ""
filename = '/home/pi/Desktop/capture.jpg'
camera.capture(filename)
camera.stop_preview()
output_lcd("### Uploader... ###", "################")
res = upload(filename)
if res:
    output_lcd("## Billede klar ##", "################")
else:
    output_lcd("!!!!! FEJL !!!!!", "!!!!!!!!!!!!!!!!")


sleep(2)
lcd.lcd_clear()
