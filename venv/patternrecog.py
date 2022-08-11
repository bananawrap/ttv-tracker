from PIL import ImageGrab, ImageDraw
from tqdm import tqdm
import random
from statistics import mode

def randcolor(start=0, end=255):
    color = random.randint(start,end), random.randint(start,end), random.randint(start,end)
    return color



def main():
    input("press enter when img in clipboard")
    img = ImageGrab.grabclipboard()
    pixelList = []
    blocklist = []
    width, height = img.size
    for y in tqdm(range(height)):
        for x in range(width):
            indicator = x,y
            pixelList.append(img.getpixel(indicator))
    backround = mode(pixelList)
    for pixel in tqdm(range(len(pixelList))):
        pointer = pixel
        try:
            if pixelList[pixel] != pixelList[pixel+1]:
                pointer +=1
                pattern = []
                loopCap = 1000000
                while not pixelList[pointer] == backround and pointer not in blocklist:
                    #if  pixelList[pointer] == pixelList[pointer+width]:
                    #    #pixelList[pointer] = 0,255,0
                    #    pattern.append(pointer)
                    #    pointer +=width
                    #elif  pixelList[pointer] == pixelList[pointer+1]:
                    #    #pixelList[pointer] = 0,255,0
                    #    pattern.append(pointer)
                    #    pointer +=1
                    #else:
                    #    pointer +=pixel+1
                    #print("pixel:",pixel,"pointer:",pointer, end="\r")
                    down = False
                    up = False
                    left = False
                    right = False
                    activedirections = []

                    if  pixelList[pointer] == pixelList[pointer+width] and pointer+width not in pattern and not pixelList[pointer+width] == backround and pointer+width not in blocklist:
                        down = "down"
                        activedirections.append(down)
                    if  pixelList[pointer] == pixelList[pointer-width] and pointer-width not in pattern and not pixelList[pointer-width] == backround and pointer-width not in blocklist:
                        up = "up"
                        activedirections.append(up)
                    if  pixelList[pointer] == pixelList[pointer-1] and pointer-1 not in pattern and not pixelList[pointer-1] == backround and pointer-1 not in blocklist:
                        left = "left"
                        activedirections.append(left)
                    if  pixelList[pointer] == pixelList[pointer+1] and pointer+1 not in pattern and not pixelList[pointer+1] == backround and pointer+1 not in blocklist:
                        right = "right"
                        activedirections.append(right)
                    try:
                        choice = random.choice(activedirections)
                    except:
                        break
                    if choice == "down":
                        blocklist.append(pointer)
                        pattern.append(pointer)
                        pointer +=width
                    elif choice == "up":
                        blocklist.append(pointer)
                        pattern.append(pointer)
                        pointer -=width
                    elif choice == "left":
                        blocklist.append(pointer)
                        pattern.append(pointer)
                        pointer -=1
                    elif choice == "right":
                        blocklist.append(pointer)
                        pattern.append(pointer)
                        pointer +=1
                    loopCap -=1
                    if loopCap <= 0:
                        break

                    


                
                for i in range(len(pixelList)):  
                    if i == 0:
                        i = pixel
                    #print(i,end="\r")
                    if pixelList[i] == pixelList[pattern[0]]:
                        counter = 0
                        pattern1 = []
                        for j in range(len(pattern)):
                            if pixelList[i] == pixelList[pattern[j]]:
                                counter +=1
                                pattern1.append(i)
                                i +=1
                            elif pixelList[i+(pattern[j+1]-pattern[j])] == pixelList[pattern[j]]:
                                i +=pattern[j+1]-pattern[j]
                            if counter-1 <= len(pattern) <= counter+1:
                                for l in range(len(pattern1)):
                                    pixelList[pattern1[l]] = 0,255,0
        except:
            pass
    img.putdata(pixelList)
    img.show()
    



if __name__=="__main__": 
    main()


