import pygame
pygame.mixer.init()
pygame.mixer.music.load("feelSomething.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue