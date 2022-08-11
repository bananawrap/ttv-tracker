import pickle
import requests
import time
import playsound
from ctypes import Structure, windll, c_uint, sizeof, byref
import matplotlib.pyplot as plt
import numpy as np
import copy
from scipy import stats
from sklearn.metrics import r2_score


"""
this code is for predicting the probability of xqc going live at a certain time of day
it uses a polynomial regression model to predict the probability of the stream starting
the model is trained on data from xqc stream history
"""

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

def get_idle_duration():
    #for the afk detection
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0


def save():
    with open('data.pckl', 'wb') as file:
        pickle.dump([week, alreadyStreamed], file)


def graph(day):
    #outdated graph
    xpoints = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    ypoints = day
    print(day)
    plt.step(xpoints,ypoints,where="mid")
    plt.grid()
    plt.show()


def main():
    global week, userinput, alreadyStreamed
    #afk detection
    #skips straight to listen if mouse isnt moved. Kinda annoying maybe remove
    afk = False
    if get_idle_duration() > 0:
        for t in range(2):
            time.sleep(1)
            if get_idle_duration() >= 1:
                print("                ",end="\r")
                print("going afk in",1-t,end="\r")
                if t >= 1:
                    afk = True
                    userinput = "listen"
                elif t <= -1:
                    break
            else:
                t -= 2

    

    try:
        with open('data.pckl', 'rb') as file:
            [week,alreadyStreamed] = pickle.load(file)
    except:
        if input("make new save? (y/n)")=="y":
            mo0, mo1, mo2, mo3, mo4, mo5, mo6, mo7, mo8, mo9, mo10, mo11, mo12, mo13, mo14, mo15, mo16, mo17, mo18, mo19, mo20, mo21, mo22, mo23 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0   
            tu0, tu1, tu2, tu3, tu4, tu5, tu6, tu7, tu8, tu9, tu10, tu11, tu12, tu13, tu14, tu15, tu16, tu17, tu18, tu19, tu20, tu21, tu22, tu23 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            we0, we1, we2, we3, we4, we5, we6, we7, we8, we9, we10, we11, we12, we13, we14, we15, we16, we17, we18, we19, we20, we21, we22, we23 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            th0, th1, th2, th3, th4, th5, th6, th7, th8, th9, th10, th11, th12, th13, th14, th15, th16, th17, th18, th19, th20, th21, th22, th23 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            fr0, fr1, fr2, fr3, fr4, fr5, fr6, fr7, fr8, fr9, fr10, fr11, fr12, fr13, fr14, fr15, fr16, fr17, fr18, fr19, fr20, fr21, fr22, fr23 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            sa0, sa1, sa2, sa3, sa4, sa5, sa6, sa7, sa8, sa9, sa10, sa11, sa12, sa13, sa14, sa15, sa16, sa17, sa18, sa19, sa20, sa21, sa22, sa23 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            su0, su1, su2, su3, su4, su5, su6, su7, su8, su9, su10, su11, su12, su13, su14, su15, su16, su17, su18, su19, su20, su21, su22, su23 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            
            monday = [mo0, mo1, mo2, mo3, mo4, mo5, mo6, mo7, mo8, mo9, mo10, mo11, mo12, mo13, mo14, mo15, mo16, mo17, mo18, mo19, mo20, mo21, mo22, mo23]
            tuesday = [tu0, tu1, tu2, tu3, tu4, tu5, tu6, tu7, tu8, tu9, tu10, tu11, tu12, tu13, tu14, tu15, tu16, tu17, tu18, tu19, tu20, tu21, tu22, tu23]
            wednesday = [we0, we1, we2, we3, we4, we5, we6, we7, we8, we9, we10, we11, we12, we13, we14, we15, we16, we17, we18, we19, we20, we21, we22, we23]
            thursday = [th0, th1, th2, th3, th4, th5, th6, th7, th8, th9, th10, th11, th12, th13, th14, th15, th16, th17, th18, th19, th20, th21, th22, th23]
            friday = [fr0, fr1, fr2, fr3, fr4, fr5, fr6, fr7, fr8, fr9, fr10, fr11, fr12, fr13, fr14, fr15, fr16, fr17, fr18, fr19, fr20, fr21, fr22, fr23]
            saturday = [sa0, sa1, sa2, sa3, sa4, sa5, sa6, sa7, sa8, sa9, sa10, sa11, sa12, sa13, sa14, sa15, sa16, sa17, sa18, sa19, sa20, sa21, sa22, sa23]
            sunday = [su0, su1, su2, su3, su4, su5, su6, su7, su8, su9, su10, su11, su12, su13, su14, su15, su16, su17, su18, su19, su20, su21, su22, su23]
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
    [mo0, mo1, mo2, mo3, mo4, mo5, mo6, mo7, mo8, mo9, mo10, mo11, mo12, mo13, mo14, mo15, mo16, mo17, mo18, mo19, mo20, mo21, mo22, mo23] = monday
    [tu0, tu1, tu2, tu3, tu4, tu5, tu6, tu7, tu8, tu9, tu10, tu11, tu12, tu13, tu14, tu15, tu16, tu17, tu18, tu19, tu20, tu21, tu22, tu23] = tuesday
    [we0, we1, we2, we3, we4, we5, we6, we7, we8, we9, we10, we11, we12, we13, we14, we15, we16, we17, we18, we19, we20, we21, we22, we23] = wednesday
    [th0, th1, th2, th3, th4, th5, th6, th7, th8, th9, th10, th11, th12, th13, th14, th15, th16, th17, th18, th19, th20, th21, th22, th23] = thursday
    [fr0, fr1, fr2, fr3, fr4, fr5, fr6, fr7, fr8, fr9, fr10, fr11, fr12, fr13, fr14, fr15, fr16, fr17, fr18, fr19, fr20, fr21, fr22, fr23] = friday
    [sa0, sa1, sa2, sa3, sa4, sa5, sa6, sa7, sa8, sa9, sa10, sa11, sa12, sa13, sa14, sa15, sa16, sa17, sa18, sa19, sa20, sa21, sa22, sa23] = saturday
    [su0, su1, su2, su3, su4, su5, su6, su7, su8, su9, su10, su11, su12, su13, su14, su15, su16, su17, su18, su19, su20, su21, su22, su23] = sunday


    #resList is all of the days combined
    cd0, cd1, cd2, cd3, cd4, cd5, cd6, cd7, cd8, cd9, cd10, cd11, cd12, cd13, cd14, cd15, cd16, cd17, cd18, cd19, cd20, cd21, cd22, cd23 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    combinedDays = [cd0, cd1, cd2, cd3, cd4, cd5, cd6, cd7, cd8, cd9, cd10, cd11, cd12, cd13, cd14, cd15, cd16, cd17, cd18, cd19, cd20, cd21, cd22, cd23]
    resList = []
    for i in range(len(combinedDays)):
        resList.append(combinedDays[i]+monday[i]+tuesday[i]+wednesday[i]+thursday[i]+friday[i]+saturday[i]+sunday[i])

    
    WEEKSTR = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    CHANNELNAME = 'xqc'

    #mainloop
    while True:
        if afk == False:
            userinput = input("=>")
        if userinput == "input":
            datainput(WEEKSTR)
            
        elif userinput == "data":
            #calc resList again since it may have changed
            resList = []
            for i in range(len(combinedDays)):
                resList.append(combinedDays[i]+monday[i]+tuesday[i]+wednesday[i]+thursday[i]+friday[i]+saturday[i]+sunday[i])
            print("/////WEEKDAYS/////")
            for day in week:
                print(day)
            print("////WHOLE WEEK////")
            print(resList)
        
        elif userinput =="listen":
            """
            checks if tracked streamer goes live and adds it into database
            also displays prediction on streamer going live with the database and polynominal regression module
            """
            live = True
            while True:
                #get time
                currenttime = time.struct_time(time.localtime())
                currentminute = currenttime[4]
                currenthour = currenttime[3]
                currentday = currenttime[6]


                #updates alreadyStreamed to current day
                if alreadyStreamed[0] == True and alreadyStreamed[1] != currentday and live == False:
                    alreadyStreamed = [False,currentday]
                    save()
                
                
                contents = requests.get('https://www.twitch.tv/' +CHANNELNAME).content.decode('utf-8')
                
                #search for stream title
                title = ""
                try:
                    index = contents.find('description" content="') #len 22
                    index += 23
                    end_index = contents.find('"',index)
                    for char in range(index, end_index):
                        title += contents[char]
                except Exception:
                    pass
                
                #see if streamer is online, also if are or have streamed
                if 'isLiveBroadcast' in contents: 
                    if live == False:
                        if alreadyStreamed[0] == False:
                            print(f"{CHANNELNAME} is live                                            ",end="\r")
                            playsound.playsound("auughhh.mp3")
                            #log it to database (its only an integrer i know, the database is only used for predicting streams)
                            week[currentday][currenthour] +=1
                            alreadyStreamed = [True,currentday]
                            live = True
                            save()
                            resList = []
                            #update resList
                            for i in range(len(combinedDays)):
                                resList.append(combinedDays[i]+monday[i]+tuesday[i]+wednesday[i]+thursday[i]+friday[i]+saturday[i]+sunday[i])
                
                #setting up prediction
                xpoints = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
                ypoints = resList

                #polynominal regression module
                model = np.poly1d(np.polyfit(xpoints,ypoints,12))
                line = np.linspace(0,23,100)

                #we use the module to get a prediction for the current time
                prediction = round((model(currenthour+currentminute/60)/sum(resList))*100,1)
        

                if 'isLiveBroadcast' in contents:
                    print(f"{CHANNELNAME} is live / avoiding misinput / {title[:30]}...                                         ",end="\r")
                    alreadyStreamed = [True,currentday]
                    streamEndHour = copy.copy(currenthour)
                    save()

                elif alreadyStreamed[0] == True and alreadyStreamed[1] == currentday and live == False:
                    print(f"{CHANNELNAME} already streamed today / overall probability {prediction}%                                                     ",end="\r")
                    live = False
                
                else:
                    print(f"{CHANNELNAME} is not live / overall probability {prediction}%                                                     ",end="\r")
                    live = False
                
                time.sleep(60)
        elif userinput == "todaysresults":
            #uses current day for graph and predictions
            currenttime = time.struct_time(time.localtime())
            currentminute = currenttime[4]
            currentday = currenttime[6]
            currenthour = currenttime[3]
            currentdaytxt = WEEKSTR[currentday]
            

            xpoints = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
            ypoints = week[currentday]

            model = np.poly1d(np.polyfit(xpoints,ypoints,12))
            line = np.linspace(0,23,100)

            prediction = round((model(currenthour+currentminute/60)/sum(week[currentday]))*100,1)
            print(f"current odds:{prediction}%")

            for j in range(len(xpoints)):
                print(f"{str(j)}: {round((model(j)/sum(week[currentday]))*100,1)}%")

            print("accuracy:", r2_score(ypoints, model(xpoints)))

            plt.title(currentdaytxt)
            plt.plot(xpoints,ypoints)
            plt.plot(line,model(line))
            plt.grid()
            plt.show()
        
        elif userinput == "results":
            #uses resList for graph and predictions
            currenttime = time.struct_time(time.localtime())
            currentminute = currenttime[4]
            currentday = currenttime[6]
            currenthour = currenttime[3]

            resList = []
            for i in range(len(combinedDays)):
                resList.append(combinedDays[i]+monday[i]+tuesday[i]+wednesday[i]+thursday[i]+friday[i]+saturday[i]+sunday[i])

            xpoints = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
            ypoints = resList

            model = np.poly1d(np.polyfit(xpoints,ypoints,12))
            line = np.linspace(0,23,100)

            prediction = round((model(currenthour+currentminute/60)/sum(resList))*100,1)
            print(f"current odds: {prediction}%")

            for j in range(len(xpoints)):
                print(f"{str(j)}: {round((model(j)/sum(resList))*100,1)}%")

            print("accuracy:", r2_score(ypoints, model(xpoints)))

            plt.plot(xpoints,ypoints)
            plt.plot(line,model(line))
            plt.grid()
            plt.show()
            
        #simple console mostly used for deleting misinputs from the listener
        elif userinput =="console":
            while True:
                consoleInput = input("console: ")
                if consoleInput == "help":
                    print("graph(day)\nsave()\nback")
                    continue
                try:
                    exec(consoleInput)
                except:
                    if consoleInput == "back":
                        break
                    else:
                        print("ran into a problem")
        elif userinput =="help":
            print("input\nresults\ntodaysresults\ndata\nlisten\nconsole")
            
            
            
def datainput(WEEKSTR):
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
            except ValueError:
                break





if __name__=="__main__": main()
