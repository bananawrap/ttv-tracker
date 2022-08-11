import pygame
from pygame.locals import *
from PIL import ImageGrab,ImageChops
from threading import Thread
import copy
import time

def makelist():
    global pixeldiff,pixelpos
    pixeldiff = []
    pixelpos = []

    while True:
        pixeldiff = []
        pixelpos = []
        try:            
            for y in range(0,height,5):
                for x in range(0,width,5):
                    coords = x,y
                    if img.getpixel(coords) != img2.getpixel(coords):
                        pixel = list(last.getpixel(coords))
                        
                        for i in range(len(pixel)):
                            pixel[i] = 255 - pixel[i]
                        pixel = tuple(pixel)
                        pixeldiff.append(pixel)
                        pixelpos.append(coords)

        except:
            pass

def render():
    global image, screen
    image = pygame.image.fromstring(last.tobytes(), last.size, last.mode)
    screen.blit(image,(0,0))


    
                
def main():
    global img,img2,width,height,screen,first,last,backround
    pygame.init()
    vittu = 1
    img = ImageGrab.grab()
    width, height = img.size
    screen = pygame.display.set_mode((width,height-55))
    img = ImageGrab.grab()
    backround = pygame.Surface(screen.get_size())
    
    t1.start()
    #t2.start()
    while True: 
        clock.tick(fps)
        if vittu == 1:
            img2 = ImageGrab.grab()
            first = img2
            last = img
            vittu = 2
        elif vittu == 2:
            img = ImageGrab.grab()
            first = img
            last = img2
            vittu = 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
        
        
        #backround.fill((0,0,0))
        
        render()
        for pixel in range(len(pixeldiff)):
            try:
                screen.set_at(pixelpos[pixel], pixeldiff[pixel])
            except:
                pass
        pygame.display.flip()

                    

        
        
        
        
        

        

if __name__=="__main__": 
    fps = 60
    clock = pygame.time.Clock()
    t1 = Thread(target=makelist)
    #t2 = Thread(target=render)
    
    main()