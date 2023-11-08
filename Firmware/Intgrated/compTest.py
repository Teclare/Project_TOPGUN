import pygame
pygame.mixer.init()
pygame.mixer.music.load("/home/topgun/Project/resource/feelSomething.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play()


import time
from rpi_ws281x import PixelStrip, Color
import rpi_ws281x as ws

import board
import neopixel


LED_COUNT = 52
LED_PIN = 18  # GPIO 18
LED_BRIGHTNESS = 255
LED_ORDER = ws.WS2812_STRIP

strip = PixelStrip(LED_COUNT, LED_PIN, dma=10, brightness=LED_BRIGHTNESS, invert=False, channel=0, strip_type=LED_ORDER)

strip.begin()

def clearLEDs(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()




try:
    while pygame.mixer.music.get_busy() == True:
        for j in range(0, 255):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(j, 0, 0))
            strip.show()
            time.sleep(0.01)
            
        for j in range(0, 255):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(0, j, 0))
            strip.show()
            time.sleep(0.01)
            
        for j in range(0, 255):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(0, 0, j))
            strip.show()
            time.sleep(0.01)
            
        time.sleep(1)
        
        for j in range(255, 0, -1):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(j, j, j))
            strip.show()
            time.sleep(0.01)
            
        time.sleep(1)
        
    clearLEDs(strip)

except KeyboardInterrupt:

    clearLEDs(strip)
