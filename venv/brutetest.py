import random
from threading import Thread
from tqdm import *
import time

def makelist():
    global newpasswordlist, testedpasswords, run, letters
    letters = [
    "A","B","C","D",
    "E","F","G","H",
    "J","K","L","M",
    "N","O","P","Q",
    "R","S","T","U",
    "V","W","X","Y",
    "Z"]
    #"1","2","3","4",
    #"5","6","7","8",
    #"9","0"]
    newpasswordlist = []
    testedpasswords = []
    while True:
        while run:
            guess = ""
            for i in range(1,password.count("")):
                guess += random.choice(letters)
            if  guess not in testedpasswords:
                newpasswordlist.append(guess)
            else:
                try:
                    newpasswordlist.remove(guess)
                    #print(guess, "was removed")
                except:
                    continue

def main():
    global testedpasswords, passwordlist, newpasswordlist, run, vittu, password
    password = input("input: ")
    testedpasswords = []
    vittu = len(letters)**(password.count("")-1)
    run = True
    passwordlist = newpasswordlist
    while True:
        for i in tqdm(range(vittu),desc=str(len(testedpasswords))):
            if len(newpasswordlist) != 0:
                passwordlist += newpasswordlist
                for guess in range(len(passwordlist)):
                    i +=1
                    if passwordlist[guess] == password:
                        print("\n")
                        print("password guessed:")
                        input(passwordlist[guess])
                    else:
                        testedpasswords.append(passwordlist[guess])
        passwordlist.clear()
        passwordlist += newpasswordlist
        newpasswordlist.clear()
            




if __name__=="__main__": 
    run = False
    t1 = Thread(target=makelist)
    t1.start()
    main()


