import random
import time
import copy


points = 1
defeat = False
fullskip = False

#ehkä jopa gameplay eikä pelkkä rng
#abilityjä
#eri pelimuotoja esim semmonen josson eri viholliset joka lvl
#vihollisia nerffaa sen verran että ei oo perseestä
#ei permadeath
#savefile
#mainmenu
#bosseja ehkä myöhemmin
#classeja
#agilitylle toinen turni jos vittuna agilityä
#skilli parryy ja antaa toisen hyökkäyksen
#medical voi hiilata
class Player:
    def __init__(self, id, name, health, strenght, skill, dexterity, agility, medical, winner, damageDone):
        self.id = id
        self.name = name
        self.health = health
        self.strenght = strenght
        self.skill = skill
        self.dexterity = dexterity
        self.agility = agility
        self.medical = medical
        self.winner = winner
        self.damageDone = damageDone
        

def mainmenu():
    pass


def gameover():
    global Player1, Player2, bet, points, defeat, skip, fullskip, skip_amount
    winner = None
    if Player1.winner == True:
        winner = Player1.name
        print("\n")
        print(Player1.name, "won!")
        print("\n")
    elif Player2.winner == True:
        winner = Player2.name
        print("\n")
        print(Player2.name, "won!")
        print("\n")

    if bet == winner:
        points +=1
        try:
            skip_amount -= 1
            if skip_amount <= 0:
                fullskip = False
                skip = False
        except:
            pass
        defeat = False
        if points == 10:
            print("YOU WIN")
            if input("endless (y/n)") == "y":
                pass
            else:
                quit()

        
    else:
        defeat = True
        
        
    print("level: ", points)
    if not fullskip:
        input("press enter to continue")


def hit_event(self, enemy, multiplier, roll):

    health = copy.copy(enemy.health)
    dodge = enemy.dexterity - self.skill
    heal_amount = random.randint(1,100*points+self.medical*2)
    if random.randint(1,10) < roll:
        if random.randint(1,100*points*2) > self.skill:

            if random.randint(1,5) == 1:
                print(self.name, "accidentally hit himself!", self.strenght*multiplier)
                self.health -= self.strenght*multiplier
            else:
                print(self.name, "missed!")
        else:
            if heal_amount < self.medical:
                print(self.name, "just healed +", self.medical - heal_amount)
                self.health += self.medical - heal_amount
            if enemy.dexterity >= points*66:
                dodge = points*66
            if dodge <= random.randint(1,100*points):
                enemy.health -= self.strenght*multiplier
                print(self.name, "did", self.strenght*multiplier, "damage skillfully")
            else:
                print(enemy.name, "dodged the attack")
    else:    
        if heal_amount < self.medical:
            print(self.name, "just healed +", self.medical - heal_amount)
            self.health += self.medical - heal_amount
        if enemy.dexterity >= points*66:
            dodge = points*66
        if dodge <= random.randint(1,100*points):
            enemy.health -= self.strenght*multiplier
            print(self.name, "did", self.strenght*multiplier, "damage")
        else:
            print(enemy.name, "dodged the attack")
        
    if enemy.health < 0:
        enemy.health = 0
    self.damageDone = self.damageDone + health - enemy.health
    return self.damageDone, enemy.health
        

def attack(self):
    roll = random.randint(1, 10)
    if self.id == 0:
        enemy = Player2
    elif self.id == 1:
        enemy = Player1
    
    if enemy.skill >= random.randint(1,self.skill+points*100):
       if 1 == random.randint(1,2):
            print(enemy.name,"parried the attack")
            attack(enemy)
            #print("total damage done: ",enemy.damageDone)
            print(self.name, "'s health:", self.health)
            
            return self, enemy

    if roll == 1:
        hit_event(self, enemy, 0.2, roll)
    elif roll == 2:
        hit_event(self, enemy, 0.3, roll)
    elif roll == 3:
        hit_event(self, enemy, 0.4, roll)
    elif roll == 4:
        hit_event(self, enemy, 0.5, roll)
    elif roll == 5:
        hit_event(self, enemy, 0.6, roll)
    elif roll == 6:
        hit_event(self, enemy, 0.7, roll)
    elif roll == 7:
        hit_event(self, enemy, 0.8, roll)
    elif roll == 8:
        hit_event(self, enemy, 1, roll)
    elif roll == 9:
        hit_event(self, enemy, 1.5, roll)
    elif roll == 10:
        hit_event(self, enemy, 3, roll)
    
    return self, enemy

    
def start():
    global Player1, Player2, white, black, bet, points, skip, counter, Player1_stats, Player2_stats, Player1_stats_backup, Player2_stats_backup, fullskip, skip_amount
    if not "Player1" in globals():
        Player1 = Player(0, "red", 1, 1, 1, 1, 1, 1, False, 0)
        Player2 = Player(1, "blue", 1, 1, 1, 1, 1, 1, False, 0)
        Player1_stats = [50,10,10,0,0,0]
        Player2_stats = [50,10,10,0,0,0]
    if not fullskip:
        skip = False
    counter = 0
    if not defeat:
        damageDone1 = Player1.damageDone
        damageDone2 = Player2.damageDone
        rng_points = 100*points
        
        rng_stat1 = random.randint(0,rng_points)
        rng_points -= rng_stat1

        rng_stat2 = random.randint(0,rng_points)
        rng_points -= rng_stat2

        rng_stat3 = random.randint(0,rng_points)
        rng_points -= rng_stat3

        rng_stat4 = random.randint(0,rng_points)
        rng_points -= rng_stat4

        rng_stat5 = random.randint(0,rng_points)
        rng_points -= rng_stat5

        rng_stat6 = random.randint(0,rng_points)
        rng_points -= rng_stat6

        rng_list = [rng_stat1, rng_stat2, rng_stat3, rng_stat4, rng_stat5, rng_stat6]
        random.shuffle(rng_list)
        Player1 = Player(0, "red", 
        Player1_stats[0] + rng_list[0], 
        Player1_stats[1] + rng_list[1], 
        Player1_stats[2] + rng_list[2], 
        Player1_stats[3] + rng_list[3], 
        Player1_stats[4] + rng_list[4], 
        Player1_stats[5] + rng_list[5], 
        False, damageDone1)

        rng_points = 100*points

        rng_stat1 = random.randint(0,rng_points)
        rng_points -= rng_stat1

        rng_stat2 = random.randint(0,rng_points)
        rng_points -= rng_stat2

        rng_stat3 = random.randint(0,rng_points)
        rng_points -= rng_stat3

        rng_stat4 = random.randint(0,rng_points)
        rng_points -= rng_stat4

        rng_stat5 = random.randint(0,rng_points)
        rng_points -= rng_stat5

        rng_stat6 = random.randint(0,rng_points)
        rng_points -= rng_stat6

        rng_list = [rng_stat1, rng_stat2, rng_stat3, rng_stat4, rng_stat5, rng_stat6]
        random.shuffle(rng_list)
        Player2 = Player(1, "blue", 
        Player2_stats[0] + rng_list[0], 
        Player2_stats[1] + rng_list[1], 
        Player2_stats[2] + rng_list[2], 
        Player2_stats[3] + rng_list[3], 
        Player2_stats[4] + rng_list[4], 
        Player2_stats[5] + rng_list[5], 
        False, damageDone2)

        Player1_stats = [
            Player1.health,
            Player1.strenght,
            Player1.skill,
            Player1.dexterity,
            Player1.agility,
            Player1.medical
        ]
        Player2_stats = [
            Player2.health,
            Player2.strenght,
            Player2.skill,
            Player2.dexterity,
            Player2.agility,
            Player2.medical
        ]
        Player1_stats_backup = copy.copy(Player1_stats)
        Player2_stats_backup = copy.copy(Player2_stats)
    else:
        Player1_stats = Player1_stats_backup
        Player2_stats = Player2_stats_backup
        Player1 = Player(0, "red",
        Player1_stats[0],
        Player1_stats[1],
        Player1_stats[2],
        Player1_stats[3],
        Player1_stats[4],
        Player1_stats[5],
        False, 0)

        Player2 = Player(1, "blue", 
        Player2_stats[0],
        Player2_stats[1],
        Player2_stats[2],
        Player2_stats[3],
        Player2_stats[4],
        Player2_stats[5],
        False, 0)


    if Player1.agility >= Player2.agility:
        white = Player1
        black = Player2
    else:
        white = Player2
        black = Player1

    print("RED (you)")
    print("health: ",Player1_stats[0])
    print("strenght: ",Player1_stats[1])
    print("skill: ",Player1_stats[2])
    print("dexterity: ", Player1_stats[3])
    print("agility: ", Player1_stats[4])
    print("medical: ", Player1_stats[5])
    print("\n")

    print("BLU")
    print("health: ",Player2_stats[0])
    print("strenght: ",Player2_stats[1])
    print("skill: ",Player2_stats[2])
    print("dexterity: ", Player2_stats[3])
    print("agility: ", Player2_stats[4])
    print("medical: ", Player2_stats[5])
    print("\n")

    Player1.damageDone = 0
    Player2.damageDone = 0
    
    bet = Player1.name
    if not fullskip:
        if input("press enter to continue") == "skip":
            skip_amount = int(input("levels to skip: "))
            skip = True
            fullskip = True


def gameloop():
    global skip, counter
    while True:
        counter +=1
        if counter >= 10000:
            if input("there has been ten thousand rounds. wanna give up? (y/n): ") == "y":
                Player1.winner = True
                skip = False
                break
            counter = 0
        if Player1.health <= 0:
            Player2.winner = True
            break
        elif Player2.health <= 0:
            Player1.winner = True
            break
        else:
                print(white.name, "turn")
                attack(white)
                #print("total damage done: ",white.damageDone)
                print(black.name, "'s health:", black.health)
                print("\n")
                if white.agility >= black.agility*2:
                    print(white.name, "turn")
                    attack(white)
                    #print("total damage done: ",white.damageDone)
                    print(black.name, "'s health:", black.health)
                if black.health <= 0:
                    white.winner = True
                    break
                        
        if not skip:
            time.sleep(5)
        print("\n")
        
        if Player1.health < 0:
            Player2.winner = True
            
        elif Player2.health < 0:
            Player1.winner = True
            
        else:
                print(black.name, "turn")
                attack(black)
                #print("total damage done: ",black.damageDone)
                print(white.name, "'s health:", white.health)
                print("\n")
                if black.agility >= white.agility*2:
                    print(black.name, "turn")
                    attack(black)
                    #print("total damage done: ",black.damageDone)
                    print(white.name, "'s health:", white.health)
                if white.health <= 0:
                    black.winner = True
                    break
                        
        if not skip:
            if input("press enter to continue") == "skip":
                skip = True
        print("\n")


if __name__=="__main__":
    while True:
        if "Player1" in globals():
            if Player1.winner == True:
                gameover()
            elif Player2.winner == True:
                gameover()

        start()

        gameloop()
    


