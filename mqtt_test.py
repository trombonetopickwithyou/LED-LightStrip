import RPi.GPIO as GPIO

import time
from datetime import datetime,date,timedelta
from neopixel import *

from random import randint


# parameters #

#ws218b led strip
LED_COUNT      = 150     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!)
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# constants #
COLOR_WARM = Color(246, 205, 139)


def wheel(pos, brightness):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(int(brightness*(pos * 3)), int(brightness*(255 - pos * 3)), 0)
    elif pos < 170:
        pos -= 85
        return Color(int(brightness*(255 - pos * 3)), 0, int(brightness*(pos * 3)))
    else:
        pos -= 170
        return Color(0, int(brightness*(pos * 3)), int(brightness*(255 - pos * 3)))

# functions #
def lightsOn (color, delay):
    global strip

    #wipe color across display one pixel at a time
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(delay/1000.0)

    #strip.show()
    print('Turned lights on!\n')

def lightsOff ():
    global strip

    #wipe color across display a pixel at a time
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(50.0/1000.0)

    print('Turned lights off!\n')



############# MAIN CODE ##############

# setup #
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)

GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 21 to be an input pin

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

lightsOff()


brightness = 0.35
offset = 0
direction = 1
on = False


while (1):

    #if the butotn is pressed
    if GPIO.input(15) == GPIO.HIGH:
        print("Button was pushed!")
        GPIO.output(14, GPIO.HIGH)
        
        time.sleep(1)

        on = True
        today = datetime.today()
        GPIO.output(14, GPIO.LOW)

    #if it's between midnight to 1am or 7pm to midnight
    while(on == True and (today.hour < 1 or today.hour > 19)):

        today = datetime.today()

        for j in range(256):
            #write values from a rainbow to all pixels on the strip
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((i+j) & 255, brightness + offset))
            strip.show()
            
            #adjust brightness "swelling" effect
            if (offset >= 0.1) or (brightness + offset >= 1):
                direction = -1

            if (offset <= -0.1) or (brightness + offset <= 0):
                direction = 1

            
            offset += direction*0.001
            time.sleep(15.0/1000.0)

            if GPIO.input(15) == GPIO.HIGH:
                print("Button was pushed")
                GPIO.output(14, GPIO.HIGH)

                lightsOff()
                on = False

                GPIO.output(14, GPIO.LOW)
                break

