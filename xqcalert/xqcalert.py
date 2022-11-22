import pickle
import requests
import time
import playsound
import matplotlib.pyplot as plt
import numpy as np
import copy
import os
import logging

from sklearn.metrics import r2_score


"""
this code is for predicting the probability of xqc going live at a certain time of day
it uses a polynomial regression model to predict the probability of the stream starting
the model is trained on data from xqc stream history
"""

TIMEDIFF = 3
hour24 = [x for x in range(0,24)]
WEEKSTR = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
CHANNELNAME = 'xqc'

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


def save():
    with open('data.pckl', 'wb') as file:
        pickle.dump([week, alreadyStreamed], file)
        
        
def predict(currenthour, currentminute, ypoints):
    
    xpoints = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    
    #polynominal regression module
    model = np.poly1d(np.polyfit(xpoints,ypoints,deg=5))
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
    

def data():
    #calc resList again since it may have changed
            resList = []
            for i in range(len(combinedDays)):
                resList.append(combinedDays[i]+week[0][i]+week[1][i]+week[2][i]+week[3][i]+week[4][i]+week[5][i]+week[6][i])
            print("/////WEEKDAYS/////")
            for j, day in enumerate(week):
                print(f"{WEEKSTR[j]}:  {' '*(len(WEEKSTR[2])-len(WEEKSTR[j]))}{day}")
            print("////TOTAL////")
            print(resList)
            return resList
            
          
def datainput():
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
                save()   
            except Exception:
                break
            

def main():
    global week, userinput, alreadyStreamed, combinedDays, resList

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
   

    try:
        with open('data.pckl', 'rb') as file:
            [week,alreadyStreamed] = pickle.load(file)
    except Exception:
        if input("make new save? (y/n)")=="y":
            
            monday =    [0 for x in range(0,24)]
            tuesday =   [0 for x in range(0,24)]
            wednesday = [0 for x in range(0,24)]
            thursday =  [0 for x in range(0,24)]
            friday =    [0 for x in range(0,24)]
            saturday =  [0 for x in range(0,24)]
            sunday =    [0 for x in range(0,24)]
            week = [monday,tuesday,wednesday,thursday,friday,saturday,sunday]
            alreadyStreamed = [False,0]
            save()
    
        

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

    
    while True:
        
        userinput = input("=>")
        if userinput == "input":
            datainput()
            
        elif userinput == "data":
            resList = data()
            
        elif userinput == "todaysresults":
            graph(False)
           
        
        elif userinput == "results":
            graph(True)
        
        
        elif userinput == "cls":
            os.system("cls")
            
            
        elif userinput =="help":
            print("input\nresults\ntodaysresults\ndata\nlisten\nconsole\ncls\ngraph(isResList)\nsave()\nback")
        
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


                        contents = requests.get('https://www.twitch.tv/' +CHANNELNAME).content.decode('utf-8')  #startdate -3 hour diff

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
                                    if hour24[currenthour-TIMEDIFF] == startdate or hour24[currenthour-TIMEDIFF+1] == startdate:
                                        playsound.playsound("auughhh.mp3")
                                        #log it to database
                                        week[currentday][currenthour] +=1
                                        alreadyStreamed = [True,currentday]
                                        live = True
                                        save()
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
                            print(f"{CHANNELNAME} is live! \ntitle: {title}",end="\r")
                            alreadyStreamed = [True,currentday]
                            streamEndHour = copy.copy(currenthour)
                            save()

                        elif alreadyStreamed[0] == True and alreadyStreamed[1] == currentday and live == False:
                            if live and "streamEndHour" in locals():
                                print(f"{CHANNELNAME} already streamed today at {streamEndHour} \noverall probability: {prediction}%",end="\r")
                            else:
                                print(f"{CHANNELNAME} already streamed today \noverall probability: {prediction}%",end="\r")

                        else:
                            print(f"{CHANNELNAME} is not live \noverall probability: {prediction}%",end="\r")
                            if live and "streamEndHour" in locals():
                                if streamEndHour != currenthour:
                                    live = False
                            else:
                                live = False
                            
                        #print(60/model(currenthour))
                        time.sleep(60/model(currenthour))
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
