"""
idea olis että kaks tyyppiä taistelee toisiaansa vastaan ja paranee ajallaan evoluution tai tekoälyn kautta emt.
saman tyylinen kun EvE mutta paremmin organisoitu.
hirvee työmää ei jaks lol teen joskus....
"""
import random
import copy

import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class Person:
    name: str
    xHistory: list
    yHistory: list
    xPointer: float = 0.50
    yPointer: float = 0.50
    cxPointer: float = copy.copy(xPointer)
    cyPointer: float = copy.copy(yPointer)
    agility: int = 100*(1-xPointer)
    health: int = 100*xPointer
    strength: int = 100*yPointer
    skill: int = 100*(1-yPointer)

    def calc_stats(self,won=bool):
        if won:
            self.xPointer += self.xPointer-self.cxPointer
            self.yPointer += self.yPointer-self.cyPointer
            if self.xPointer >= 1: self.xPointer = 0.99
            elif self.xPointer <= 0: self.xPointer = 0.01
            if self.yPointer >= 1: self.yPointer = 0.99
            elif self.yPointer <= 0: self.yPointer = 0.01
            self.xHistory.append(self.xPointer)
            self.yHistory.append(self.yPointer)
            self.health   = round(100*self.xPointer)
            self.strength = round(100*self.yPointer)
            self.agility  = round(100*(1-self.xPointer))
            self.skill    = round(100*(1-self.yPointer))
            if self.name == "red":
                winList.append(1)
            else:
                winList.append(0)
        else:
            self.cxPointer = copy.copy(self.xPointer)
            self.cyPointer = copy.copy(self.yPointer)
            self.xPointer += random.uniform(-0.05,0.05)
            self.yPointer += random.uniform(-0.05,0.05)
            if self.xPointer >= 1: self.xPointer = 0.99
            elif self.xPointer <= 0: self.xPointer = 0.01
            if self.yPointer >= 1: self.yPointer = 0.99
            elif self.yPointer <= 0: self.yPointer = 0.01
            self.xHistory.append(self.xPointer)
            self.yHistory.append(self.yPointer)
            self.health   = round(100*self.xPointer)
            self.strength = round(100*self.yPointer)
            self.agility  = round(100*(1-self.xPointer))
            self.skill    = round(100*(1-self.cyPointer))

    def attack(self,enemy):
        dodge = enemy.agility - self.skill
        x = random.uniform(0,1)
        if random.randint(1,100) <= 50:
            if random.randint(1,100) > self.skill:

                if random.randint(1,5) == 1:
                    
                    print(f"{self.name} accidentally hit himself! {self.strength*x}")
                    self.health -= self.strength*x
                else:
                    print(f"{self.name} missed!")
            else:
                if dodge <= random.randint(1,100):
                    enemy.health -= self.strength
                    print(f"{self.name} did {self.strength} damage skillfully")
                else:
                    print(f"{enemy.name} dodged the attack")
        else:    
            if dodge <= random.randint(0,100):
                enemy.health -= self.strength*x
                print(f"{self.name} did {self.strength*x} damage")
            else:
                print(f"{enemy.name} dodged the attack")

        if enemy.health < 0:
            enemy.health = 0


def battle(first,finish):
    while True:
        first.attack(finish)
        print(f"{finish.name} health: {finish.health}")
        if finish.health <= 0:
            print(f"{first.name} won")
            first.calc_stats(True)
            finish.calc_stats(False)
            break
        finish.attack(first)
        print(f"{first.name} health: {first.health}")
        if first.health <= 0:
            print(f"{finish.name} won")
            first.calc_stats(False)
            finish.calc_stats(True)
            break
        if input("\n") == "plot":
            plot()


def plot():
    ax = plt.gca()
    ax.set_ylim([0, 1])
    plt.grid()
    x = [x for x in range(len(red.xHistory))]
    plt.plot(x,red.xHistory,color="r")
    plt.plot(x,red.yHistory,color="m")
    plt.plot(x,blue.xHistory,color="b")
    plt.plot(x,blue.yHistory,color="c")
    plt.scatter(x,winList,color="g")
    plt.legend(["red health / agility","red strength / skill","blue health / agility","blue strength / skill","red=1 / blue=0"])
    plt.show()


def main():
    global red,blue, winList
    red = Person("red",[],[])
    blue = Person("blue",[],[])
    winList = []
    while True:
        if input() == "plot":
            plot()
        print(f"name:{red.name}\nhealth:{red.health}\nagility:{red.agility}\nstrength:{red.strength}\nskill:{red.skill}\nxPointer:{red.cxPointer}\nyPointer:{red.cyPointer}\n\n")
        print(f"name:{blue.name}\nhealth:{blue.health}\nagility:{blue.agility}\nstrength:{blue.strength}\nskill:{blue.skill}\nxPointer:{blue.cxPointer}\nyPointer:{blue.cyPointer}\n\n")
        if red.agility > blue.agility:
            battle(red,blue)
        elif red.agility < blue.agility:
            battle(blue,red)
        else:
            x = random.randint(1,2)
            if x == 1:
                battle(red,blue)
            else:
                battle(blue,red)


if __name__=="__main__":
    main()

