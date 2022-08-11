from PIL import Image, ImageGrab, ImageDraw, ImageFilter
import math
import time
from tqdm import tqdm
indicator = x, y = 0, 0
time.sleep(2)
img = ImageFilter.SHARPEN
input("press enter when ready")
img = ImageGrab.grabclipboard()
width = img.size[0]
height = img.size[1]
print(width, height)
pixelList = []
counter = 0

for y in range(height):
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
        pixelList.append(img.getpixel(indicator))
        
print("opening final image")
img.putdata(pixelList)
#print(indicator)
#img.show()

def outliner():
    global pixelList
    counter = 0
    for i in tqdm(range(len(pixelList))):
        counter = 0
        
        if len(pixelList)-1 > i:
            if pixelList[i] != pixelList[i+1]:
                counter = counter+1
                #print("front")

        if len(pixelList)-(width+1) > i:  

            if pixelList[i] != pixelList[i+width]:
                counter = counter+1
                #print("bottom")
            
        
            if pixelList[i] != pixelList[i+width+1]:
                counter = counter+1
                #print("bottom right")

            
            if pixelList[i] != pixelList[i+width-1]:
                counter = counter+1
                #print("bottom left")

            
        if counter >= 3:
                pixelList[i] = 0, 0, 0 #tarkotus olla 0, 0, 0

        #print(counter)
    img.putdata(pixelList)
    img.show()
    for i in range(len(pixelList)):
        i = i-1
        if pixelList[i] != (0, 0, 0): # 0, 0, 0
            pixelList[i] = 255, 255, 255 #tarkotus olla 255, 255, 255
    img.putdata(pixelList)
    img.show()
outliner()