from flask import Flask
from flask import request

########### Local Internet Server ###########
app = Flask(__name__)
traffic = 0

@app.route('/')
def root():
    return 'TSP50 Control Server'

@app.route('/getint') #get the int value from stored variable traffic
def getint():
    global traffic
    return str(traffic)


@app.route('/getbin') #get binary bits sequence of the LED queue, first correspond to LED#2
def getbin():
    global traffic
    b = bin(traffic)[2:]
    while (len(b) < 7):
        b = '0'+b
    b = b[::-1]
    return b

@app.route('/post') #post an int value to this server and stored as traffic
def post():
    global traffic
    n = int(request.args.get('n'))
    if n < 128 and n >= 0:
        traffic = n
        LED_flags = intToBinArr(traffic)
        for i in range(0, 7):
            if i+2 in LED_MAPPING:
                GPIO.output(LED_MAPPING[i+2], LED_flags[i]) # 0 is on
    else:
        return "input value is invalid, it should be ranged from 0 to 127"
        
    
    return "request is proceeded, data is modified to " + str(traffic) + "and the bits squence are " + getbin()

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

def intToBinArr(n): #convert an int to bits array
    b = bin(127-n)[2:] #complement exp. '0b0000110' => '0b1111001', there are total 7 LEDs 7 bits
    while (len(b) < 7):
        b = '0'+b
    arr = list(map(int, list(b)))
    arr = arr[::-1]
    return arr
    
configTSP50()

    
