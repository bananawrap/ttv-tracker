import requests
import time
import playsound
import copy
import os
import logging
import json
import tqdm
import socket
import re
import inspect

from threading import Thread
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from win10toast import ToastNotifier
#from bs4 import BeautifulSoup

class TtvTracker():
    def __init__(self) -> None:
        self.ips = {
        "pc":"192.168.0.57",
        "pi":"192.168.0.77"
        }

        self.toast = ToastNotifier()

        self.TIMEDIFF = 3
        self.hour24 = [x for x in range(0,24)]
        self.WEEKSTR = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

        self.main_dir = os.path.split(os.path.abspath(__file__))[0]
        
        self.settings = self.loadsettings()
        
        self.commands = [
        "input",
        "results",
        "todaysresults",
        "data",
        "track",
        "cls",
        "set",
        "multitrack",
        "settings",
        ]


        
    
    """
    this code is for predicting the probability of a streamer going live at a certain time of day
    it uses a polynomial regression model to predict the probability of the stream starting
    the model is trained on data from the streamer's stream history
    """
        



    def makesave(self):
        monday =    [0 for x in range(0,24)]
        tuesday =   [0 for x in range(0,24)]
        wednesday = [0 for x in range(0,24)]
        thursday =  [0 for x in range(0,24)]
        friday =    [0 for x in range(0,24)]
        saturday =  [0 for x in range(0,24)]
        sunday =    [0 for x in range(0,24)]
        week = [monday,tuesday,wednesday,thursday,friday,saturday,sunday]
        alreadyStreamed = [False,0]
        data = {
                "week":week,
                "alreadyStreamed":alreadyStreamed
                }
        return data
    
    def makesettings(self):
        self.settings = {
            "channelname": f"{input('channelname: ')}",
            "authorization": "1234"
        }
        self.savesettings()

    def load(self, channelname): #load savefile function
        try:
            fullname = os.path.join(self.main_dir, f'{channelname}_data.json')
            with open(fullname, 'r') as file:
                data = json.load(file)
        except Exception as err:
            logging.error(err)
            print("failed to load. Check log.txt")
            if input(f"try to make a new save for {channelname}? y/n : ") == "y":
                self.save(self.makesave(), channelname)
                try:
                    with open(fullname, 'r') as file:
                        data = json.load(file)
                except Exception as err:
                    logging.error(err)
                    print(err)
                else:
                    return data
        
        else: 
            return data

    
    def save(self, data, channelname):
        fullname = os.path.join(self.main_dir, f'{channelname}_data.json')
        with open(fullname, 'w') as file:
            json.dump(data, file)
            
            
    def savesettings(self):
        for setting in self.settings:
            if self.settings[setting] in self.userscripts:
                isUserscript = True
            else:
                isUserscript = False
            self.settings[setting] = [self.settings[setting], isUserscript]
        fullname = os.path.join(self.main_dir, 'settings.json')
        with open(fullname, "w") as file:
            json.dump(self.settings,file)
        self.loadsettings()
            
            
    def loadsettings(self):
        try:
            self.userscripts = []
            fullname = os.path.join(self.main_dir, 'settings.json')
            with open(fullname, "r") as file:
                self.settings = json.load(file)
            try: 
                for setting in self.settings:
                    if isinstance(self.settings[setting], list):
                        if self.settings[setting][1]:
                            self.userscripts.append(self.settings[setting][0])
                        self.settings[setting] = self.settings[setting][0]
            except Exception:
                pass

        except Exception as err:
            logging.error(err),
            self.makesettings()
            with open(fullname, "r") as file:
                self.settings = json.load(file)


    def setTarget(self, channelname): 
        print(f"current target: {channelname}")
        try:
            userinput = {"channelname":input("set target: ")}
            if userinput["channelname"] != "":
                self.savesettings(userinput)
                return self.loadsettings()

            else:
                raise ValueError("empty name")
            
        except Exception as err:
            print(f"failure: {err}")
        


    def predict(self, currenthour, currentminute, ypoints):
        
        
        #polynominal regression module
        model = np.poly1d(np.polyfit(self.hour24,ypoints,deg=5))
        line = np.linspace(0,23,100)
        
        #we use the module to get a prediction for the current time
        if not sum(ypoints) == 0:
            prediction = round((model(currenthour+currentminute/60)/sum(ypoints)*100),1)
            return prediction, line, model
        else:
            return None, None, None


    def graph(self, isResList, data):
        #uses resList or current day for graph and predictions

        currentday, currenthour, currentminute = self.get_time()
        resList = self.update_reslist(data)
        week = data["week"]
        
        if not isResList:
            currentdaytxt = self.WEEKSTR[currentday]
            mode = week[currentday]
        else:
            mode = resList



        ypoints = mode
    
        prediction, line, model = self.predict(currenthour,currentminute,mode)
        print(f"current odds:{prediction}%")

        for j in range(len(self.hour24)):
            print(f"{str(j)}: {round((model(j)/sum(mode))*100,1)}%")

        print("accuracy:", r2_score(ypoints, model(self.hour24)))
        if not isResList:
            plt.title(currentdaytxt)
        plt.plot(self.hour24,ypoints)
        plt.plot(line,model(line))
        plt.grid()
        plt.show()
        

    def displaydata(self, data, channelname): # basically a fancy and a complicated way of centering the different outputs
        
        resList = self.update_reslist(data)
        week = data["week"]
        
        print(f"showing data for {channelname}")
        string = f"hour:  {' '*(len(self.WEEKSTR[2])-len('hour'))}"
        for j, hour in enumerate(self.hour24):
            string += f"{hour}  "
        print(f"{' '*round((len(string))/2)}/////DAYS/////")
        #print(f"hour:  {' '*(len(self.WEEKSTR[2])-len('hour'))}{self.hour24}")
        print(string)
        for i, day in enumerate(week):
            string = f"{self.WEEKSTR[i]}:  {' '*(len(self.WEEKSTR[2])-len(self.WEEKSTR[i]))}"
            for j, hour in enumerate(day):
                string += f"{hour}|{' '*len(str(self.hour24[j]))}"
            print(string)
        #print(f"{' '*round((len(self.WEEKSTR[2])+(24*3))/2)}/////TOTAL/////")
        print("")
        string = f"total:  {' '*(len(self.WEEKSTR[2])-len('total'))}"
        for j, hour in enumerate(resList):
            string += f"{hour}|{' '*len(str(self.hour24[j]))}"
        print(string)
                
            
    def datainput(self, data, channelname): #manually add logs to database
        
        week = data["week"]
        run = True
        x = False
        while run:
            
            dayInput = input("day: ")
            for d in range(7):
                for lenght in range(1,self.WEEKSTR[d].__len__()):
                    if dayInput == self.WEEKSTR[d][:lenght]:
                        day = week[d]
                        x = True
                        break
                    elif d == 6:
                        run = False
                        break
                if x:
                    x = False
                    break
            while run:
                try:
                    hour = int(input("hour: "))
                    day[hour] +=1
                    data["week"] = week
                    self.save(data, channelname)   
                except Exception:
                    break
                
            

    def clear(self):
        if os.name=="nt":
            os.system("cls")
        else:
            os.system('clear')
            
        
    def check_port(self, ip,port): 
        try:
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            c.settimeout(2)
            c.connect((ip, port))
            c.close()
            return True
        except socket.error:
            return False
    
            
    def sync(self, data, channelname, silent=False):
        
        resList = self.update_reslist(data)
        totalsum = sum(resList)
        
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 1024
        
        port = 5785
        
        authorization = self.settings["authorization"]
        
        s = socket.socket()
        
        if not silent: print(f"[+] Connecting to {self.ips['pi']}:{port}")
        s.connect((self.ips["pi"], port))
        if not silent: print("[+] Connected.")

        s.send(f"{authorization}{SEPARATOR}{channelname}{SEPARATOR}{totalsum}".encode())
        
        message = s.recv(BUFFER_SIZE).decode()
        
        if message == "2":
            received = s.recv(BUFFER_SIZE).decode()
            filename, filesize = received.split(SEPARATOR)
            filename = os.path.basename(filename)
            filesize = int(filesize)
            

            if not silent: progress = tqdm.tqdm(range(filesize), f"[+] Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "wb") as f:
                while True:

                    bytes_read = s.recv(BUFFER_SIZE)
                    if not bytes_read:    
                        break

                    f.write(bytes_read)
                    if not silent: progress.update(len(bytes_read))
                    
                s.close()
                if not silent: print("")
            
        elif message == "1":
            filename = f"{channelname}_data.json"
            filesize = os.path.getsize(filename)
            
            s.send(f"{filename}{SEPARATOR}{filesize}".encode())
            time.sleep(1)
            if not silent: progress = tqdm.tqdm(range(filesize), f"[+] Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                while True:

                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:

                        break

                    s.sendall(bytes_read)

                    progress.update(len(bytes_read))
            s.close()
            if not silent: print("")
        elif message == "0":
            s.send("".encode())
            s.close()
            if not silent: print(f"[+] {channelname} data is already synced")
            return
        else:
            if not silent: print(f"[+] server message: {message}")
        
    def get_time(self):
        currenttime = time.struct_time(time.localtime())
        currentminute = currenttime[4]
        currenthour = currenttime[3]
        currentday = currenttime[6]
        return currentday, currenthour, currentminute

    def get_title(self, contents):
        title = ""
        try:
            index = contents.find('description" content="') #len 22
            index += 22
            end_index = contents.find('"',index)
            for char in range(index, end_index):
                title += contents[char]
        except Exception:
            pass

        return title

    def get_startdate(self, contents):
        starthour = ""
        try:
            index = contents.find('startDate":"') #len 12
            if index == -1:
                return index
            index += 12
            index = contents.find('T',index)
            index += 1
            end_index = contents.find(':',index)
            for num in range(index,end_index):
                starthour += contents[num]
            starthour = int(starthour)
        except Exception:
            pass
        else:
            return starthour

    def update_reslist(self, data):
        week = data["week"]
        resList = []
        combinedDays = [0 for x in range(0,24)]
        for i in range(len(combinedDays)):
            resList.append(combinedDays[i]+week[0][i]+week[1][i]+week[2][i]+week[3][i]+week[4][i]+week[5][i]+week[6][i])
        return resList

    def get_stream(self, channelname):
        return requests.get('https://www.twitch.tv/' +channelname).content.decode('utf-8')  #startdate -3 hour diff

    def get_accuracy(self, data):
        return r2_score(self.update_reslist(data), self.predict(self.get_time()[1], self.get_time()[2], self.update_reslist(data))[2](self.hour24))
    
    def check_internet(self):
        return self.check_port("google.com",80)

    def track(self, data, channelname):
        """
        checks if tracked streamer goes live and adds it into database
        also displays prediction on streamer going live with the database and polynominal regression module
        """
        
        antenna = r"""
        ,-.
        / \  `.  __..-,O
        :   \ --''_..-'.'
        |    . .-' `. '.
        :     .     .`.'
        \     `.  /  ..
        \      `.   ' .
        `,       `.   \
        ,|,`.        `-.\
        '.||  ``-...__..-`
        |  |
        |__|
        /||\
        //||\\
        // || \\
    __//__||__\\__
    '--------------'"""
        
        week = data["week"]
        alreadyStreamed = data["alreadyStreamed"]
        resList = self.update_reslist(data)
        
        try:
            if self.check_port(self.ips["pi"],5785):
                self.sync(data, channelname)
                data = self.load(channelname)
                time.sleep(5)
        except Exception as err:
            print(err)
            logging.error(err)
            time.sleep(5)
        
        streamEndHour = 0
        live = True
        while True:
            try:

                self.clear()
                
                print(antenna)
                
                currentday, currenthour, currentminute = self.get_time()

                #updates alreadyStreamed to current day
                if alreadyStreamed[0] == True and alreadyStreamed[1] != currentday and live == False:
                    alreadyStreamed = [False,currentday]
                    self.save(data, channelname)
                    
                #request stream data from twitch
                contents = requests.get('https://www.twitch.tv/' +channelname).content.decode('utf-8')  #startdate -3 hour diff
                
                #search for stream title
                title = self.get_title(contents)
                
                #check stream startTime for verification
                starthour = self.get_startdate(contents)

                #see if streamer is online, also avoid misinput if streamed already
                if 'isLiveBroadcast' in contents and starthour != -1: 
                    if live == False:
                        if alreadyStreamed[0] == False:
                            #verifies if the stream has started in the past hour to avoid false positives
                            if self.hour24[currenthour-self.TIMEDIFF] == starthour or self.hour24[currenthour+1-self.TIMEDIFF] == starthour:
                                playsound.playsound("auughhh.mp3")

                                #log it to the data list
                                week[currentday][currenthour] +=1
                                
                                #set the already streamed flag to true
                                alreadyStreamed = [True,currentday]

                                #confirm that the stream is live
                                live = True

                                #pack the information into a data dictionary and self.save it to (channelname)_data.json
                                data["week"] = week
                                data["alreadyStreamed"] = alreadyStreamed
                                self.save(data, channelname)
                                
                                resList = self.update_reslist(data)
                                
                                
                                logging.info("stream started")
                                
                                #show a windows toast
                                self.toast.show_toast(
                                f"{channelname} went live!",
                                f"{title}",
                                duration = 20,
                                icon_path = "pythowo.ico",
                                threaded = True,
                                )
                            else:
                                #weird mystery bug which has been badly patched
                                logging.info(f"avoided misinput: {self.hour24[currenthour-self.TIMEDIFF]} != {starthour} ")
                                
                #prediction
                prediction,line,model = self.predict(currenthour,currentminute,resList)
                
                if 'isLiveBroadcast' in contents:
                    print(f"{channelname} is live! \ntitle: {title}",end="\r")
                    alreadyStreamed = [True,currentday]
                    data["week"] = week
                    data["alreadyStreamed"] = alreadyStreamed
                    streamEndHour = copy.copy(currenthour)
                    self.save(data, channelname)
                
                elif alreadyStreamed[0] == True and alreadyStreamed[1] == currentday and live == False:
                    if "streamEndHour" in locals():
                        print(f"{channelname} already streamed today at {streamEndHour} \noverall probability: {prediction}%",end="\r")
                    else:
                        print(f"{channelname} already streamed today \noverall probability: {prediction}%",end="\r")
                else:
                    print(f"{channelname} is not live \noverall probability: {prediction}%",end="\r")
                    if live and "streamEndHour" in locals():
                        if streamEndHour != currenthour:
                            live = False
                    else:
                        live = False
                
                try:
                    if 60/model(currenthour) < 10000000 and prediction != None:
                        time.sleep(60/model(currenthour))
                    else:
                        time.sleep(60)
                except TypeError:
                    time.sleep(60)
                        
            except KeyboardInterrupt:
                    self.clear()
                    break
                
            except Exception as err:
                logging.exception(err)
                

    def track_lite(self, data, channelname):
        """
        checks if tracked streamer goes live and adds it into database
        also displays prediction on streamer going live with the database and polynominal regression module
        """
        
        
        week = data["week"]
        alreadyStreamed = data["alreadyStreamed"]
        resList = self.update_reslist(data)
        
        try:          
            currentday, currenthour, currentminute = self.get_time()

            #updates alreadyStreamed to current day
            if alreadyStreamed[0] == True and alreadyStreamed[1] != currentday:
                alreadyStreamed = [False,alreadyStreamed[1]]
                data["alreadyStreamed"] = alreadyStreamed
                self.save(data, channelname)
                
            #request stream data from twitch
            contents = self.get_stream(channelname)

            #search for stream title
            title = self.get_title(contents)
                
                
            #check stream startTime for verification
            starthour = self.get_startdate(contents)

            #see if streamer is online, also avoid misinput if streamed already
            if starthour != None:
                if 'isLiveBroadcast' in contents and starthour != -1: 
                    if alreadyStreamed[0] == False:
                        #verifies if the stream has started in the past hour to avoid false positives
                        if self.hour24[currenthour-self.TIMEDIFF] == starthour or self.hour24[currenthour+1-self.TIMEDIFF] == starthour:
                            #log it to the data list
                            week[currentday][currenthour] +=1
                            #set the already streamed flag to true
                            alreadyStreamed = [True,currentday]
                            #confirm that the stream is live
                            live = True
                            #pack the information into a data dictionary and self.save it to (channelname)_data.json
                            data["week"] = week
                            data["alreadyStreamed"] = alreadyStreamed
                            self.save(data, channelname)
                                
                            resList = self.update_reslist(data)
                                
                                
                            logging.info(f"{channelname} stream started") # log into log.txt
                            #show a windows toast
                            self.toast.show_toast(
                            f"{channelname} went live!",
                            f"{title}",
                            duration = 20,
                            icon_path = "pythowo.ico",
                            threaded = True,
                            )
                        else:
                            #weird mystery bug which has been badly patched
                            logging.info(f"avoided misinput: {self.hour24[currenthour-self.TIMEDIFF]} != {starthour} ")
                            
            #prediction
            prediction,line,model = self.predict(currenthour,currentminute,resList)
            
            if 'isLiveBroadcast' in contents:
                live = True
                alreadyStreamed = [True,currentday]
                data["week"] = week
                data["alreadyStreamed"] = alreadyStreamed
                self.save(data, channelname)
            else:
                live = False
            
            return data, prediction, live
        except Exception as err:
            logging.exception(err)    
            

    def multitrack(self, autoplay=False):
        accuracyratings = ["bad", "decent", "good", "very good"]
        listeners = {}
        message = ""
        while True:
            self.clear()
            print("multitrack paused")
            print(f"listeners: {len(listeners)}")
            print(f"{message}")
            message = ""
            print("")
            userinput = ""
            if not autoplay: userinput = input("=> ")
            
            if "add" in userinput.split(" ")[0]:
                if not self.findword("all")(userinput):
                    channelname = userinput.split(" ")[1]
                    listeners[channelname] = self.load(channelname)
                    message = f"{channelname} added"
                else:
                    for channelname in self.find_savefiles():
                        listeners[channelname] = self.load(channelname)
                        message += f"{channelname} added\n"
                
                
            elif "rm" in userinput.split(" ")[0]:
                channelname = userinput.split(" ")[1]
                listeners.pop(channelname)
                message = f"{channelname} removed"
            
            elif "back" in userinput:
                break
            
            elif "show" in userinput:
                for listener in listeners:
                    message += f"{listener}\n"
            
            elif "play" in userinput or autoplay:
                if autoplay:
                    for channelname in self.find_savefiles():
                        listeners[channelname] = self.load(channelname)
                        message += f"{channelname} added\n"
                    autoplay = False
                message = ""
                for streamer in listeners:
                    try:
                        if self.check_port(self.ips["pi"],5785):
                            self.sync(listeners[streamer], streamer)
                            time.sleep(5)
                    except ConnectionError:
                        print("no internet")
                    except Exception as err:
                        logging.error(err)
                        time.sleep(5)
                
                while True:
                    try:
                        self.clear()
                        print("multitrack playing (ctrl + c) to pause")
                        print(f"active listeners: {len(listeners)}")
                        print(f"{message}")
                        
                        for streamer in listeners:
                            listeners[streamer] = self.load(streamer)

                        for streamer in listeners:
                            streaminfo = self.track_lite(listeners[streamer],streamer)
                            streaminfo = { 
                                        "data":streaminfo[0], 
                                        "prediction":streaminfo[1], 
                                        "live":streaminfo[2], 
                                        }
                            try:
                                accuracyrating = accuracyratings[round(self.get_accuracy(streaminfo["data"])*100/25)]
                            except Exception:
                                accuracyrating = "none"
                            
                            self.save(streaminfo["data"], streamer)
                            print(f"{'-'*os.get_terminal_size()[0]}")
                            print(f"streamer: {streamer}")
                            print(f"live: {streaminfo['live']}")
                            if streaminfo["live"]:
                                print(f"title: {self.get_title(self.get_stream(streamer))}")
                            else:
                                print(f"probability of a stream: {streaminfo['prediction']}%")
                                print(f"prediction accuracy is {accuracyrating}")
                                print(f"last stream on {self.WEEKSTR[streaminfo['data']['alreadyStreamed'][1]]}")
                        time.sleep(60)
                            
                            
            
                    except KeyboardInterrupt:
                        break
                    except Exception as err:
                        logging.error(err)
                        message = "an error occured during tracking. Check log.txt"
                        
            elif "help" in userinput:
                message += "usage: first do 'add streamername' and then 'play'\n"
                message += "commands:\n"
                for command in [
                "add",
                "rm",
                "back",
                "show",
                "play",  
                ]: message += f"{command}\n"
                
    def find_savefiles(self):
        path = self.main_dir
        name = "_data.json"
        result = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if name in file:
                    result.append(file.replace(name,""))
        return result

    def findword(self, w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

    def settings_manager(self):
        message = ""
        while True:
            self.clear()
            print("settings manager\n")
            print(f"{message}")
            for i, setting in enumerate(self.settings):
                if self.settings[setting] in self.userscripts:
                    print(f"{i+1}. {setting}: {self.settings[setting]} (userscript)")
                else:
                    print(f"{i+1}. {setting}: {self.settings[setting]}")
            message = ""
            print("")
            userinput = input("=> ")
            
            if "set" in userinput.split(" ")[0]:
                    self.settings[userinput.split(" ")[1]] = userinput.split(" ")[2]
                    self.savesettings()
                    message = f"{userinput.split(' ')[1]} set with the value of {userinput.split(' ')[2]}"
                
                
            elif "rm" in userinput.split(" ")[0]:
                self.settings.pop(userinput.split(" ")[1])
                message = f"{userinput.split(' ')[1]} removed"
            
            elif "userscript" in userinput.split(" ")[0]:
                value = userinput.replace(userinput.split(" ")[0],"").strip()
                value = value.replace(value.split(" ")[0],"").strip()
                self.settings[userinput.split(" ")[1]] = value
                self.userscripts = value
                self.savesettings()
                message = f"{userinput.split(' ')[1]} set with the value of {value}"
            
            elif "back" in userinput:
                break
                
            elif "help" in userinput:
                message += "usage: command + settingname + value\n"
                message += "usercript lets you run a piece of code every iteration\n"
                message += "commands:\n"
                for command in [
                "set",
                "rm",
                "back",  
                "userscript"
                ]: message += f"{command}\n"
            

    def main(self):

        #setting up logs and disabling unnecessary loggers
        logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
        logging.getLogger("urllib3.util.retry").disabled = True
        logging.getLogger("urllib3.util").disabled = True
        logging.getLogger("urllib3").disabled = True
        logging.getLogger("urllib3.connection").disabled = True
        logging.getLogger("urllib3.response").disabled = True
        logging.getLogger("urllib3.connectionpool").disabled = True
        logging.getLogger("urllib3.poolmanager").disabled = True
        logging.getLogger("requests").disabled = True

        self.loadsettings()
        channelname = self.settings["channelname"]
        
        for script in self.userscripts:
            try:
                exec(script)
            except Exception as err:
                print(f"error in userscript: {err}")
            
        while True:
            try:
                data = self.load(channelname)
                
                userinput = input("=> ")
                if userinput == "input":
                    self.datainput(data, channelname)
                
                    
                elif userinput == "data":
                    self.displaydata(data, channelname)
                    
                    
                elif userinput == "todaysresults":
                    self.graph(False, data)
                
                
                elif userinput == "results":
                    self.graph(True, data)
                
                
                elif userinput == "cls":
                    self.clear()
                    
                    
                elif userinput == "help":
                    
                    for command in self.commands:
                        print(command)
                    
                    
                elif self.findword("set")(userinput.split(" ")[0]):
                    channelname = userinput.split(" ")[1]
                    data = self.load(channelname)
                    self.settings["channelname"] = channelname
                    self.savesettings()
                    self.save(data, channelname)
                    self.settings = self.loadsettings()


                elif userinput == "multitrack":
                    if self.check_internet: self.multitrack()
                    else: print("no internet")
                
                
                elif userinput == "track":
                    if self.check_internet: self.track(data, channelname)
                    else: print("no internet")
                    
                elif userinput == "savefiles":
                    for self.savefile in self.find_self.savefiles():
                        print(self.savefile)
                
                elif userinput == "settings":
                    self.settings_manager()
                
                
                #simple console
                else:
                    try:
                        exec(userinput)
                    except Exception as err:
                        if userinput == "exit":
                            break
                        else:
                            print(f"ran into a problem, try help. error: {err}")
            except IndexError:
                print("set needs streamer's twitch name")
                
            except Exception as err:
                print(err)
                
                    
                

if __name__=="__main__": 
    
    tracker = TtvTracker()
    tracker.main()
