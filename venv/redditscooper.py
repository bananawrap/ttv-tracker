from PIL import Image

import praw
import requests
import re
import io
import os


reddit_read_only = praw.Reddit(client_id="Ic7vVFYyBNw_-dQ3Yre5RQ",
                          client_secret="YJetdenm8HpRJEH8Umj18wn0TYYIWA",
                          user_agent="scraper for imageprocessing u/tollofin"
                                    )

def setSubreddit(name):
    return reddit_read_only.subreddit(name)

def hotImgScoop(subreddit,limit):
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, "output")
    postList = subreddit.hot(limit=limit)
    imgList = []
    for post in postList:
        url = (post.url)
        file_name = url.split("/")
        if len(file_name) == 0:
            file_name = re.findall("/(.*?)", url)
        file_name = file_name[-1]
        if "." not in file_name:
            file_name += ".jpg"
        if ".gif" not in file_name:
            print(file_name)
            r = requests.get(url)
            r.raw.decode_content = True
        try:
            img = Image.open(io.BytesIO(r.content))
            imgList.append([img,file_name])
        except:
            #to skip non image ones
            pass
    return imgList


def main():
    subreddit = reddit_read_only.subreddit("cursedimages")
    postList = subreddit.hot(limit=5)
    imgList = []
    for post in postList:
        url = (post.url)
        file_name = url.split("/")
        if len(file_name) == 0:
            file_name = re.findall("/(.*?)", url)
        file_name = file_name[-1]
        if "." not in file_name:
            file_name += ".jpg"
        print(file_name)
        r = requests.get(url)
        r.raw.decode_content = True
        imgList.append(r.content)
    
    img = Image.open(io.BytesIO(imgList[0]))
    img.show()

if __name__=="__main__": main()