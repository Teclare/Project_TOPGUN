
#Common
import time
import math
import multiprocessing

#================================

#Base Setting

originalDevID = '0'
originalSN = '001'

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

pygame.mixer.init()
pygame.mixer.music.load("notification.wav")
pygame.mixer.music.set_volume(1.0)

#=================================

#LED Setting
from rpi_ws281x import PixelStrip, Color
import rpi_ws281x as ws

import board
import neopixel

LED_COUNT = 30
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
    
def blinkLEDs(r, g, b, time, interval):
    for i in range(time):
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

def ai():
    
    while True: 
        ret, frame = cap.read()
    
        if ret:
            cv2.imwrite("captured_image.jpg", frame)
        else:
            print("image capture fail")
            
    
        if frame is None:
            print('could not open image')
            
        else:
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            
            if face_cascade.empty():
                print('fail to detect face')
                
            else:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                countedPeople = len(faces)
                
                
                for(x, y, w, h) in faces:
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0),2)
                
        
                if countedPeople > 5:
                    pygame.mixer.music.play()
                    danger = 1
                    blinkLEDs(255, 0, 0, 6, 0.5)
                    
                    print("Warning: More than 5 people detected!")
                elif countedPeople > 7:
                    danger = 2
                    blinkLEDs(255, 0, 0, 6, 0.5)
        
        print(faces)
        time.sleep(interval)

#=================================

#XBee Recieved and Upload
def Other_Device():
    while True:
    
        if ser.inWaiting():
              recieved_info = ser.readline().decode('utf-8').strip()
              print("Received: ", recieved_info)
    
              devID1, SN1, humanInfo1, cadaInfo1 = str(recieved_info).split('@')[:-1]
              
              response_text1 = send_data(devID1, originalDevID, SN1, humanInfo1, cadaInfo1)
              
              print("====class1=====\n devID: ", devID1, "\n contID: ", originalDevID, "\n SN: ", SN1, "\n humanInfo: ", humanInfo1, "\n cadaInfo: ", cadaInfo1, "\n ===============")
              print(f"responce: {response_text1}")
              time.sleep(interval)
              
        
#================================= 
                   
#Check Things and Upload  
def This_Device():
    while True:
        
        cadaInfo = co2Read()
        humanInfo = danger
        
        response_text = send_data(originalDevID, originalDevID, originalSN, humanInfo, cadaInfo)
        print("====class2=====\n devID: ", originalDevID, "\n contID: ", originalDevID, "\n SN: ", originalSN, "\n humanInfo: ", humanInfo, "\n cadaInfo: ", cadaInfo, "\n ===============")
        print(f"responce: {response_text}")
        time.sleep(interval)

#=================================

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=Other_Device)
    p2 = multiprocessing.Process(target=This_Device)
    p3 = multiprocessing.Process(target=ai)
    

    p1.start()
    p2.start()
    p3.start()