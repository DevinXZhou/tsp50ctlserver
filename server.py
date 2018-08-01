from flask import Flask
from flask import request

########### Local Internet Server ###########
app = Flask(__name__)
traffic = 0
last_flags = [1]*8
@app.route('/')
def root():
    return 'TSP50 Control Server'

@app.route('/getint') #get the int value from stored variable traffic
def getint():
    global traffic
    return str(traffic)


@app.route('/getbin') #get binary bits sequence of the LED queue
def getbin():
    global traffic
    b = bin(traffic)[2:]
    while (len(b) < 8):
        b = '0'+b
    return b

@app.route('/post') #post an int value to this server and stored as traffic
def post():
    global traffic
    n = int(request.args.get('n'))
    if n < 256 and n >= 0:
        traffic = n
        LED_flags = intToBinArr(traffic)
        for i in range(1, 8):
            if i+1 in LED_MAPPING:
		if last_flags[i] != LED_flags[i]:
			GPIO.output(LED_MAPPING[i+1], LED_flags[i]) # 0 is on
	last_flags = LED_flags
    else:
        return "input value is invalid, it should be ranged from 0 to 255"
        
    
    return "int:" + str(traffic) + ", bits: " + getbin()

@app.route('/alloff')
def alloff():
    global traffic
    GPIO.output(DetectorGPIOs, True)
    traffic = 0
    return "all LED are turned off"

@app.route('/allon')
def allon():
    global traffic
    GPIO.output(DetectorGPIOs, False)
    traffic = 255
    return "all LED are turned on"

@app.route('/reset')
def reset():
    alloff()
    GPIO.cleanup()
    configTSP50()
    return "TSP50 is cleaned up, and reseted"

########## Control TSP50 LED ###########
import RPi.GPIO as GPIO
import time
import sys

GPIO_BCM_channels = [2,3,4,17,27,22,10,9,11,5,6,13,19,26,
			21,20,16,12,7,8,25,24,23,18,15,14]
DetectorGPIOs = [2, 3, 4, 17, 27, 22, 10]
LED_MAPPING = {2:2, 3:3, 4:4, 5:17, 6:27, 7:22, 8:10}

def DETECTOR_ON_ALL():
        GPIO.output(DetectorGPIOs, False)
        return 0

def DETECTOR_OFF_ALL():
        GPIO.output(DetectorGPIOs, True)
        return 0

def configTSP50():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_BCM_channels, GPIO.OUT)
    DETECTOR_OFF_ALL()

def intToBinArr(n): #convert an int (8 bit int) to bits array
    b = bin(255-n)[2:] #complement exp. '0b0000110' => '0b1111001', there are total 7 LEDs 7 bits
    while (len(b) < 8):
        b = '0'+b
    arr = list(map(int, list(b)))
    arr = arr[::-1]
    return arr
    
configTSP50()

    
