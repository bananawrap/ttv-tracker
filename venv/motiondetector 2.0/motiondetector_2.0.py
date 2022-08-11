import pygame
from pygame.locals import *
from PIL import ImageGrab,ImageChops,Image,ImageOps
from threading import Thread
import copy
import time
import numpy as np

              
def main():
    global img,img2,width,height,screen,backround
    pygame.init()
    img = ImageGrab.grab()
    width, height = img.size
    screen = pygame.display.set_mode((width,height))
    #img = ImageGrab.grab()
    backround = pygame.Surface(screen.get_size())
    
    
    while True: 
        
        img2 = ImageGrab.grab()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                break
        diff = ImageChops.difference(img,img2)
        diff = ImageOps.autocontrast(diff)
        image = pygame.image.fromstring(diff.tobytes(), diff.size, diff.mode)
        screen.blit(image,(0,0))
        pygame.display.flip()
    
        img = ImageGrab.grab()
       
        diff = ImageChops.difference(img,img2)
        diff = ImageOps.autocontrast(diff)
        image = pygame.image.fromstring(diff.tobytes(), diff.size, diff.mode)
        screen.blit(image,(0,0))
        pygame.display.flip()
        
                    

        
        
        
        
        

        

if __name__=="__main__": 
    FPS = 60
    clock = pygame.time.Clock()
    main()



