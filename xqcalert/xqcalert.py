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
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0

def save():
    with open('data.pckl', 'wb') as file:
        pickle.dump([week, alreadyStreamed], file)


    

def graph(day):
    xpoints = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    ypoints = day
    print(day)
    plt.step(xpoints,ypoints,where="mid")
    plt.grid()
    plt.show()



def main():
    global week, userinput, alreadyStreamed
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


    
    cd0, cd1, cd2, cd3, cd4, cd5, cd6, cd7, cd8, cd9, cd10, cd11, cd12, cd13, cd14, cd15, cd16, cd17, cd18, cd19, cd20, cd21, cd22, cd23 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    combinedDays = [cd0, cd1, cd2, cd3, cd4, cd5, cd6, cd7, cd8, cd9, cd10, cd11, cd12, cd13, cd14, cd15, cd16, cd17, cd18, cd19, cd20, cd21, cd22, cd23]
    resList = []
    for i in range(len(combinedDays)):
        resList.append(combinedDays[i]+monday[i]+tuesday[i]+wednesday[i]+thursday[i]+friday[i]+saturday[i]+sunday[i])

    

    channelName = 'xqc'

    while True:
        if afk == False:
            userinput = input("=>")
        if userinput == "input":
            while True:
                dayInput = input("back / day: ")
                if dayInput == "mo":
                    day = monday
                elif dayInput == "tu":
                    day = tuesday
                elif dayInput == "we":
                    day = wednesday
                elif dayInput == "th":
                    day = thursday
                elif dayInput == "fr":
                    day = friday
                elif dayInput == "sa":
                    day = saturday
                elif dayInput == "su":
                    day = sunday
                elif dayInput == "back":
                    break
                while True:
                    try:
                        hourInput = int(input("back / hour: "))
                        for i in range(24):
                            if hourInput == i:
                                hour = i
                                break


                        day[hour] +=1
                        if dayInput == "mo":
                            week[0] = monday
                        elif dayInput == "tu":
                            week[1] = tuesday
                        elif dayInput == "we":
                            week[2] = wednesday
                        elif dayInput == "th":
                            week[3] = thursday
                        elif dayInput == "fr":
                            week[4] = friday
                        elif dayInput == "sa":
                            week[5] = saturday
                        elif dayInput == "su":
                            week[6] = sunday
                        save()

                    except:
                        break
        elif userinput == "data":
            resList = []
            for i in range(len(combinedDays)):
                resList.append(combinedDays[i]+monday[i]+tuesday[i]+wednesday[i]+thursday[i]+friday[i]+saturday[i]+sunday[i])
            print("/////WEEKDAYS/////")
            for day in week:
                print(day)
            print("////WHOLE WEEK////")
            print(resList)
        
        elif userinput =="listen":
            live = True
            counter = 0
            while True:
                counter += 1
                currenttime = time.struct_time(time.localtime())
                currentminute = currenttime[4]
                currenthour = currenttime[3]
                currentday = currenttime[6]
                if currentday == 0:
                    currentday2 = monday
                elif currentday == 1:
                    currentday2 = tuesday
                elif currentday == 2:
                    currentday2 = wednesday
                elif currentday == 3:
                    currentday2 = thursday
                elif currentday == 4:
                    currentday2 = friday
                elif currentday == 5:
                    currentday2 = saturday
                elif currentday == 6:
                    currentday2 = sunday


                if alreadyStreamed[0] == True and alreadyStreamed[1] != currentday and live == False:
                    alreadyStreamed = [False,currentday]
                    save()
                
                contents = requests.get('https://www.twitch.tv/' +channelName).content.decode('utf-8')
                title = ""
                try:
                    index = contents.find('description" content="') #len 22
                    index += 23
                    end_index = contents.find('"',index)
                    for char in range(index, end_index):
                        title += contents[char]
                except Exception:
                    pass
                if 'isLiveBroadcast' in contents: 
                    if live == False:
                        if alreadyStreamed[0] == False:
                            print(f"{channelName} is live                                            ",end="\r")
                            playsound.playsound("auughhh.mp3")
                            currentday2[currenthour] +=1
                            if currentday == 0:
                                week[0] = monday
                            elif currentday == 1:
                                week[1] = tuesday
                            elif currentday == 2:
                                week[2] = wednesday
                            elif currentday == 3:
                                week[3] = thursday
                            elif currentday == 4:
                                week[4] = friday
                            elif currentday == 5:
                                week[5] = saturday
                            elif currentday == 6:
                                week[6] = sunday
                            
                            alreadyStreamed = [True,currentday]
                            
                            live = True
                            save()
                            resList = []
                            for i in range(len(combinedDays)):
                                resList.append(combinedDays[i]+monday[i]+tuesday[i]+wednesday[i]+thursday[i]+friday[i]+saturday[i]+sunday[i])
                
                xpoints = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
                ypoints = resList

                model = np.poly1d(np.polyfit(xpoints,ypoints,12))
                line = np.linspace(0,23,100)

                prediction = round((model(currenthour+currentminute/60)/sum(resList))*100,1)
        

                if 'isLiveBroadcast' in contents:
                    print(f"{channelName} is live / avoiding misinput / {title[:30]}...                                         ",end="\r")
                    alreadyStreamed = [True,currentday]
                    streamEndHour = copy.copy(currenthour)
                    save()

                elif alreadyStreamed[0] == True and alreadyStreamed[1] == currentday and live == False:
                    print(f"{channelName} already streamed today / overall probability {prediction}%                                                     ",end="\r")
                    live = False
                
                else:
                    print(f"{channelName} is not live / overall probability {prediction}%                                                     ",end="\r")
                    live = False
                
                time.sleep(60)
        elif userinput == "todaysresults":
            currenttime = time.struct_time(time.localtime())
            currentminute = currenttime[4]
            currentday = currenttime[6]
            currenthour = currenttime[3]
            if currentday == 0:
                currentdaytxt = "monday"
            elif currentday == 1:
                currentdaytxt = "tuesday"
            elif currentday == 2:
                currentdaytxt = "wednesday"
            elif currentday == 3:
                currentdaytxt = "thursday"
            elif currentday == 4:
                currentdaytxt = "friday"
            elif currentday == 5:
                currentdaytxt = "saturday"
            elif currentday == 6:
                currentdaytxt = "sunday"
            

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
            #print(model(line))

            print("accuracy:", r2_score(ypoints, model(xpoints)))

            plt.plot(xpoints,ypoints)
            plt.plot(line,model(line))
            plt.grid()
            plt.show()
            
        
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





if __name__=="__main__": main()



