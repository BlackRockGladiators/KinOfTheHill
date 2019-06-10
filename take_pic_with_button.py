import RPi.GPIO as GPIO
from picamera import PiCamera
import time
from Tkinter import *

class KingOfTheHill():
    time_displayed = 60

    def __init__(self):
        # set up button
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        input_pin = 10
        pin_off = GPIO.PUD_DOWN
        GPIO.setup(input_pin, GPIO.IN, pull_up_down=pin_off)
        GPIO.add_event_detect(input_pin, GPIO.RISING, callback=self.button_callback)

        # set up cammera
        self.camera = PiCamera()
        self.camera.start_preview()

    def __del__(self):
        GPIO.cleanup()

    def button_callback(self, channel):
        pic_file = "/that_harddrive_we_brought/winners_photos/probably_someone_getting_hurt_{}.jpg".format(time.now())
        self.camera.capture(pic_file)
        display = self.display_image(pic_file)
        self.camera.stop_preview()

        time.sleep(self.time_displayed)
        self.camera.start_preview()
        display.destroy()

    def display_image(self, file):
        root = Tk()
        canvas = Canvas(root, width =1224,height=1000) # TODO: make fullscreen
        pic = PhotoImage(file=file)
        canvas.create_image(0, 0, image=pic)
        root.mainloop()
        return root

if __name__ == '__main__':
    hill = KingOfTheHill()
    while True:
        input("The blood of out enemies!\n\n")
