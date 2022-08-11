import random
from tqdm import tqdm
from statistics import mode, median
import matplotlib.pyplot as plt


def simulated():
    while True:
        input("press enter to continue")
        chance = float(1.435)
        resultList = []
        success = 0
        counter = 0
        for i in tqdm(range(1000000)):
            primogems = 120
            tries = 0
            counter +=1
            for j in range(13):
                dailyPrimogems = 480
                primogems += dailyPrimogems
                while primogems >= 160 and tries < 90:
                    if primogems >= 160:
                        tries +=1
                        primogems -= 160
                        if random.uniform(0,100) <= chance or tries >= 90:
                            resultList.append(tries)
                            success +=1
                            break
                
        #print(sorted(resultList))
        averagetries = sum(resultList) / len(resultList)
        print(f"keskimäärin {averagetries} yritystä")
        print(f"mode:{mode(resultList)}")
        print(f"median:{median(resultList)}")
        print(f"success is {(success/counter)*100}%")
        indexList = list(dict.fromkeys(sorted(resultList)))
        countList = [] 
        for i in range(len(indexList)):
            countList.append(resultList.count(resultList[resultList.index(indexList[i])]))
            print(f"{indexList[i]}: {countList[i]}")
        
        plt.plot(indexList,countList)
        plt.show()

        #print(resultList)


def calculated():
    
    while True:
        chance_to_get = float(input("wanted % to pull this banner:"))
        time_left = int(input("time left:"))
        chance = 1.435

        print(f"needed pulls a day for {chance_to_get}% is {(chance_to_get/chance)/time_left}")

        

if __name__=="__main__": calculated()
