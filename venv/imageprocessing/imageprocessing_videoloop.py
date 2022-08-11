from PIL import Image, ImageGrab
import math
import time
from operator import sub, add, floordiv
import statistics
import urllib.request,io
import copy
import subprocess
from tkinter import * 
from tkinter.ttk import *
while True:
    indicator = x, y = 0, 0
    frames = []
    FPS = 1
    
    
    for n in range(FPS):
        frames.append(ImageGrab.grab())
        time.sleep(1/FPS)

    #frames = ImageFilter.SHARPEN
    width = frames[0].size[0]
    height = frames[0].size[1]
    print(width, height)
    pixelList = []
    pixelListList = {}
    counter = 0

    def progress_bar(current, total, bar_length = 20):
        percent = float(current) * 100 / total
        arrow   = '-' * int(percent/100 * bar_length - 1) + '>'
        spaces  = ' ' * (bar_length - len(arrow))

        print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')

    for i in range(len(frames)):
        
        for y in range(height):
            progress_bar (y, height)
            for x in range(width):
                #counter = counter+1      #glitch mode
            # if counter == 50000:    
                #    counter = 0
                #   print("reloading image")
                #  img.close()
                # img = ImageGrab.grab()
                    #width = img.size[0]
                    #height = img.size[1]
                indicator = x, y
                pixelList.append(frames[i].getpixel(indicator))
        pixelList[i] = copy.copy(pixelList)
        pixelListList.update({i: pixelList[i]})
        
        pixelList.clear()
            
            
    with open("image.txt", "w") as output:
        output.write(str(pixelListList))


    #print("opening image")
    #print("starting processing soon...")
    #img.putdata(pixelList)
    #img.show()

    def outliner():
        for bruh in range(len(frames)):
            
            global pixelListList
            pixelList = []
            pixelList = pixelListList[bruh]
            color1 = []
            color2 = []
            color3 = []
            color4 = []
            lol = math.floor(len(pixelList))/2
            lol = int(lol)
            x = (0, 0, 0)
            y = (0, 0, 0)
            shademodifier = 0
            counter1 = 0
            #getting 4 lists of pixels
            for i in range(lol*2):
                if i < len(pixelList)-3:
                    color1.append(pixelList[i])
                    color2.append(pixelList[i+1])
                    color3.append(pixelList[i+2])
                    color4.append(pixelList[i+3])
            color1 = color1[::4]
            color2 = color2[::4]
            color3 = color3[::4]
            color4 = color4[::4]
            #calc average of lists
            sum = 0
            for sub2 in color1:
                for i in sub2:
                    sum = sum + i
            res = sum / len(color1)
            sum2 = 0
            for sub2 in color2:
                for i in sub2:
                    sum2 = sum2 + i
            res2 = sum2 / len(color2)
            sum3 = 0
            for sub2 in color3:
                for i in sub2:
                    sum3 = sum3 + i
            res3 = sum3 / len(color3)
            sum4 = 0
            for sub2 in color4:
                for i in sub2:
                    sum4 = sum4 + i
            res4 = sum4 / len(color4)
            colorlist = [res, res2, res3, res4]
            colorlist.sort(reverse=True)
            colorlist2 = colorlist.copy()
            colorlist2.sort()
            for i in range(3):
                hihihihaa = colorlist[i] - colorlist2[i]
                shademodifier = shademodifier + hihihihaa
            #print(shademodifier)
            #print(colorlist)
            shademodifier = math.ceil(shademodifier*10)
            
            
            #vittuu = len(pixelList) / 100
            for i in range(len(pixelList)):
                counter = 3

                shaderange = (shademodifier, shademodifier, shademodifier)
            
                if len(pixelList)-1 > i:
                    if tuple(map(sub, pixelList[i+1], shaderange)) < pixelList[i] <  tuple(map(add, pixelList[i+1], shaderange)):
                        counter = counter-1
                        #print("front")
                    
                if len(pixelList)-(width+1) > i:  

                    if tuple(map(sub, pixelList[i+width], shaderange)) < pixelList[i] <  tuple(map(add, pixelList[i+width], shaderange)):
                        counter = counter-1
                        #print("bottom")
                    
                
                    if tuple(map(sub, pixelList[i+width+1], shaderange)) < pixelList[i] <  tuple(map(add, pixelList[i+width+1], shaderange)):
                        counter = counter-1
                        #print("bottom right")  
            
                    
                if counter >= 2:
                        pixelList[i] = 0, 0, 0 #tarkotus olla 0, 0, 0
                        counter1 = counter1+1
                        if counter1 == 100:
                            #print(int(math.ceil(i / vittuu)),"%")
                            progress_bar(i, len(pixelList))
                            counter1 = 0
                #print(counter)
                #print(tuple(map(sub, pixelList[i+1], shaderange)), pixelList[i],  tuple(map(add, pixelList[i+1], shaderange)))
            #img.putdata(pixelList)
            #img.show()
            for i in range(len(pixelList)):
                i = i-1
                if pixelList[i] != (0, 0, 0): # 0, 0, 0
                    pixelList[i] = 255, 255, 255 #tarkotus olla 255, 255, 255
            frames[bruh].putdata(pixelList)
            
        subprocess.call("taskkill /f /im Microsoft.Photos.exe", shell=True)
        for i in range(len(frames)):
            time.sleep(1/FPS)
            frames[i].show()
    
        
    outliner()