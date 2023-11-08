
#Common
import time
import math
from multiprocessing import Process, Queue

#================================

#Base Setting

LED_COUNT = 52

originalDevID = '0375285912696493'
originalSN = '0000000002'

humanInfo = 0

countedPeople = 0
danger = 0

interval = 3

#================================

#CV Setting

import cv2
    
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('camera connect fail')
    exit()

#==========================

#HTTP connection
import requests
import json

def send_data(devID, contID, SN, humanInfo, cadaInfo):
    url = "http://104.248.99.126:10540/send_data"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "devID": str(devID),
        "contID": str(contID),
        "SN": str(SN),
        "humanInfo": str(humanInfo),
        "cadaInfo": str(cadaInfo)
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    return response.text

#=================================

#Sound Function
import pygame

def playSound(queue):
    pygame.mixer.init()
    while True:
        sound_file = queue.get()  # This will block until a sound file is received
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

#=================================

#LED Setting
from rpi_ws281x import PixelStrip, Color
import rpi_ws281x as ws

import board
import neopixel

LED_PIN = 18  # GPIO 18
LED_BRIGHTNESS = 255
LED_ORDER = ws.WS2812_STRIP

strip = PixelStrip(LED_COUNT, LED_PIN, dma=10, brightness=LED_BRIGHTNESS, invert=False, channel=0, strip_type=LED_ORDER)

strip.begin()

def clearLEDs():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def setLEDs(r, g, b):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(r, g, b))
    strip.show()
    
def blinkLEDs(r, g, b, count, interval):
    for i in range(count):
        setLEDs(r, g, b)
        time.sleep(interval)
        clearLEDs()
        time.sleep(interval)

#==========================

#Xbee recieve
import serial

uart_port = '/dev/ttyS0'
baud_rate = 9600 

ser = serial.Serial(uart_port, baud_rate, timeout=1)

#==========================

#Co2 Scanning
import spidev
import RPi.GPIO as GPIO

MG_PIN = 0
BOOL_PIN = 2
DC_GAIN = 8.5

READ_SAMPLE_INTERVAL = 0.05
READ_SAMPLE_TIMES = 5

ZERO_POINT_VOLTAGE = 0.220
REACTION_VOLTAGE = 0.030
CO2_CURVE = [2.602, ZERO_POINT_VOLTAGE, REACTION_VOLTAGE / (2.602 - 3)]

GPIO.setmode(GPIO.BCM)
GPIO.setup(BOOL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

spi=spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1000000

def co2Read():
    v = 0
    for i in range(READ_SAMPLE_TIMES):
        adc = spi.xfer2([1, (8 + MG_PIN) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        v += data
        time.sleep(READ_SAMPLE_INTERVAL)
    volts = (v / READ_SAMPLE_TIMES) * 5.0 / 1024
    
    if (volts / DC_GAIN) >= ZERO_POINT_VOLTAGE:
        return '<400'
    else:
        return str(round(math.pow(10, (volts/DC_GAIN - CO2_CURVE[1]) / CO2_CURVE[2] + CO2_CURVE[0]), 2))
        
#=================================

def ai(queue):
    
    while True: 
        ret, frame = cap.read()
    
        if ret:
            cv2.imwrite("captured_image.jpg", frame)
        else:
            print("image capture fail")
            
    
        if frame is None:
            print('could not open image')
            
        else:
            face_cascade = cv2.CascadeClassifier('/home/topgun/Project/resource/haarcascade_frontalface_default.xml')
            
            if face_cascade.empty():
                print('fail to detect face')
                
            else:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                countedPeople = len(faces)
                
                
                for(x, y, w, h) in faces:
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0),2)
                
        
                if countedPeople >= 3:
                    danger = 1
                    blinkLEDs(255, 127, 0, 10, 0.5)
                    setLEDs(255, 255, 255)
                    
                elif countedPeople >= 5:
                    queue.put("/home/topgun/Project/resource/amber.mp3")
                    danger = 2
                    blinkLEDs(255, 0, 0, 10, 0.5)
                    setLEDs(255, 255, 255)
                
                elif countedPeople >= 7:
                    queue.put("/home/topgun/Project/resource/amber.mp3")
                    danger = 3
                    blinkLEDs(255, 0, 0, 10, 0.5)
                    setLEDs(255, 255, 255)
                    
                else:
                    danger = 0
        
        print(faces)
        time.sleep(interval)

#=================================

#Developer Option
#0@0@

def Developer(queue):
    
    while True:
    
        if ser.inWaiting():
            recieved_command = ser.readline().decode('utf-8').strip()
            print("Received: ", recieved_command)
            testLed, testSound = str(recieved_command).split('@')[:-1]
    
            if testSound == '1':
                queue.put("/home/topgun/Project/resource/amber.mp3")
            
            if testLed == '1':
                blinkLEDs(255, 127, 0, 10, 0.5)
                setLEDs(255, 255, 255)

            time.sleep(interval)
              
#================================= 
                   
#Check Things and Upload  
def This_Device():
    while True:
        
        cadaInfo = co2Read()
        humanInfo = danger
        
        ser.write(originalDevID.encode('utf-8'))
        ser.write("@".encode('utf-8'))
        ser.write(originalSN.encode('utf-8'))
        ser.write("@".encode('utf-8'))
        ser.write(str(humanInfo).encode('utf-8'))
        ser.write("@".encode('utf-8'))
        ser.write(str(cadaInfo).encode('utf-8'))
        ser.write("@".encode('utf-8'))
        ser.write(b'\n')
        
        print("Send")
        time.sleep(interval)

#=================================

if __name__ == "__main__":

    sound_queue = Queue()
    
    # Start the sound playing process
    sound_process = Process(target=playSound, args=(sound_queue,))
    sound_process.start()
    
    #Booting Sequance
    pygame.mixer.init()
    pygame.mixer.music.load("/home/topgun/Project/resource/amber.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(1)

    #Booting Sequance
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 255, 0))
        strip.show()
        time.sleep(0.15)

    setLEDs(255, 255, 255)
    
    #Other processes
    p1 = Process(target=This_Device)
    p2 = Process(target=ai, args=(sound_queue,))
    p3 = Process(target=Developer, args=(sound_queue,))
    
    #Start other processes
    p1.start()
    p2.start()
    p3.start()
    
    #Join processes if needed
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    sound_process.join()