from PIL import Image,ImageGrab,ImageDraw
from tqdm import tqdm


def main():
    input("press enter when img in clipboard")
    img = ImageGrab.grabclipboard()

    width, height = img.size
    pixelList = []
    posList = []

    for y in tqdm(range(height)):
        for x in range(width):
            indicator = x,y
            pixelList.append(img.getpixel(indicator))
            posList.append(indicator)     


    draw = ImageDraw.Draw(img)
    counter = width*50
    for pixel in tqdm(range(len(pixelList))):
        counter += 1
        try:
            #while True:
            #if not pixelList[pixel] == (0,0,0):
                if not pixelList[pixel] == pixelList[pixel+1]:
                    pI = pixelList.index(pixelList[pixel],counter)
                    draw.line(xy=[(posList[pixel]),(posList[pI])],fill=pixelList[pixel])
        except:
            pass
    
    img.show()

if __name__=="__main__": main()
