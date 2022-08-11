from PIL import Image, ImageGrab, ImageDraw, ImageColor
import time
from threading import *
import copy
from tqdm import tqdm
from operator import sub, add, floordiv

#detect = False

ready_img_start = False
ready_img_end = False
img_start, img_end = ImageGrab.grab(), ImageGrab.grab()
images = [img_start, img_end]
pixelList_img_start = []
pixelList_img_end = []
pixeldiff1 = []
pixeldiff2 = []
pixelpos1 = []
pixelpos2 = []
vittu = 0




def askinput():
    global userinput, width, height, img_start, img_end
    userinput = input("screenshot, clipboard (s / c): ")
    if userinput == "s":
        img = ImageGrab.grab()
        width = img.size[0]
        height = img.size[1]
    elif userinput == "c":
        img_start = ImageGrab.grabclipboard()
        print("//image sizes must be the same//")
        input("enter when second image ready")
        img_end = ImageGrab.grabclipboard()
        width = img_start.size[0]
        height = img_start.size[1]
    input("press enter to continue")
    detection()

def detection():
    global width, height, img_start, img_end
    #while True:
    shaderange = (127,127,127)
    if userinput == "s":
        img_start = ImageGrab.grab()
    t1.start()
    if userinput == "s":
        time.sleep(2)
        img_end = ImageGrab.grab()
    t2.start()
    while not ready_img_start or not ready_img_end:
        time.sleep(1)
                            #//rotuerottelu//#
        if ready_img_start and ready_img_end:
            pixelList_final = copy.copy(pixelList_img_end)
            for pixel in tqdm(range(len(pixelList_img_start)),desc="searching for differences"):
                if pixelList_img_start[pixel] != pixelList_img_end[pixel]:
                    pixeldiff1.append(pixelList_img_start[pixel])
                    pixelpos1.append(pixel)
            pixel = 0
            for pixel in tqdm(range(len(pixelList_img_end)),desc="searching for differences"):
                if pixelList_img_end[pixel] != pixelList_img_start[pixel]:
                    pixeldiff2.append(pixelList_img_end[pixel])
                    pixelpos2.append(pixel)
            pixel = 0
            for pixel in tqdm(range(len(pixeldiff2)),desc="coloring"):
                    
                    pixel1 = pixeldiff2[pixel]
                    pixel1 = list(pixel1)
                    
                    for i in range(len(pixel1)):
                        pixel1[1] += 10

                    pixel1 = tuple(pixel1)
                    #pixeldiff2[pixel] = pixel1
                    #pixelList_img_start[pixelpos2[pixel]] = pixeldiff2[pixel]
            pixel = 0
            for pixel in tqdm(range(len(pixeldiff2)),desc="creating final img"):
                if tuple(map(sub, pixeldiff1[pixel], shaderange)) < pixeldiff2[pixel] < tuple(map(add, pixeldiff1[pixel], shaderange)):
                    #pixelList_final[pixelpos1[pixel]] = pixelList_img_start[pixelpos1[pixel]]
                    pixelList_final[pixelpos1[pixel]] = 0,255,0

                if not tuple(map(sub, pixeldiff1[pixel], shaderange)) < pixeldiff2[pixel] < tuple(map(add, pixeldiff1[pixel], shaderange)):
                    #pixelList_final[pixelpos1[pixel]] = pixelList_img_end[pixelpos2[pixel]]
                    pixelList_final[pixelpos1[pixel]] = 255,0,0


    
    
    img_start.putdata(pixelList_final)
    img_start.show()
            

                

        
def image_scan1():
    global ready_img_start, width, height, img_start, img_end
    for y in tqdm(range(height),desc="creating list of pixels for img1"):
        for x in range(width):
            indicator = x, y
            pixelList_img_start.append(img_start.getpixel(indicator))
    ready_img_start = True
    return pixelList_img_start

def image_scan2():
    global ready_img_end, width, height, img_start, img_end
    for y in tqdm(range(height),desc="creating list of pixels for img2"):
        for x in range(width):
            indicator = x, y
            pixelList_img_end.append(img_end.getpixel(indicator))
    ready_img_end = True
    return pixelList_img_end
        
t1 = Thread(target=image_scan1)
t2 = Thread(target=image_scan2)

askinput()

