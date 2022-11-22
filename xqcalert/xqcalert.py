import pickle
import requests
import time
import playsound
import matplotlib.pyplot as plt
import numpy as np
import copy
import os
import logging
import json

from sklearn.metrics import r2_score


"""
this code is for predicting the probability of xqc going live at a certain time of day
it uses a polynomial regression model to predict the probability of the stream starting
the model is trained on data from xqc stream history
"""

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

TIMEDIFF = 3
hour24 = [x for x in range(0,24)]
WEEKSTR = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

def load(channelname):
    global week, userinput, alreadyStreamed, combinedDays, resList, data
    try:
        with open(f'{channelname}_data.json', 'r') as file:
            data = json.load(file)
    except Exception as err:
        try:
            with open(f'data.pckl', 'rb') as file:
                [week,alreadyStreamed] = pickle.load(file)
            data = {
                "week":week,
                "alreadyStreamed":alreadyStreamed
                }
            save(data)
            with open(f'{channelname}_data.json', 'r') as file:
                data = json.load(file)
        except Exception as err2:
            logging.error(err)
            logging.error(err2)
            print("failed to load. Check log.txt")
            if input(f"try to make a new save for {channelname}? y/n : ") == "y":
                save(makesave())
                print("xqcalert.py is about to exit, if it doesn't please close it yourself")
                time.sleep(5)
                exit()
    
    else: 
        
        week = data["week"]
        alreadyStreamed = data["alreadyStreamed"]

        
        
        monday = week[0]
        tuesday = week[1]
        wednesday = week[2]
        thursday = week[3]
        friday = week[4]
        saturday = week[5]
        sunday = week[6]


        #resList is all of the days combined

        combinedDays = [0 for x in range(0,24)]
        resList = []
        for i in range(len(combinedDays)):
            resList.append(combinedDays[i]+monday[i]+tuesday[i]+wednesday[i]+thursday[i]+friday[i]+saturday[i]+sunday[i])
        return channelname

def savesettings(settings):
    with open(f'settings.json', "w") as file:
        json.dump(settings,file)
    return settings["channelname"]
        
        
def save(data):
    with open(f'{channelname}_data.json', 'w') as file:
        json.dump(data, file)
        
        


try:
    with open(f'settings.json', "r") as file:
        settings = json.load(file)
    
except Exception as err:
    logging.error(err),
    target = {"channelname":input("set target: ")}
    savesettings(target)
channelname = settings["channelname"]

def setTarget(channelname): 
    print(f"current target: {channelname}")
    try:
        userinput = {"channelname":input("set target: ")}
        if userinput["channelname"] != "":
            channelname = savesettings(userinput)
            try:
                channelname = load(channelname)
            except:
                data = makesave()
                return data
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


def graph(isResList):
    #uses resList or current day for graph and predictions

    currenttime = time.struct_time(time.localtime())
    currentminute = currenttime[4]
    currentday = currenttime[6]
    currenthour = currenttime[3]
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
    

def displaydata():
    #calc resList again since it may have changed
            resList = []
            for i in range(len(combinedDays)):
                resList.append(combinedDays[i]+week[0][i]+week[1][i]+week[2][i]+week[3][i]+week[4][i]+week[5][i]+week[6][i])
            print(f"showing data for {channelname}")
            print("/////WEEKDAYS/////")
            for j, day in enumerate(week):
                print(f"{WEEKSTR[j]}:  {' '*(len(WEEKSTR[2])-len(WEEKSTR[j]))}{day}")
            print("////TOTAL////")
            print(resList)
            return resList
            
          
def datainput(data):
    #manually add logs to database
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
                save(data)   
            except Exception:
                break
            
def makesave():
    global week, alreadyStreamed, channelname 
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
    
            

def main():
    global week, userinput, alreadyStreamed, combinedDays, resList, channelname, data

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

    channelname = load(channelname)

    
    while True:
        with open(f'settings.json', "r") as file:
            settings = json.load(file)
        
        channelname = settings["channelname"]
        
        userinput = input("=>")
        if userinput == "input":
            datainput(data)
            
        elif userinput == "data":
            resList = displaydata()
            
        elif userinput == "todaysresults":
            graph(False)
           
        
        elif userinput == "results":
            graph(True)
        
        
        elif userinput == "cls":
            os.system("cls")
            
            
        elif userinput == "help":
            print("input\nresults\ntodaysresults\ndata\nlisten\nconsole\ncls\ngraph(isResList)\nsave()\nback\nsetTarget")
            
        elif userinput == "setTarget":
            data = setTarget(channelname)
            
            if data != None:
                save(data)
                week = data["week"]
                alreadyStreamed = data["alreadyStreamed"]



                monday = week[0]
                tuesday = week[1]
                wednesday = week[2]
                thursday = week[3]
                friday = week[4]
                saturday = week[5]
                sunday = week[6]
            
        
        elif userinput =="listen":
            """
            checks if tracked streamer goes live and adds it into database
            also displays prediction on streamer going live with the database and polynominal regression module
            """
            streamEndHour = 0
            live = True
            while True:
                try:
                    try:
                        os.system("cls")
                        
                        print(antenna)
                        
                        #get time
                        currenttime = time.struct_time(time.localtime())
                        currentminute = currenttime[4]
                        currenthour = currenttime[3]
                        currentday = currenttime[6]

                        #updates alreadyStreamed to current day
                        if alreadyStreamed[0] == True and alreadyStreamed[1] != currentday and live == False:
                            alreadyStreamed = [False,currentday]
                            save()


                        contents = requests.get('https://www.twitch.tv/' +channelname).content.decode('utf-8')  #startdate -3 hour diff

                        #search for stream title
                        title = ""
                        try:
                            index = contents.find('description" content="') #len 22
                            index += 22
                            end_index = contents.find('"',index)
                            for char in range(index, end_index):
                                title += contents[char]
                        except Exception:
                            pass
                        
                        #check stream startTime for verification
                        startdate = ""
                        try:
                            index = contents.find('startDate":"') #len 12
                            index += 12
                            index = contents.find('T',index)
                            index += 1
                            end_index = contents.find(':',index)
                            for num in range(index,end_index):
                                startdate += contents[num]
                            startdate = int(startdate)
                        except Exception:
                            pass
                        
                        #see if streamer is online, also avoid misinput if have streamed already
                        if 'isLiveBroadcast' in contents: 
                            if live == False:
                                if alreadyStreamed[0] == False:
                                    if hour24[currenthour-TIMEDIFF] == startdate:
                                        print(f"{channelname} is live                                            ",end="\r")
                                        playsound.playsound("auughhh.mp3")
                                        #log it to database
                                        week[currentday][currenthour] +=1
                                        alreadyStreamed = [True,currentday]
                                        live = True
                                        data["week"] = week
                                        data["alreadyStreamed"] = alreadyStreamed
                                        save(data)
                                        resList = []
                                        #update resList
                                        for i in range(len(combinedDays)):
                                            resList.append(combinedDays[i]+monday[i]+tuesday[i]+wednesday[i]+thursday[i]+friday[i]+saturday[i]+sunday[i])
                                        logging.info("stream started")
                                    else:
                                        #weird mystery bug which has been badly patched
                                        logging.info(f"avoided misinput: {hour24[currenthour-TIMEDIFF]} != {startdate} ")
                                        
                        #prediction
                        prediction,line,model = predict(currenthour,currentminute,resList)

                        if 'isLiveBroadcast' in contents:
                            print(f"{channelname} is live! \ntitle: {title}",end="\r")
                            alreadyStreamed = [True,currentday]
                            streamEndHour = copy.copy(currenthour)
                            save()

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
                        if 60/model(currenthour) < 100000000000:
                            time.sleep(60/model(currenthour))
                        else:
                            time.sleep(60)
                    except KeyboardInterrupt:
                        os.system("cls")
                        break
                except Exception as err:
                    logging.exception(err)
                
        #simple console
        else:
            try:
                exec(userinput)
            except Exception as err:
                if userinput == "back":
                    break
                else:
                    print(f"ran into a problem, try help. error: {err}")
                
            

if __name__=="__main__": main()
