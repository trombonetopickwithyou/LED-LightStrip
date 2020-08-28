import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

from neopixel import *
from random import randint



# parameters #

#mqtt
CLIENT_NAME = "rp6102"
BROKER_URL = "test.mosquitto.org"
BROKER_PORT = 1883
TOPIC = "l_102934692"

#ws218b led strip
LED_COUNT      = 150     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!)
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 75     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# constants #
COLOR_WARM = Color(246, 205, 139)


# global variables #
#strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
global_color = COLOR_WARM
global_dance = 0



# functions #

def lightsOn ():

	global global_color
	global COLOR_WARM
	global strip


	#if color of lights are off, set to warm color by default
	#if (global_color == Color(0, 0, 0)):
	#print('made it here2\n')
	#global_color = COLOR_WARM


	#wipe color across display a pixel at a time
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, global_color)
		strip.show()
		time.sleep(1.0/1000.0)

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







#executes whenever a message is posted to mqtt topic
def messageFunction (client, userdata, message):

	global global_color
	global COLOR_WARM

	global global_dance

	topic = str(message.topic)
	message = message.payload.decode("utf-8")

	print(topic + ': ' + message)

	if (message == "on"):
		print('turning lights on...\n')
		lightsOn()

	elif (message == "off"):
		print('turning lights off...\n')
		lightsOff()

	elif (message == "red"):
		global_color = Color(0, 0, 255)
		lightsOn()

	elif (message == "green"):
		global_color = Color(0, 255, 0)
		lightsOn()

	elif (message == "blue"):
		global_color = Color(255, 0, 0)
		lightsOn()

	elif (message == "white"):
		global_color = Color(255, 255, 255)
		lightsOn()

	elif (message == "warm"):
		global_color = COLOR_WARM
		lightsOn()

	elif (message == "dance"):
		global_dance = 1

	elif (message == "danceoff"):
		global_dance = 0

	else:
		print('command not recognized, assuming custom color code')
		
		message = str(message)
		print("Red: ", int(message[0:3]))
		print("Blue: ", int(message[3:6]))
		print("Green: ", int(message[6:9]))

		global_color = Color(int(message[0:3]), int(message[3:6]), int(message[6:9]))
		lightsOn()


############# MAIN CODE ##############

# setup #

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)

#give the rpi time to connect to the internet
print("Waiting 15 seconds on startup...")
GPIO.output(14,GPIO.HIGH)
time.sleep(15)
GPIO.output(14, GPIO.LOW)


#mqtt
myClient = mqtt.Client(CLIENT_NAME) 			#MQTT client object

myClient.connect(BROKER_URL, BROKER_PORT) 		#Connect to the broker (mosquitto free test server)
myClient.subscribe(TOPIC) 						#Subscribe to the topic
myClient.on_message = messageFunction			#(on_message should act like an interrupt)

#lights
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)






# start #

#mqtt
myClient.loop_start()
print('Successfully started\nMQTT Broker: ' + BROKER_URL + ':' + str(BROKER_PORT) + '\nTopic: ' + TOPIC + '\n')

#lights
strip.begin()


while(1):
	
	time.sleep(1)

	if (global_dance == 1):
		global_color = Color(randint(0,255), randint(0,255), randint(0,255))
		lightsOn()