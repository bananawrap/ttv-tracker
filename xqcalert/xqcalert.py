import requests
import time
import playsound
import copy
import os
import logging
import json
import tqdm
import socket

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from win10toast import ToastNotifier

"""
this code is for predicting the probability of a streamer going live at a certain time of day
it uses a polynomial regression model to predict the probability of the stream starting
the model is trained on data from the streamer's stream history
"""
    
ips = {
 "pc":"192.168.0.57",
 "pi":"192.168.0.77"
}

toast = ToastNotifier()

TIMEDIFF = 3
hour24 = [x for x in range(0,24)]
WEEKSTR = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

main_dir = os.path.split(os.path.abspath(__file__))[0]


def load(channelname): #load savefile function
    try:
        fullname = os.path.join(main_dir, f'{channelname}_data.json')
        with open(fullname, 'r') as file:
            data = json.load(file)
    except Exception as err:
        logging.error(err)
        print("failed to load. Check log.txt")
        if input(f"try to make a new save for {channelname}? y/n : ") == "y":
            save(makesave(), channelname)
            try:
                with open(fullname, 'r') as file:
                    data = json.load(file)
            except Exception as err:
                logging.error(err)
                print("xqcalert.py is about to exit, if it doesn't please close it yourself")
                time.sleep(3)
                exit()
            else:
                return data
    
    else: 
        return data

  
def save(data, channelname):
    fullname = os.path.join(main_dir, f'{channelname}_data.json')
    with open(fullname, 'w') as file:
        json.dump(data, file)
        
        
def savesettings(settings):
    fullname = os.path.join(main_dir, 'settings.json')
    with open(fullname, "w") as file:
        json.dump(settings,file)
        
        
def loadsettings():
    try:
        fullname = os.path.join(main_dir, 'settings.json')
        with open(fullname, "r") as file:
            settings = json.load(file)

    except Exception as err:
        logging.error(err),
        target = {"channelname":input("set target: ")}
        savesettings(target)
        with open(fullname, "r") as file:
            settings = json.load(file)
    return settings["channelname"]


def setTarget(channelname): 
    print(f"current target: {channelname}")
    try:
        userinput = {"channelname":input("set target: ")}
        if userinput["channelname"] != "":
            savesettings(userinput)
            return loadsettings()

        else:
            raise ValueError("empty name")
        
    except Exception as err:
        print(f"failure: {err}")
    


def predict(currenthour, currentminute, ypoints):
    
    
    #polynominal regression module
    model = np.poly1d(np.polyfit(hour24,ypoints,deg=5))
    line = np.linspace(0,23,100)
    
    #we use the module to get a prediction for the current time
    prediction = round((model(currenthour+currentminute/60)/sum(ypoints)*100),1)
    return prediction, line, model


def graph(isResList, data):
    #uses resList or current day for graph and predictions

    currentday, currenthour, currentminute = get_time()
    resList = update_reslist(data)
    week = data["week"]
    
    if not isResList:
        currentdaytxt = WEEKSTR[currentday]
        mode = week[currentday]
    else:
        mode = resList



    ypoints = mode
   
    prediction, line, model = predict(currenthour,currentminute,mode)
    print(f"current odds:{prediction}%")

    for j in range(len(hour24)):
        print(f"{str(j)}: {round((model(j)/sum(mode))*100,1)}%")

    print("accuracy:", r2_score(ypoints, model(hour24)))
    if not isResList:
        plt.title(currentdaytxt)
    plt.plot(hour24,ypoints)
    plt.plot(line,model(line))
    plt.grid()
    plt.show()
    

def displaydata(data, channelname): # basically a fancy and a complicated way of centering the different outputs
    
    resList = update_reslist(data)
    week = data["week"]
    
    print(f"showing data for {channelname}")
    print(f"{' '*round((len(WEEKSTR[2])+(24*3))/2)}/////DAYS/////")
    for j, day in enumerate(week):
        print(f"{WEEKSTR[j]}:  {' '*(len(WEEKSTR[2])-len(WEEKSTR[j]))}{day}")
    print(f"{' '*round((len(WEEKSTR[2])+(24*3))/2)}/////TOTAL/////")
    print(f"{' '*(len(WEEKSTR[2])+3)}{resList}")
            
          
def datainput(data, channelname): #manually add logs to database
    
    week = data["week"]
    run = True
    x = False
    while run:
        
        dayInput = input("day: ")
        for d in range(7):
            for lenght in range(1,WEEKSTR[d].__len__()):
                if dayInput == WEEKSTR[d][:lenght]:
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
                save(data, channelname)   
            except Exception:
                break
            
def makesave():
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
         

def clear():
    if os.name=="nt":
        os.system("cls")
    else:
        os.system('clear')
        
    
def check_port(ip,port): 
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        c.connect((ip, port))
        c.close()
        return True
    except socket.error:
        return False
        
def sync(data, channelname):
    
    resList = update_reslist(data)
    
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 1024
    
    port = 5785
    
    
    s = socket.socket()
    print(f"[+] Connecting to {ips['pi']}:{port}")
    s.connect((ips["pi"], port))
    print("[+] Connected.")

    s.send(f"{channelname}".encode())
    
    server_totalsum = int(s.recv(BUFFER_SIZE).decode())
    
    if server_totalsum > sum(resList):
        s.send("2".encode())
        received = s.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        

        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            while True:

                bytes_read = s.recv(BUFFER_SIZE)
                if not bytes_read:    
                    break

                f.write(bytes_read)
                progress.update(len(bytes_read))
                
            s.close()
            print("")
        
    elif server_totalsum < sum(resList):
        s.send("1".encode())
        filename = f"{channelname}_data.json"
        filesize = os.path.getsize(filename)
        
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())
        time.sleep(1)
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:

                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:

                    break

                s.sendall(bytes_read)

                progress.update(len(bytes_read))
        s.close()
        print("")
    else:
        s.send("".encode())
        s.close()
        print("already synced")
        return
    
def get_time():
    currenttime = time.struct_time(time.localtime())
    currentminute = currenttime[4]
    currenthour = currenttime[3]
    currentday = currenttime[6]
    return currentday, currenthour, currentminute

def get_title(contents):
    title = ""
    try:
        index = contents.find('description" content="') #len 22
        index += 22
        end_index = contents.find('"',index)
        for char in range(index, end_index):
            title += contents[char]
    except Exception:
        pass

def get_startdate(contents):
    starthour = ""
    try:
        index = contents.find('startDate":"') #len 12
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

def update_reslist(data):
    week = data["week"]
    resList = []
    combinedDays = [0 for x in range(0,24)]
    for i in range(len(combinedDays)):
        resList.append(combinedDays[i]+week[0][i]+week[1][i]+week[2][i]+week[3][i]+week[4][i]+week[5][i]+week[6][i])
    return resList

def listen(data, channelname):
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
    resList = update_reslist(data)
    
    try:
        if check_port(ips["pi"],5785):
            sync(data, channelname)
            load(channelname)
    except Exception as err:
        print(err)
        logging.error(err)
    
    time.sleep(5)
    streamEndHour = 0
    live = True
    while True:
        try:
            try:
                clear()
                
                print(antenna)
                
                currentday, currenthour, currentminute = get_time()
  
                #updates alreadyStreamed to current day
                if alreadyStreamed[0] == True and alreadyStreamed[1] != currentday and live == False:
                    alreadyStreamed = [False,currentday]
                    save(data, channelname)

                #request stream data from twitch
                contents = requests.get('https://www.twitch.tv/' +channelname).content.decode('utf-8')  #startdate -3 hour diff

                #search for stream title
                title = get_title(contents)
                
                
                #check stream startTime for verification
                starthour = get_startdate(contents)
  
                #see if streamer is online, also avoid misinput if streamed already
                if 'isLiveBroadcast' in contents: 
                    if live == False:
                        if alreadyStreamed[0] == False:
                            #verifies if the stream has started in the past hour to avoid false positives
                            if hour24[currenthour-TIMEDIFF] == starthour or hour24[currenthour+1-TIMEDIFF] == starthour:
                                playsound.playsound("auughhh.mp3")
  
                                #log it to the data list
                                week[currentday][currenthour] +=1
                                #set the already streamed flag to true
                                alreadyStreamed = [True,currentday]
  
                                #confirm that the stream is live
                                live = True
  
                                #pack the information into a data dictionary and save it to (channelname)_data.json
                                data["week"] = week
                                data["alreadyStreamed"] = alreadyStreamed
                                save(data, channelname)
                                
                                resList = update_reslist(data)
                                
                                
                                logging.info("stream started") # log into log.txt
                                #show a windows toast
                                toast.show_toast(
                                f"{channelname} went live!",
                                f"{title}",
                                duration = 20,
                                icon_path = "pythowo.ico",
                                threaded = True,
                                )
                            else:
                                #weird mystery bug which has been badly patched
                                logging.info(f"avoided misinput: {hour24[currenthour-TIMEDIFF]} != {starthour} ")
                                
                #prediction
                prediction,line,model = predict(currenthour,currentminute,resList)
                
                if 'isLiveBroadcast' in contents:
                    print(f"{channelname} is live! \ntitle: {title}",end="\r")
                    alreadyStreamed = [True,currentday]
                    streamEndHour = copy.copy(currenthour)
                    save(data, channelname)
                
                elif alreadyStreamed[0] == True and alreadyStreamed[1] == currentday and live == False:
                    if live and "streamEndHour" in locals():
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
                    
                #print(60/model(currenthour))
                if 60/model(currenthour) < 10000000:
                    time.sleep(60/model(currenthour))
                else:
                    time.sleep(60)
            except KeyboardInterrupt:
                clear()
                break
        except Exception as err:
            logging.exception(err)    

def main():

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

    channelname = loadsettings()
    
    data = load(channelname)

    while True:
        
        data = load(channelname)
        
        userinput = input("=> ")
        if userinput == "input":
            datainput(data, channelname)
            
        elif userinput == "data":
            displaydata(data, channelname)
            
        elif userinput == "todaysresults":
            graph(False, data)
           
        
        elif userinput == "results":
            graph(True, data)
        
        
        elif userinput == "cls":
            clear()
            
            
        elif userinput == "help":
            for command in commands:
                print(command)
            
        elif userinput == "setTarget":
            channelname = setTarget(channelname)
            
            if data != None:
                save(data, channelname)

        
        elif userinput =="listen":
            listen(data, channelname)
        
        #simple console
        else:
            try:
                exec(userinput)
            except Exception as err:
                if userinput == "exit":
                    break
                else:
                    print(f"ran into a problem, try help. error: {err}")
                
            

if __name__=="__main__": 
    commands = [name for (name, thing) in locals().items() if callable(thing)]
    for i in range(len(commands)): 
        commands[i] += "()"
        
    commands.extend(
     [
     "input",
     "results",
     "todaysresults",
     "data",
     "listen",
     "cls",
     "exit",
     "setTarget",
     ]
    )  
    
    main()
