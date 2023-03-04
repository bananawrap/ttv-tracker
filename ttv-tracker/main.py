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

from telegramBot import TelegramBot
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from win10toast import ToastNotifier
from bs4 import BeautifulSoup

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
        self.data_dir = os.path.join(self.main_dir, "data")
        
        self.logo = os.path.join(self.data_dir, 'pythowo.ico')
        self.soundalert = os.path.join(self.data_dir, 'auughhh.mp3')
        
        self.settings = self.load_settings()
        
        
        self.commands = {
        "COMMAND":"DESCRIPTION",
        "input":"allows the user to input new data into the selected streamer's savefile.",
        "results":"displays a graph of the data saved in the selected savefile.",
        "todaysresults":"displays a graph of the data saved in the selected savefile for the current day.",
        "data":"displays the raw data saved in the selected savefile.",
        "track":"allows the user to track the selected Twitch channel and save data about it.",
        "multitrack":"allows the user to track multiple Twitch channels simultaneously.",
        "cls":"clears the console window.",
        "set":"allows the user to select the Twitch channel to track. Usage: set (channelname)",
        "settings":"allows the user to view and modify program settings.",
        "savefiles":"displays a list of available savefiles",
        "exit":"self explanatory",
        }


        
    
    """
    this code is for predicting the probability of a streamer going live at a certain time of day
    it uses a polynomial regression model to predict the probability of the stream starting
    the model is trained on data from the streamer's stream history
    """
        



    def make_save(self):
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
    
    def make_settings(self):
        self.settings = {
            "channelname": f"{input('channelname: ')}",
            "authorization": "ChangeMe",
            "telegram_bot_enabled": False,
            "telegram_bot_API": "",
            "telegram_chatID": "",       
        }
        self.save_settings()

    def load(self, channelname): #load savefile function
        try:
            fullname = os.path.join(self.data_dir, f'{channelname}_data.json')
            with open(fullname, 'r') as file:
                data = json.load(file)
        except Exception as err:
            logging.error(err)
            print(f"no savefile found for {channelname}")
            if input(f"make a new save for {channelname}? y/n : ") == "y":
                self.save(self.make_save(), channelname)
                try:
                    with open(fullname, 'r') as file:
                        data = json.load(file)
                except Exception as err:
                    logging.error(err)
                    print(err)
                else:
                    return data
            else:
                return None
        
        else: 
            return data

    
    def save(self, data, channelname):
        fullname = os.path.join(self.data_dir, f'{channelname}_data.json')
        with open(fullname, 'w') as file:
            json.dump(data, file)
            
            
    def save_settings(self):
        for setting in self.settings:
            if self.settings[setting] in self.userscripts:
                isUserscript = True
            else:
                isUserscript = False
            self.settings[setting] = [self.settings[setting], isUserscript]
        fullname = os.path.join(self.main_dir, 'settings.json')
        with open(fullname, "w") as file:
            json.dump(self.settings,file)
        self.load_settings()
            
            
    def load_settings(self):
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
            
            try:

                if self.settings["telegram_bot_enabled"]=="True":
                    self.bot = TelegramBot(self.settings["telegram_bot_API"])
            except Exception as err:
                logging.error(err)

        except Exception as err:
            logging.error(err),
            self.make_settings()
            with open(fullname, "r") as file:
                self.settings = json.load(file)


    def set_target(self, channelname): 
        print(f"current target: {channelname}")
        try:
            userinput = {"channelname":input("set target: ")}
            if userinput["channelname"] != "":
                self.save_settings(userinput)
                return self.load_settings()

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

        print(f"accuracy: {round((r2_score(ypoints, model(self.hour24)))*100)}%")
        if not isResList:
            plt.title(currentdaytxt)
        plt.plot(self.hour24,ypoints)
        plt.plot(line,model(line))
        plt.grid()
        plt.show()
        

    def display_data(self, data, channelname): # defines a method called displaydata with three parameters: self, data, and channelname
        resList = self.update_reslist(data) # calls the update_reslist method of the current object with data as an argument and assigns the result to resList
        week = data["week"] # assigns the "week" key from data to the variable week
        
        # prints the channel name
        print(f"showing data for {channelname}")
        
        # constructs a string representing the header row of the table, with hours in columns
        string = f"hour:  {' '*(len(self.WEEKSTR[2])-len('hour'))}"
        for j, hour in enumerate(self.hour24):
            string += f"{hour}  "
        
        # prints a divider and the "DAYS" label
        print(f"{' '*round((len(string))/2)}/////DAYS/////")
        
        # prints the header row of the table
        print(string)
        
        # iterates over each day in the week and prints a row for each day
        for i, day in enumerate(week):
            # constructs a string representing the row label for the current day
            string = f"{self.WEEKSTR[i]}:  {' '*(len(self.WEEKSTR[2])-len(self.WEEKSTR[i]))}"
            for j, hour in enumerate(day):
                # appends each hour's value for the current day to the row string
                string += f"{hour}|{' '*len(str(self.hour24[j]))}"
            print(string) # prints the completed row
        
        # prints an empty line
        print("")
        
        # constructs a string representing the totals row of the table, with totals for each hour in columns
        string = f"total:  {' '*(len(self.WEEKSTR[2])-len('total'))}"
        for j, hour in enumerate(resList):
            string += f"{hour}|{' '*len(str(self.hour24[j]))}"
        print(string) # prints the completed totals row

                
            
    def data_input(self, data, channelname): #manually add logs to database
        
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
        
        BUFFER_SIZE = 1024
        
        port = 5785
        
        authorization = self.settings["authorization"]
        
        s = socket.socket()
        
        if not silent: print(f"[+] Connecting to {self.ips['pi']}:{port}")
        s.connect((self.ips["pi"], port))
        if not silent: print("[+] Connected.")

        message = json.dumps({
            "authorization":authorization,
            "channelname":channelname,
            "data":data,
        })

        s.send(message.encode())
             
        
        received = json.loads(s.recv(BUFFER_SIZE).decode())
        
        if received["option"] == "send_to_client":
            
            received_channelname = received["channelname"]
            received_data = received["data"]

            if not silent: print(f"[+] saving {received_channelname}_data.json from the server")
            
            self.save(received_data,received_channelname)
            
            s.close()
            if not silent: print("")
            
        elif received["option"] == "send_to_server":
            
            if not silent: print(f"[+] sent {received_channelname}_data.json to the server")
            
            s.close()
            if not silent: print("")
        elif received["option"] == "synced":
            s.close()
            if not silent: print(f"[+] {channelname}_data.json was in sync with the server")
            return
        else:
            if not silent: 
                print(f"[+] server message: {message}")
                time.sleep(5)
        
    def get_time(self):
        currenttime = time.struct_time(time.localtime())
        currentminute = currenttime[4]
        currenthour = currenttime[3]
        currentday = currenttime[6]
        return currentday, currenthour, currentminute

    def get_title(self, contents):
        return contents.head.find("meta", attrs={"property":"og:description"})["content"]
         

    def get_startdate(self, contents):
        starthour = ""
        try:
            contents = (contents.head.find("script", attrs={"type":"application/ld+json"}).contents)[0]
            if contents:
                index = contents.find('startDate":"') #len 12
                index += 12
                index = contents.find('T',index)
                index += 1
                end_index = contents.find(':',index)
                for num in range(index,end_index):
                    starthour += contents[num]
                starthour = int(starthour)
            else:
                return None
        except Exception:
            return None
        else:
            return starthour
    
    def isLive(self, contents):
        try:
            (contents.head.find("script", attrs={"type":"application/ld+json"}).contents)[0]
            return True
        except Exception:
            return False
        
    def get_methods(self):
        return [m for m in dir(TtvTracker()) if inspect.ismethod(getattr(TtvTracker(), m))]

    def update_reslist(self, data):
        week = data["week"]
        resList = []
        combinedDays = [0 for x in range(0,24)]
        for i in range(len(combinedDays)):
            resList.append(combinedDays[i]+week[0][i]+week[1][i]+week[2][i]+week[3][i]+week[4][i]+week[5][i]+week[6][i])
        return resList

    def get_stream(self, channelname):
        return BeautifulSoup(requests.get('https://www.twitch.tv/' +channelname).content.decode('utf-8'),"html.parser")

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
                contents = self.get_stream(channelname)
                
                #search for stream title
                title = self.get_title(contents)
                
                #check stream startTime for verification
                starthour = self.get_startdate(contents)

                #see if streamer is online, also avoid misinput if streamed already
                if self.isLive(contents) and starthour is not None: 
                    if not live:
                        if not alreadyStreamed[0]:
                            #verifies if the stream has started in the past hour to avoid false positives
                            if self.hour24[currenthour-self.TIMEDIFF] == starthour or self.hour24[currenthour+1-self.TIMEDIFF] == starthour:
                                playsound.playsound(self.soundalert)

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
                                
                                #send a telegram message if its enabled
                                if self.settings["telegram_bot_enabled"]=="True":
                                    self.bot.send(self.settings["telegram_chatID"], f"{channelname} went live!\n{title}\nhttps://www.twitch.tv/{channelname}")
                                
                                #show a windows toast
                                self.toast.show_toast(
                                f"{channelname} went live!",
                                f"{title}",
                                duration = 20,
                                icon_path = self.logo,
                                threaded = True,
                                )
                            else:
                                #weird mystery bug which has been badly patched
                                logging.info(f"avoided misinput: {self.hour24[currenthour-self.TIMEDIFF]} != {starthour} ")
                                
                #prediction
                prediction,line,model = self.predict(currenthour,currentminute,resList)
                
                if self.isLive(contents):
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
                if not self.check_internet():
                    print("no internet")
                else:
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
            if starthour is not None:
                if self.isLive(contents) and starthour != -1: 
                    if not alreadyStreamed[0]:
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
                            
                             
                            #send a telegram message if its enabled
                            if self.settings["telegram_bot_enabled"]=="True":
                                    self.bot.send(self.settings["telegram_chatID"], f"{channelname} went live!\n{title}\nhttps://www.twitch.tv/{channelname}")
                                
                                
                            logging.info(f"{channelname} stream started") # log into log.txt
                            #show a windows toast
                            self.toast.show_toast(
                            f"{channelname} went live!",
                            f"{title}",
                            duration = 20,
                            icon_path = self.logo,
                            threaded = True,
                            )
                        else:
                            #weird mystery bug which has been badly patched
                            logging.info(f"avoided misinput: {self.hour24[currenthour-self.TIMEDIFF]} != {starthour} ")
                            
            #prediction
            prediction,line,model = self.predict(currenthour,currentminute,resList)
            
            if self.isLive(contents):
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
                    if listeners[channelname]!=None: 
                        message = f"{channelname} added"
                    else:
                        listeners.pop(channelname)
                else:
                    for channelname in self.find_savefiles():
                        listeners[channelname] = self.load(channelname)
                        message += f"{channelname} added\n"
                
                
            elif "rm" in userinput.split(" ")[0]:
                if not self.findword("all")(userinput):
                    channelname = userinput.split(" ")[1]
                    listeners.pop(channelname)
                    message = f"{channelname} removed"
                else:
                    message
                    listeners.clear()
            
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
                            time.sleep(3)
                    except ConnectionError:
                        print("no internet")
                    except Exception as err:
                        logging.error(err)
                        
                total_errors = 0
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
                        if not self.check_internet():
                            print("no internet")
                            time.sleep(5)
                        else:
                            logging.error(err)
                            total_errors += 1
                            message = f"an error occured during tracking. X{total_errors}"
                        
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
                try:
                    num = int(userinput.split(" ")[1])-1
                except ValueError:
                    self.settings[userinput.split(" ")[1]] = userinput.split(" ")[2]
                    self.save_settings()
                    message = f"{userinput.split(' ')[1]} set with the value of {userinput.split(' ')[2]}"
                else:
                    self.settings[list(self.settings.keys())[num]] = userinput.split(" ")[2]
                    self.save_settings()
                    message = f"{list(self.settings.keys())[num]} set with the value of {userinput.split(' ')[2]}"
                
                
            elif "rm" in userinput.split(" ")[0]:
                self.settings.pop(userinput.split(" ")[1])
                message = f"{userinput.split(' ')[1]} removed"
            
            elif "userscript" in userinput.split(" ")[0]:
                name = userinput.split(" ")[2]
                value = userinput.split(" ")[3:]
                if len(value) != 0:
                    self.settings[name] = value
                    self.userscripts = value
                    self.save_settings()
                    message = f"{name} set with the value of {value}"
                else:
                    message = f"invalid input\n"
                    message += f"userscripts get run in initilation\n"
                    message += f"syntax: userscript group name value"
            
            elif "back" in userinput:
                break
                
            elif "help" in userinput:
                message += "usage: command + settingname + value\n"
                message += "usercript lets you run a piece of code before the mainloop\n"
                message += "commands:\n"
                for command in [
                "set",
                "rm",
                "back",  
                "userscript"
                ]: message += f"{command}\n"
            
    
    def run_userscript(self):
        for script in self.userscripts:
            try:
                exec(script)
            except Exception as err:
                print(f"error in userscript: {err}")
    
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

        self.load_settings()
        channelname = self.settings["channelname"]
        
        self.run_userscript()
            
        while True:
            try:
                data = self.load(channelname)
                
                userinput = input("=> ")
                if userinput == "input":
                    self.data_input(data, channelname)
                
                    
                elif userinput == "data":
                    self.display_data(data, channelname)
                    
                    
                elif userinput == "todaysresults":
                    self.graph(False, data)
                
                
                elif userinput == "results":
                    self.graph(True, data)
                
                
                elif userinput == "cls":
                    self.clear()
                    
                    
                elif userinput == "help":
                    print("")
                    for command in self.commands:
                        print(f"{command}   {' '*(len('todaysresults')-len(command))}{self.commands[command]}")
                    
                    print("\nfunctions can be used directly if you have (self.) before them")
                    methods = self.get_methods()
                    for i in range(0,len(methods),2):
                        try:
                            print(f"{methods[i]}(){' '*(len('find_savefiles()')-len(methods[i]))}\t{methods[i+1]}()")
                        except IndexError:
                            print(f"{methods[i]}()")
                    
                    
                elif self.findword("set")(userinput.split(" ")[0]):
                    channelname = userinput.split(" ")[1]
                    data = self.load(channelname)
                    self.settings["channelname"] = channelname
                    self.save_settings()
                    self.save(data, channelname)



                elif userinput == "multitrack":
                    if self.check_internet(): self.multitrack()
                    else: print("no internet")
                
                
                elif userinput == "track":
                    if self.check_internet(): self.track(data, channelname)
                    else: print("no internet")
                    
                elif userinput == "savefiles":
                    for self.savefile in self.find_savefiles():
                        print(self.savefile)
                
                elif userinput == "settings":
                    self.settings_manager()
                
                
                #simple console
                else:
                    if userinput == "exit":
                        return
                    try:
                        exec(userinput)
                    except Exception as err:
                        logging.exception(err)
                        print(f"ran into a problem, try help. error: {err}")
            except IndexError:
                print("set needs streamer's twitch name")
                
            except Exception as err:
                print(err)
    

                
                    
                
if __name__=="__main__": 
    
    tracker = TtvTracker()
    tracker.main()