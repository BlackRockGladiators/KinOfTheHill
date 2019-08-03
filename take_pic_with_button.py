import RPi.GPIO as GPIO
from picamera import PiCamera
import datetime
from PIL import Image
import time
import sys

class KingOfTheHill():
    time_displayed = 5

    def __init__(self):
        # set up cammera
        self.camera = PiCamera()
        self.camera.start_preview()

    #def __del__(self):
    #    GPIO.cleanup()

    def button_callback(self):
        pic_file = "probably_someone_getting_hurt_{}.png".format(datetime.datetime.now())
        self.camera.capture(pic_file)
        self.display_image(pic_file)

    def display_image(self, file):
        img = Image.open(file)
        pad = Image.new('RGB', ( \
            ((img.size[0] + 31) // 32) * 32, \
            ((img.size[1] + 15) // 16) * 16, \
            ))
        # Paste the original image into the padded one
        pad.paste(img, (0, 0))
        o = self.camera.add_overlay(pad.tobytes(), size=img.size)
        o.alpha = 255
        o.layer = 3
        self.camera.preview.alpha = 0
        time.sleep(10)
        
        self.camera.preview.alpha = 255
        self.camera.remove_overlay(o)

if __name__ == '__main__':
    #hill = KingOfTheHill()
    #line = sys.stdin.readline().strip()
    #while line != "q":
    #    hill.button_callback()
    #    line = sys.stdin.readline().strip()
    #time.sleep(5)


    # set up button
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    pin = 10
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    while True:
        if GPIO.input(pin) == GPIO.HIGH:
            print GPIO.input(pin)

        
