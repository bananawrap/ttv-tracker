import copy
import time

from PIL import ImageGrab, Image, ImageChops, ImageDraw
from dataclasses import dataclass, field
from tqdm import tqdm


@dataclass
class Pattern:
    pixelAmount: int 
    patternPosList: list
    patternColorList: list

def main():
    input("press enter when img in clipboard")
    img = ImageGrab.grabclipboard()
    size = img.size
    width, height = size
    pixelList = [img.getpixel((x,y)) for y in range(height) for x in range(width)]
    imgMap = []
    posList = []
    blockList = []
    patternList = []
    counter = 0
    #look for patterns
    for pixel in range(len(pixelList)):
        try:
            if pixelList[pixel] != pixelList[pixel+1]:
                #patternList.append(pixelList[pixel])
                posList.append(pixel)
            else:
                posList.append(0)
        except IndexError:
            pass
    #separate patterns
    xoperator = 1
    yoperator = width
    for pixel in tqdm(range(len(posList))):
        if posList[pixel] not in blockList and posList[pixel] != 0:
            anchor = pixel
            pA = 0
            patternPosList = []
            patternColorList = []
            xpointer = copy.copy(anchor)
            ypointer = copy.copy(anchor)
            for i in range(anchor,len(pixelList)):
                try:
                    if posList[xpointer]+xoperator == posList[xpointer+xoperator] and xpointer not in blockList:
                        blockList.append(xpointer)
                        pA += 1
                        patternPosList.append(xpointer)
                        patternColorList.append(pixelList[xpointer])
                        xpointer +=1
                        #pixelList[posList[xpointer]] = (0,255,0)
                        counter += 1
                    elif posList[ypointer]+yoperator == posList[ypointer+yoperator] and ypointer not in blockList:
                        blockList.append(ypointer)
                        pA += 1
                        patternPosList.append(ypointer)
                        patternColorList.append(pixelList[ypointer])
                        ypointer +=width
                        #pixelList[posList[ypointer]] = (0,255,0)
                        counter += 1
                    else:
                        xpointer,ypointer = ypointer,xpointer
                        pass
                    
                    if ypointer in blockList and xpointer in blockList:
                        xoperator *= -1
                        yoperator *= -1
                        if ypointer in blockList and xpointer in blockList:
                            xoperator *= -1
                            yoperator *= -1
                            break
            
                    if not posList[xpointer]+xoperator == posList[xpointer+xoperator] and not posList[ypointer]+yoperator == posList[ypointer+yoperator]:
                        xoperator *= -1
                        yoperator *= -1
                        if not posList[xpointer]+xoperator == posList[xpointer+xoperator] and not posList[ypointer]+yoperator == posList[ypointer+yoperator]:
                            xoperator *= -1
                            yoperator *= -1
                            break
                        elif i > xpointer+10:
                            break
                    elif i > xpointer+10:
                        break
                except IndexError:
                    break
            patternList.append(Pattern(pA,patternPosList,patternColorList))
    patternList.sort(key=lambda x: x.pixelAmount, reverse=True)
    print(len(patternList))
    try:
        for pattern in patternList:
            for pattern2 in patternList:
                if pattern.pixelAmount == pattern2.pixelAmount:
                    if pattern.patternColorList == pattern2.patternColorList:
                        if not pattern.patternPosList == pattern2.patternPosList:
                            for j in pattern.patternPosList:
                                pixelList[j] = (0,255,0)

        #for a in range(len(patternList)):
        #    for j in patternList[a].patternPosList:
        #        pixelList[j] = (0,255,0)
    except IndexError:
        pass
    print(counter)
    img.putdata(pixelList)
    img.show()
    






if __name__=="__main__": 
    start = time.time()
    main()
    end = time.time()
    print(f"time: {(end-start)/60:.4f} minutes")
