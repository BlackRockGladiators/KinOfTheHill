import RPi.GPIO as GPIO
from picamera import PiCamera
import datetime
from PIL import Image
import time

PIC_DIR = ''

class KingOfTheHill:
    def __init__(self, input_pin):
        self.input_pin = input_pin
        
        # set up cammera
        self.camera = PiCamera()
        self.camera.start_preview()

        # set up button
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #GPIO.add_event_detect(input_pin, GPIO.RISING, callback=self.button_callback)

        self.last_layer = None

    def picture(self):
        pic_file = PIC_DIR + "probably_someone_getting_hurt_{}.png".format(datetime.datetime.now())
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
        if self.last_layer:
            self.last_layer.layer = 2
        o.alpha = 255
        o.layer = 3
        
        if self.last_layer:
            self.camera.remove_overlay(self.last_layer)
        self.last_layer = o

        time.sleep(5)

    def button_pressed(self):
        return GPIO.input(self.input_pin) == GPIO.HIGH
        

if __name__ == '__main__':
    hill = KingOfTheHill(10)

    while True:
        if hill.button_pressed():
                hill.picture()
    GPIO.cleanup()
