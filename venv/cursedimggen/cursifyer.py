import redditscooper
from tqdm import tqdm
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "output")

subreddit = redditscooper.setSubreddit(input("subreddit:"))

imgList = redditscooper.hotImgScoop(subreddit,int(input("amount:")))
for img in imgList:
    size = img[0].size
    width, height = size
    pixelList = [img[0].getpixel((x,y)) for y in range(height) for x in range(width)]
    counter = 0
    for i in tqdm(range(len(pixelList))):
        counter = 0
        
        if len(pixelList)-1 > i:
            if pixelList[i] != pixelList[i+1]:
                counter = counter+1
                #front


        if len(pixelList)-(width+1) > i:  
            if pixelList[i] != pixelList[i+width]:
                counter = counter+1
                #bottom
        
            if pixelList[i] != pixelList[i+width+1]:
                counter = counter+1
                #bottom right

            if pixelList[i] != pixelList[i+width-1]:
                counter = counter+1
                #bottom left

            
        if counter >= 4:
                pixelList[i] = 0, 0, 0
        else:
            pixelList[i] = 255, 255, 255
    img[0].putdata(pixelList)
    img[0].save(os.path.join(data_dir, img[1]))
    