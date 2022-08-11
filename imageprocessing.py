from PIL import Image, ImageGrab, ImageDraw, ImageFilter, ImageColor
import math
import time
from operator import sub, add, floordiv
import statistics
import urllib.request,io
from tqdm import tqdm
indicator = x, y = 0, 0
time.sleep(2)
img = ImageFilter.SHARPEN
png = '.png'
userinput = input("screenshot, URL, clipboard (s / u / c): ")
if userinput == "u":
    url = input("Image URL: ")
    try:
        path = io.BytesIO(urllib.request.urlopen(url).read())
        img = Image.open(path)
    except OSError:
        print("joo ei toi toiminu :( otetaanks sit screenshot vai clipboard")
        userinput = input("(s / c / kys)")
        if userinput == "s":
            img = ImageGrab.grab()
        elif userinput == "c":
                img = ImageGrab.grabclipboard()
        else:
            quit()
elif userinput == "s":
    img = ImageGrab.grab()
elif userinput == "c":
        img = ImageGrab.grabclipboard()
try:
    width = img.size[0]
except:
    print("vitun idiootti")
    time.sleep(1)
    print("homo")
    time.sleep(1)
    print("kato mitä sä teit")
    time.sleep(1)
height = img.size[1]
print(width, height)
pixelList = []
counter = 0



for y in tqdm(range(height)):
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
        
        
with open("image.txt", "w") as output:
    output.write(str(pixelList))
print("opening image")
print("starting processing soon...")

def outliner():
    global pixelList

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
    #getting 2 lists of pixels
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
    #print(colorlist)
    print(shademodifier)
    shademodifier = round(shademodifier*10,2)
    #shademodifier *=10
    userinput = input("käytetäänkö automatisoitua asetusta (" + str(shademodifier) + ") vai vaihdetaanko. (y / n): ")
    if userinput == "y": 
        try:
            shademodifier = int(input("no pistä: "))
        except:
            print("hei vitun homo et yritä tollasta, ei sitte vaiheta")
    print(shademodifier)
    time.sleep(1)
    
    #vittuu = len(pixelList) / 100
    for i in tqdm(range(len(pixelList))):
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
                 
            if tuple(map(sub, pixelList[i+width-1], shaderange)) < pixelList[i] <  tuple(map(add, pixelList[i+width-1], shaderange)):
                counter = counter-1
                #print("bottom left")  
    
            
        if counter >= 3:
                pixelList[i] = 0, 0, 0 #tarkotus olla 0, 0, 0
                pixelList[i-1]      = 20, 20, 20
                pixelList[i-width]  = 20, 20, 20
                try:
                    pixelList[i+1]      = 20, 20, 20
                    pixelList[-i+width] = 20, 20, 20
                except IndexError:
                    pass
                
                counter1 = counter1+1
                if counter1 == 100:
                    #print(int(math.ceil(i / vittuu)),"%")
                    counter1 = 0
        #print(counter)
        #print(tuple(map(sub, pixelList[i+1], shaderange)), pixelList[i],  tuple(map(add, pixelList[i+1], shaderange)))
    img.putdata(pixelList)
    img.show()
    for i in range(len(pixelList)):
        i = i-1
        if pixelList[i] != (0, 0, 0): # 0, 0, 0
             pixelList[i] = 255, 255, 255 #tarkotus olla 255, 255, 255
    img.putdata(pixelList)
    img.show()
    
outliner()