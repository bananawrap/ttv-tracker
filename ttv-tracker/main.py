import time
import os
import logging
import json
import socket
import re
import inspect

# NOTE: sklearn is optional since i can't get it working on a raspberrypi
try:
    from sklearn.metrics import r2_score
    accuracy_enabled = True
except ModuleNotFoundError:
    accuracy_enabled = False
    print("accuracy feature disabled")

from telegramBot import TelegramBot
import numpy as np
import matplotlib.pyplot as plt
from twitchParser import TwitchParser
from fileHandler import FileHandler
from server import TtvServer

class TtvTracker():
    def __init__(self) -> None:

        self.hour24 = range(0,24)
        self.WEEKSTR = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

        self.main_dir = os.path.split(os.path.abspath(__file__))[0]
        self.data_dir = os.path.join(self.main_dir, "data")
        
        
        fh.settings = fh.load_settings()
        
        
        self.commands = {
        "COMMAND":"DESCRIPTION",
        "input":"Input new data into the selected streamer's savefile.",
        "data":"Displays the raw data saved and displays a graph of the data in the selected savefile.",
        "track":"Track multiple Twitch channels simultaneously.",
        "cls":"Clears the console window.",
        "set":"Select the Twitch channel to track. Usage: set (channelname)",
        "settings":"View and modify program settings.",
        "savefiles":"Displays a list of available savefiles",
        "sync":"Syncs the local savefiles with the server.",
        "server":"Runs the server code, although i recommend running it from something like crontab and scheduling server.py.",
        "exit":"Self explanatory",
        }


        
    
    """
    this code is for predicting the probability of a streamer going live at a certain time of day
    it uses a polynomial regression model to predict the probability of the stream starting
    the model is trained on data from the streamer's stream history
    """
        





    def set_target(self, channelname): 
        print(f"current target: {channelname}")
        try:
            userinput = {"channelname":input("set target: ")}
            if userinput["channelname"] != "":
                fh.save_settings(userinput)
                return fh.load_settings()

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


    def graph(self, data):
        #uses data for a graph and predictions

        currentday, currenthour, currentminute = self.get_time()
        resList = self.update_reslist(data)
        week = data["week"]
        

        currentdaytxt = self.WEEKSTR[currentday]
        currentdaytxt = currentdaytxt[0].capitalize()+currentdaytxt[1:]
        currentday = week[currentday]


        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(10,4))
        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.3, hspace=0.4)
    
        prediction, line, model = self.predict(currenthour,currentminute,resList)
        
        ax1.set_title("Total")
        ax1.plot(self.hour24,resList)
        ax1.plot(line,model(line))
        ax1.grid()
        ax1.set_xticks(range(0,23,2))
        
        prediction, line, model = self.predict(currenthour,currentminute,currentday)
        
        ax2.set_title(currentdaytxt)
        ax2.plot(self.hour24,currentday)
        ax2.plot(line,model(line))
        ax2.grid()
        ax2.set_xticks(range(0,23,2))
        
        ax3.set_title("Streams per day")
        for i, day in enumerate(week):
            ax3.bar(i, day)
        ax3.set_xticks(range(7))
        ax3.set_xticklabels([x[:3] for x in self.WEEKSTR])
        ax3.grid(axis="y")
        if accuracy_enabled:
            ax4.set_title("Accuracy")
            ax4.bar(0,self.get_accuracy(resList)*100)
            ax4.bar(1,self.get_accuracy(currentday)*100)
            ax4.set_xticks((0,1))
            ax4.set_xticklabels(("Total accuracy", "Current day's accuracy"))
            ax4.set_yticks(range(0,110,10))
            ax4.set_yticklabels([f"{str(x)}%" for x in range(0,110,10)])
            ax4.grid(axis="y")
        else:
            ax4.set_title("Accuracy is disabled")
        
        plt.show()
        

    def display_data(self, data, channelname):
        resList = self.update_reslist(data) # calls the update_reslist method of the current object with data as an argument and assigns the result to resList
        week = data["week"] # assigns the "week" key from data to the variable week
        
        # prints the channel name
        print(f"Showing data for {channelname}")
        
        # constructs a string representing the header row of the table, with hours in columns
        string = f"Hour:  {' '*(len(self.WEEKSTR[2])-len('hour'))}"
        for j, hour in enumerate(self.hour24):
            string += f"{'0'+str(hour) if len(str(hour)) < 2 else str(hour)}  "
        
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
                string += f"{'0'+str(hour) if len(str(hour)) < 2 else str(hour)}| "
            print(string) # prints the completed row
        
        # prints an empty line
        print("")
        
        # constructs a string representing the totals row of the table, with totals for each hour in columns
        string = f"Total:  {' '*(len(self.WEEKSTR[2])-len('total'))}"
        for j, hour in enumerate(resList):
            string += f"{'0'+str(hour) if len(str(hour)) < 2 else str(hour)}| "
        print(string) # prints the completed totals row

                
            
    def data_input(self, data, channelname): #manually add data
        message = ""
        while True:
            self.clear()
            print("data editor\n")
            print(f"{message}")
            message = ""
            self.display_data(data)
            print("")
            userinput = input("==> ")
            command = userinput.split(" ")[0]
            selected_day = userinput.split(" ")[1]
            selected_hour = userinput.split(" ")[2]
            value = userinput.split(" ")[3]

            for day, i in enumerate(self.WEEKSTR):
                if selected_day in day:
                    selected_day = i
            
            if "set" == command:
                data["week"][selected_day][selected_hour] = value
                fh.save(data, channelname)
                
                
            elif "add" == command:
                data["week"][selected_day][selected_hour] =+ value
            
            
            elif "back" == command:
                break
                
            elif "help" == command:
                message += "usage: command + settingname + value\n"
                message += "commands:\n"
                for x in [
                "set",
                "rm",
                "back",  
                ]: message += f"{x}\n"
                
            

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
        try:
            BUFFER_SIZE = 1024
            
            port = int(fh.settings["port"])
            
            authorization = fh.settings["authorization"]
            
            s = socket.socket()
            server = f"{fh.settings['server_ip']}"
            
            if not silent: print(f"[+] Connecting to {server}:{port}")
            s.connect((server, port))
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
                
                fh.save(received_data,received_channelname)
                
                s.close()
                if not silent: print("")
                
            elif received["option"] == "send_to_server":
                
                if not silent: print(f"[+] sent {received_channelname}_data.json to the server")
                
                s.close()
                if not silent: print("")
                
            elif received["option"] == "synced":
                s.close()
                if not silent: print(f"[+] {channelname}_data.json was in sync with the server")
                if not silent: print("")
                return
            
            else:
                if not silent: 
                    print(f"[+] server message: {received}")
                    time.sleep(5)
        except Exception as err:
            print(f"[+] Error: {err}")
                
    def multisync(self, listeners):
        server = f"{fh.settings['server_ip']}"
        if self.check_port(server,5785):
            for streamer in listeners:
                try:
                    self.sync(listeners[streamer], streamer)
                    time.sleep(3)
                except ConnectionError:
                    print("no internet")
                except Exception as err:
                    logging.error(err)
        else:
            print("no connection to a server")
       
        
    def get_time(self):
        currenttime = time.struct_time(time.localtime())
        currentminute = currenttime[4]
        currenthour = currenttime[3]
        currentday = currenttime[6]
        return currentday, currenthour, currentminute
    
        
    def get_methods(self):
        return [m for m in dir(TtvTracker()) if inspect.ismethod(getattr(TtvTracker(), m))]

    def update_reslist(self, data):
        week = data["week"]
        resList = []
        combinedDays = [0 for x in range(0,24)]
        for i in range(len(combinedDays)):
            resList.append(combinedDays[i]+week[0][i]+week[1][i]+week[2][i]+week[3][i]+week[4][i]+week[5][i]+week[6][i])
        return resList


    def get_accuracy(self, array):
        if accuracy_enabled:
            return r2_score(array, self.predict(self.get_time()[1], self.get_time()[2], array)[2](self.hour24))
        else:
            return 0.0
    
    def check_internet(self):
        return self.check_port("google.com",80)
    
    def telegram_alert(self, channelname, title):
        if fh.settings["telegram_bot_enabled"]=="True":
                self.bot.send(fh.settings["telegram_chatID"], f"{channelname} went live!\n{title}\nhttps://www.twitch.tv/{channelname}")
    
    def register_broadcast(self, data, channelname, contents=None):

        if contents is not None:
            start_time = tp.get_startdate(contents)
            title = tp.get_title(contents)
        
        week = data["week"]
        alreadyStreamed = data["alreadyStreamed"]


        currentday, currenthour, currentminute = self.get_time()

        week[currentday][currenthour] +=1

        alreadyStreamed = [True,currentday]
        
        
        data = {
        "week":week,
        "alreadyStreamed":alreadyStreamed,
        "lastStream":start_time,
        }

        fh.save(data, channelname)
            
        self.telegram_alert(channelname, title)
            
        logging.info(f"{channelname} stream started") 

        # NOTE: disabled for not being cross platform
        #show a windows toast
        # self.toast.show_toast(
        # f"{channelname} went live!",
        # f"{title}",
        # duration = 20,
        # icon_path = self.logo,
        # threaded = True,
        # )
   

    def check_stream(self, data, channelname):
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
                fh.save(data, channelname)
                
            contents = tp.get_stream(channelname)

            start_time = tp.get_startdate(contents)

            timediff = fh.settings['timediff']

            if start_time is not None:
                if tp.is_live(contents) and start_time["hour"] != -1: 
                    if not alreadyStreamed[0]:
                        #verifies if the stream has started in the past hour to avoid false positives
                        if self.hour24[currenthour-timediff] == start_time["hour"] or self.hour24[currenthour+1-timediff] == start_time["hour"]:
                            self.register_broadcast(data, contents)
                            live = True

                        else:
                            #weird mystery bug which has been badly patched
                            logging.info(f"avoided misinput: {self.hour24[currenthour-timediff]} != {start_time['hour']} ")
                            
            #prediction
            prediction,line,model = self.predict(currenthour,currentminute,resList)
            
            if tp.is_live(contents):
                live = True
                alreadyStreamed = [True,currentday]
                data = {
                "week":week,
                "alreadyStreamed":alreadyStreamed,
                "lastStream":start_time,
                }
                fh.save(data, channelname)
            else:
                live = False
            
            return data, prediction, live
        except Exception as err:
            logging.exception(err)    
            

    def track(self, autoplay=False):
        accuracyratings = ["bad", "decent", "good", "very good"]
        listeners = {}
        message = ""
        while True:
            try:
                self.clear()
                print("tracking paused")
                print(f"listeners: {len(listeners)}")
                print(f"{message}")
                message = ""
                print("")
                userinput = ""
                add_all = False
                if not autoplay: userinput = input("==> ")
                
                if "add" in userinput.split(" ")[0]:
                    if not self.findword("all")(userinput):
                        add_all = False
                        channelname = userinput.split(" ")[1]
                        listeners[channelname] = fh.load(channelname)      
                        if listeners[channelname]!=None: 
                            message = f"{channelname} added"
                        else:
                            listeners.pop(channelname)
                    else:
                        add_all = True
                        for channelname in self.find_savefiles():
                            listeners[channelname] = fh.load(channelname)
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
                            listeners[channelname] = fh.load(channelname)
                            message += f"{channelname} added\n"
                        autoplay = False
                    message = ""
                    
                    self.multisync(listeners)
                            
                    total_errors = 0
                    while True:
                        try:
                            self.clear()
                            print("tracking (ctrl + c) to pause")
                            print(f"active listeners: {len(listeners)}")
                            print(f"{message}")

                            if add_all and len(self.find_savefiles()) > len(listeners):
                                for channelname in self.find_savefiles():
                                    listeners[channelname] = fh.load(channelname)

                            
                            for streamer in listeners:
                                listeners[streamer] = fh.load(streamer)

                            for streamer in listeners:
                                streaminfo = self.check_stream(listeners[streamer], streamer)
                                streaminfo = { 
                                            "data":streaminfo[0], 
                                            "prediction":streaminfo[1], 
                                            "live":streaminfo[2], 
                                            }
                                try:

                                    if accuracy_enabled:
                                        accuracyrating = accuracyratings[round(self.get_accuracy(self.update_reslist(streaminfo["data"]))*100/25)-1]
                                    else:
                                        accuracyrating = "disabled"
                                except Exception:
                                    accuracyrating = "none"
                                
                                fh.save(streaminfo["data"], streamer)
                                print(f"{'-'*os.get_terminal_size()[0]}")
                                print(f"streamer: {streamer}")
                                print(f"live: {streaminfo['live']}")
                                if streaminfo["live"]:
                                    print(f"title: {tp.get_title(tp.get_stream(streamer))}")
                                else:
                                    print(f"probability of a stream: {streaminfo['prediction']}%")
                                    print(f"prediction accuracy is {accuracyrating}")
                                    try:
                                        print(f"last stream on {self.WEEKSTR[streaminfo['data']['alreadyStreamed'][1]]} {streaminfo['data']['lastStream']['date']}")
                                    except Exception:
                                        print(f"last stream on {self.WEEKSTR[streaminfo['data']['alreadyStreamed'][1]]}")
                            time.sleep(60)
                                
                                
                
                        except KeyboardInterrupt:
                            print("")
                            break
                        except Exception as err:
                            if not self.check_internet():
                                print("no internet")
                                time.sleep(5)
                            else:
                                time.sleep(total_errors)
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
            except KeyboardInterrupt:
                print("")
                break
                
    def find_savefiles(self):
        path = self.main_dir
        identifier = "_data.json"
        results = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if identifier in file:
                    results.append(file.replace(identifier,""))
        savefiles = {}
        for streamer in results:
            savefiles[streamer] = fh.load(streamer)
        return savefiles

    def findword(self, w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

    def settings_manager(self):
        message = ""
        while True:
            try:
                self.clear()
                print("settings manager\n")
                print(f"{message}")
                for i, setting in enumerate(fh.settings):
                    if fh.settings[setting] in fh.userscripts:
                        print(f"{i+1}. {setting}: {fh.settings[setting]} (userscript)")
                    else:
                        print(f"{i+1}. {setting}: {fh.settings[setting]}")
                message = ""
                print("")
                userinput = input("==> ")
                command = userinput.split(" ")[0]
                try:
                    setting = userinput.split(" ")[1]
                    value   = userinput.split(" ")[2:]
                    if isinstance(value, list):
                        value = value[0]
                except IndexError:
                    pass
                
                if "set" == command:
                    if type(setting) == int:
                        fh.settings[list(fh.settings.keys())[setting]] = value
                        fh.save_settings()
                        message = f"{list(fh.settings.keys())[setting]} set with the value of {value}"
                    else:
                        fh.settings[setting] = value
                        fh.save_settings()
                        message = f"{setting} set with the value of {value}"
                    
                    
                elif "rm" == command:
                    fh.settings.pop(setting)
                    message = f"{setting} removed"
                
                elif "userscript" == command:
                    if len(value) != 0:
                        fh.settings[setting] = value
                        fh.userscripts = value
                        fh.save_settings()
                        message = f"{setting} set with the value of {value}"
                    else:
                        message = f"invalid input\n"
                        message += f"userscripts get run in initilation\n"
                        message += f"syntax: userscript group name value"
                
                elif "back" == command:
                    break
                    
                elif "help" == command:
                    message += """
usage: command + settingname/index + value\n 
usercript lets you run a piece of code before the mainloop\n 
\nexplanations for some of the variables:\n
channelname: is the default channel to track. Can be changed with the set command outside of settings\n
authorization: the password used to communicate with a server.\n
timediff: timezone offset.\n

\ncommands:\n
"""
                    for x in [
                    "set",
                    "rm",
                    "back",  
                    "userscript"
                    ]: message += f"{x}\n"
            except KeyboardInterrupt:
                print("")
                break
            
    
    def run_userscript(self):
        for script in fh.userscripts:
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

        fh.load_settings()
        channelname = fh.settings["channelname"]
        
        self.run_userscript()

        try:

            if fh.settings["telegram_bot_enabled"]=="True":
                self.bot = TelegramBot(fh.settings["telegram_bot_API"])
        except Exception as err:
            logging.error(err)
            
        while True:
            try:
                data = fh.load(channelname)
                
                userinput = input("=> ")
                if userinput == "input":
                    self.data_input(data, channelname)
                
                    
                elif userinput == "data":
                    self.display_data(data, channelname)
                    self.graph(data)
                
                
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
                    try:
                        name = userinput.split(" ")[1]
                        data = fh.load(name)
                        if data:
                            channelname = name
                            fh.settings["channelname"] = channelname
                            fh.save_settings()
                            fh.save(data, channelname)
                    except IndexError:
                        print("set needs streamer's name")


                elif userinput == "track":
                    if self.check_internet(): self.track()
                    else: print("no internet")
                
                    
                elif userinput == "savefiles":
                    for self.savefile in self.find_savefiles().keys():
                        print(self.savefile)
                

                elif userinput == "settings":
                    self.settings_manager()

                    
                elif userinput == "sync":
                    self.multisync(self.find_savefiles())

                elif userinput == "server":
                    server.main()
                
                
                #simple console
                else:
                    if userinput == "exit":
                        return
                    try:
                        exec(userinput)
                    except Exception as err:
                        logging.exception(err)
                        print(f"ran into a problem, try help. error: {err}")

            except KeyboardInterrupt:
                print("")
                break

            except IndexError:
                print("Index error")
                
            except Exception as err:
                print(err)
    
          
if __name__=="__main__": 
    fh = FileHandler()
    server = TtvServer(fh)
    tp = TwitchParser()
    tracker = TtvTracker()
    tracker.main()
