
import requests
import json
from bs4 import BeautifulSoup

class TwitchParser():
    def __init__(self) -> None:
        pass


    def get_stream(self, channelname):
        return BeautifulSoup(requests.get('https://www.twitch.tv/' +channelname).content.decode('utf-8'),"html.parser")

    def is_live(self, contents):
        try:
            (contents.head.find("script", attrs={"type":"application/ld+json"}).contents)[0]
            return True
        except Exception:
            return False

    def get_stream_info(self, contents):
        if self.is_live(contents):
            return json.loads((contents.head.find("script", attrs={"type":"application/ld+json"}).contents)[0])[0]
            

    def get_title(self, contents):
        return contents.head.find("meta", attrs={"property":"og:description"})["content"]
         

    def get_startdate(self, contents):
        if self.is_live(contents):
            full_time = self.get_stream_info(contents)["publication"]["startDate"]
            
            date = full_time.split("T")[0]
            hour = full_time.split("T")[1].split(":")[0]
            minute = full_time.split("T")[1].split(":")[1]
            
            start_time = {"date": date, 
                          "hour": hour, 
                          "minute": minute
            } 
            
            return start_time
        return None
