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


weekstr = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
CHANNELNAME = 'xqc'


logging.basicConfig(filename='log.txt', level=logging.ERROR, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)


def save():
    with open('data.pckl', 'wb') as file:
        pickle.dump([week, alreadyStreamed], file)
        
def predict(currenthour, currentminute, ypoints):
    
    xpoints = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    
    #polynominal regression module
    model = np.poly1d(np.polyfit(xpoints,ypoints,deg=5))
    line = np.linspace(0,23,100)
    
    #we use the module to get a prediction for the current time
    prediction = round((model(currenthour+currentminute/60)/sum(resList))*100,1)
    return prediction, line, model


def graph(isResList):
    #uses resList or current day for graph and predictions

    currenttime = time.struct_time(time.localtime())
    currentminute = currenttime[4]
    currentday = currenttime[6]
    currenthour = currenttime[3]
    if not isResList:
        currentdaytxt = weekstr[currentday]
        mode = week[currentday]
    else:
        mode = resList


    xpoints = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    ypoints = mode
   
    prediction, line, model = predict(currenthour,currentminute,mode)
    print(f"current odds:{prediction}%")

    for j in range(len(xpoints)):
        print(f"{str(j)}: {round((model(j)/sum(mode))*100,1)}%")

    print("accuracy:", r2_score(ypoints, model(xpoints)))
    if not isResList:
        plt.title(currentdaytxt)
    plt.plot(xpoints,ypoints)
    plt.plot(line,model(line))
    plt.grid()
    plt.show()

def data():
    #calc resList again since it may have changed
            resList = []
            for i in range(len(combinedDays)):
                resList.append(combinedDays[i]+week[0][i]+week[1][i]+week[2][i]+week[3][i]+week[4][i]+week[5][i]+week[6][i])
            print("/////WEEKDAYS/////")
            for day in week:
                print(day)
            print("////WHOLE WEEK////")
            print(resList)
            
            
def datainput():
    #manually add logs to database
    run = True
    x = False
    while run:
        
        dayInput = input("day: ")
        for d in range(7):
            for lenght in range(1,weekstr[d].__len__()):
                if dayInput == weekstr[d][:lenght]:
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

def main():
    global week, userinput, alreadyStreamed, combinedDays, resList

   

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

    
    


    while True:
        

        userinput = input("=>")
        if userinput == "input":
            datainput()
            
        elif userinput == "data":
            data()
        
        elif userinput =="listen":
            """
            checks if tracked streamer goes live and adds it into database
            also displays prediction on streamer going live with the database and polynominal regression module
            """
            live = True
            while True:
                try:
                    try:
                        os.system("cls")
                        
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
                            index += 22
                            end_index = contents.find('"',index)
                            for char in range(index, end_index):
                                title += contents[char]
                        except Exception:
                            pass
                        
                        #see if streamer is online, also avoid misinput if have streamed already
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


                        prediction,line,model = predict(currenthour,currentminute,resList)



                        if 'isLiveBroadcast' in contents:
                            print(f"{CHANNELNAME} is live / avoiding misinput / {title}",end="\r")
                            alreadyStreamed = [True,currentday]
                            streamEndHour = copy.copy(currenthour)
                            save()

                        elif alreadyStreamed[0] == True and alreadyStreamed[1] == currentday and live == False:
                            print(f"{CHANNELNAME} already streamed today / overall probability {prediction}%",end="\r")
                            live = False

                        else:
                            print(f"{CHANNELNAME} is not live / overall probability {prediction}%",end="\r")
                            live = False
                        #print(60/model(line[currenthour]))
                        time.sleep(60/model(line[currenthour]))
                    except KeyboardInterrupt:
                        os.system("cls")
                        break
                except Exception as err:
                    logging.exception(err)
                
                
        elif userinput == "todaysresults":
            graph(False)
           
        
        elif userinput == "results":
            graph(True)
        
        
        elif userinput == "cls":
            os.system("cls")
            
            
        #simple console
        elif userinput =="console":
            while True:
                consoleInput = input("console: ")
                if consoleInput == "help":
                    print("graph(isResList)\nsave()\nback")
                    continue
                try:
                    exec(consoleInput)
                except:
                    if consoleInput == "back":
                        break
                    else:
                        print("ran into a problem")
        elif userinput =="help":
            print("input\nresults\ntodaysresults\ndata\nlisten\nconsole\ncls")
            






if __name__=="__main__": main()



