# oton openworld peli ඞ

import pygame
from pygame.locals import *
import os
import math
import getopt
import random
from socket import *
import copy
import time
import pygame_widgets
from pygame_widgets.button import Button


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

def load_png(name):
    #kuvat pelihi
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    return image, image.get_rect()



class Creature:
    def __init__(self, level, health, strenght, skill, dexterity, agility, medical, skillPoints, winner):
        self.level = level
        self.health = health
        self.strenght = strenght
        self.skill = skill
        self.dexterity = dexterity
        self.agility = agility
        self.medical = medical
        self.skillPoints = skillPoints
        self.winner = winner
        self.health = health+100*self.level
        self.skillPoints = level*100-(self.health-100)-(self.strenght-10)-(self.skill-10)-(self.dexterity-10)-(self.medical-10)


class Playermarker(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("playericon.png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 2
        self.state = "still"
        self.movepos = [0,0]
        self.currentAngle = 0
        self.reinit()
    
    def reinit(self):
        self.state = "still"
        self.movepos = [0,0]
        self.rect.center = self.area.center
        

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()
    
    def moveup(self):
        self.movepos[1] -= self.speed
        self.state = "moveup"
        self.angle = 0
        print("moving up      ",end="\r")

    def moveleft(self):
        self.movepos[0] -= (self.speed)
        self.state = "moveleft"
        self.angle = 90
        print("moving left    ",end="\r") 
    
    def movedown(self):
        self.movepos[1] += (self.speed)
        self.state = "movedown"
        self.angle = 180
        print("moving down    ",end="\r")

    def moveright(self):
        self.movepos[0] += (self.speed)
        self.state = "moveright"
        self.angle = 270
        print("moving right    ",end="\r")

    def rotate(self):
        #print(self.angle)
        for i in range(0,4):
            if self.angle == 90*i:
                #print(i*90-self.currentAngle)
                self.image = pygame.transform.rotate(self.image, i*90-self.currentAngle)
                self.currentAngle = i*90
        #print(self.currentAngle)

class menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("menuwindow.png")
        self.image = pygame.transform.scale(self.image, (500,500))
        screen = pygame.display.get_surface()
        self.area = screen.get_rect() 
        self.menufont = pygame.font.Font(os.path.join(data_dir, "ARCADECLASSIC.TTF"),24)
        self.resumeButton = Button(
            screen,
            10,
            20,
            70,
            30,
            text="resume",
            onClick=lambda: self.resumeButton.clicked
            
            )
        self.skillsButton = Button(
            screen,
            10,
            60,
            70,
            30,
            text="skills",
            onClick=lambda: self.skillsButton.clicked
            )
        self.addHealthButton = Button(
            screen,
            130,
            62,
            20,
            20,
            text="+",
            onClick=lambda: self.addHealthButton.clicked
            )
        self.addStrenghtButton = Button(
            screen,
            130,
            102,
            20,
            20,
            text="+",
            onClick=lambda: self.addStrenghtButton.clicked
            )
        self.addSkillButton = Button(
            screen,
            130,
            144,
            20,
            20,
            text="+",
            onClick=lambda: self.addSkillButton.clicked
            )
        self.addDexterityButton = Button(
            screen,
            130,
            183,
            20,
            20,
            text="+",
            onClick=lambda: self.addDexterityButton.clicked
            )
        self.addAgilityButton = Button(
            screen,
            130,
            222,
            20,
            20,
            text="+",
            onClick=lambda: self.addAgilityButton.clicked
            )
        self.addMedicalButton = Button(
            screen,
            130,
            264,
            20,
            20,
            text="+",
            onClick=lambda: self.addMedicalButton.clicked
            )
        
        self.addbuttons = [self.addHealthButton, self.addStrenghtButton,self.addSkillButton,self.addDexterityButton,self.addAgilityButton,self.addMedicalButton]
    def renderskills(self):
        self.skillsList = [player.level, player.health,player.strenght,player.skill,player.dexterity,player.agility,player.medical,player.skillPoints]
        for skill in range(len(self.skillsList)):
            self.skillsList[skill] = str(self.skillsList[skill])
        levelTxt = self.menufont.render("level "+self.skillsList[0],0,(0,0,0))
        healthTxt = self.menufont.render("Health "+self.skillsList[1],0,(0,0,0))
        strenghtTxt = self.menufont.render("Strength "+self.skillsList[2],0,(0,0,0))
        skillTxt = self.menufont.render("Skill "+self.skillsList[3],0,(0,0,0))
        dexterityTxt = self.menufont.render("Dexterity "+self.skillsList[4],0,(0,0,0))
        agilityTxt = self.menufont.render("Agility "+self.skillsList[5],0,(0,0,0))
        medicalTxt = self.menufont.render("Medical "+self.skillsList[6],0,(0,0,0))
        skillPointsTxt = self.menufont.render("skill points  "+self.skillsList[7],0,(0,0,0))
        skills = [levelTxt,healthTxt,strenghtTxt,skillTxt,dexterityTxt,agilityTxt,medicalTxt,skillPointsTxt]
        for i in range(len(skills)):
            screen.blit(skills[i],(160,40*i+20))
        #self.addStrenghtButton.disable()
    
    def open(self, skillsSelected=False):
        clock = pygame.time.Clock()
        isopen = True
        #skillsSelected = False
        self.rect.topleft = self.area.topleft
        while isopen:
            clock.tick(60)
            screen.blit(self.image, self.rect)
            for event in pygame.event.get():
                print(event)
                if event.type == QUIT:
                    pygame.QUIT()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        isopen = False
                elif self.resumeButton.clicked == True:
                    isopen = False
                elif self.skillsButton.clicked == True:
                    self.renderskills()
                    if skillsSelected == False:
                        skillsSelected = True
                    else:
                        skillsSelected = False
                if player.skillPoints >= 1:
                    if self.addHealthButton.clicked == True:
                        player.health +=10
                        player.skillPoints -=10
                    elif self.addStrenghtButton.clicked == True:
                        player.strenght +=10
                        player.skillPoints -=10
                    elif self.addSkillButton.clicked == True:
                        player.skill +=10
                        player.skillPoints -=10
                    elif self.addDexterityButton.clicked == True:
                        player.dexterity +=10
                        player.skillPoints -=10
                    elif self.addAgilityButton.clicked == True:
                        player.agility +=10
                        player.skillPoints -=10
                    elif self.addMedicalButton.clicked == True:
                        player.medical +=10
                        player.skillPoints -=10
            if skillsSelected == True:
                for button in self.addbuttons:
                    button.enable()
                    button.show()
                    self.renderskills()
            else:
                for button in self.addbuttons:
                    button.disable()
                    button.hide()


            pygame_widgets.update(events=pygame.event.get())
            pygame.display.flip()
            
    
class Objective(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("objective.png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.currentlocation = [0,0]

    def spawn(self):
        self.location = [
        random.randint(50,450),
        random.randint(50, 450)
        ] 
        self.currentlocation[0] *= -1
        self.currentlocation[1] *= -1
        newpos = self.rect.move(self.currentlocation)
        self.rect = newpos
        newpos = self.rect.move(self.location)
        self.rect = newpos
        self.currentlocation = copy.copy(self.location)
        pygame.event.pump()
        if pygame.Rect.colliderect(playersprite.rect, objective.rect):
            self.spawn()

class FightScene(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("fightscene.png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = self.area.topleft

    def battle(self):
        global enemy,player
        enemyLevel = player.level * random.uniform(0.5,1.5)
        enemyLevel = round(enemyLevel)
        enemypoints = 100*enemyLevel
        print("enemylevel:", enemyLevel)
        print("enemypoints:", enemypoints)
        rngStat1 = random.randint(0,enemypoints)
        enemypoints -= rngStat1
        rngStat2 = random.randint(0,enemypoints)
        enemypoints -= rngStat2
        rngStat3 = random.randint(0,enemypoints)
        enemypoints -= rngStat3
        rngStat4 = random.randint(0,enemypoints)
        enemypoints -= rngStat4
        rngStat5 = random.randint(0,enemypoints)
        enemypoints -= rngStat5
        rngStat6 = random.randint(0,enemypoints)
        enemypoints -= rngStat6

        rngList = [rngStat1, rngStat2, rngStat3, rngStat4, rngStat5, rngStat6,]
        rngList = random.shuffle(rngList)
        enemy = Creature(
            enemyLevel,
            rngStat1+100*enemyLevel,
            rngStat2,
            rngStat3,
            rngStat4,
            rngStat5,
            rngStat6,
            enemypoints,
            False
        )
        print("health:",enemy.health)
        print("strenght:",enemy.strenght)
        print("skill:",enemy.skill)
        print("dexterity:", enemy.dexterity)
        print("agility:", enemy.agility)
        print("medical:", enemy.medical)
        print("\n")

        if player.agility > enemy.agility:
            starter = player
            finisher = enemy
        else:
            starter = enemy
            finisher = player

        fightscene = FightScene()

        clock = pygame.time.Clock()
        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == quit:
                    pygame.QUIT()

            screen.blit(self.image,self.rect)
            pygame.display.flip()

def main():
    global screen, player, objective
    pygame.init()

    player = Creature(1,0,10,10,10,10,10,100,False)

    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption("game...")


    floor = load_png("floor.png")
    backround = pygame.Surface(screen.get_size())
    backround = backround.convert()

    screen.blit(floor[0], (0,0))
    pygame.display.flip()

    global playersprite
    playersprite = Playermarker()
    playermarkersprite = pygame.sprite.RenderPlain((playersprite))
    
    clock = pygame.time.Clock()

    mainmenu = menu()
    fightscene = FightScene()

    objective = Objective()
    objective.spawn()
    mainmenu.open(skillsSelected=True)
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    playersprite.moveup()
                    playersprite.rotate()
                if event.key == K_a:
                    playersprite.moveleft()
                    playersprite.rotate()
                if event.key == K_s:
                    playersprite.movedown()
                    playersprite.rotate()
                if event.key == K_d:
                    playersprite.moveright()
                    playersprite.rotate()
                if event.key == K_ESCAPE:
                    mainmenu.open()
            elif event.type == KEYUP:
                if event.key ==  K_w or event.key ==  K_a or event.key ==  K_s or event.key ==  K_d:
                    playersprite.movepos = [0,0]
                    print("still       ",end="\r")
                    
        if pygame.Rect.colliderect(playersprite.rect, objective.rect):
              print("colliding",end="\r")
              objective.spawn()
              fightscene.battle()
        screen.blit(backround, playersprite.rect)
        screen.blit(floor[0], (0,0))
        screen.blit(objective.image, objective.rect)
        playermarkersprite.update()
        playermarkersprite.draw(screen)
        pygame.display.flip()

if __name__=="__main__": main()


