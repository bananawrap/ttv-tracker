import random
import time
import copy

from dataclasses import dataclass, field

AGENT_COUNT = 100
GATHERJOB_COUNT = 2
TRADER_COUNT = 5
TARGET_HUMAN = 0
agents = []
gatherJobs = []
traders = []

price_of_food = 1
counter = 0

@dataclass(order=True)
class Trader():
    sort_index: int = field(init=False)
    name: int
    trader_wealth: int
    food_resource: int
    food_buy_price: int = price_of_food
    food_sell_price: int = price_of_food
    food_buy_price_yesterday: int = price_of_food
    food_sell_price_yesterday: int = price_of_food
    money_made_today: int = 0
    money_made_yesterday: int = 0

    def __post_init__(self):
        self.sort_index = self.food_buy_price
    
    def calculate_food_price(self):
        if self.food_buy_price > 0 and self.food_sell_price > 0:
            #if self.money_made_today >= self.money_made_yesterday:
            #    self.food_buy_price  += self.food_buy_price-self.food_buy_price_yesterday
            #    self.food_sell_price += self.food_sell_price-self.food_sell_price_yesterday
            if self.money_made_today <= self.money_made_yesterday:
                self.food_buy_price  = self.food_buy_price_yesterday
                self.food_sell_price = self.food_sell_price_yesterday
                self.food_buy_price  += random.randint(-1,1)
                self.food_sell_price += random.randint(-1,1)
        else:
            self.food_buy_price += 1
            self.food_sell_price += 2
        self.money_made_yesterday = copy.copy(self.money_made_today)
        self.food_buy_price_yesterday = copy.copy(self.food_buy_price)
        self.food_sell_price_yesterday = copy.copy(self.food_sell_price)
        

 
@dataclass
class GatheringJob():
    name: int
    business_wealth: int
    food_resource: int
    workers: list
    owner: list
    avgsalary: float = 2
    
    def sell_food(self):
        for j in traders:
            target_trader = random.choice(traders)
            if target_trader.food_buy_price >= random.uniform(0,price_of_food) and target_trader.trader_wealth > 0:
                break
        print(f"{self.name} preferred trader:{target_trader.name}")
        for i in range(self.food_resource):
            if self.food_resource > 0 and target_trader.trader_wealth > 0:
                self.food_resource -= 1
                target_trader.food_resource += 1
                self.business_wealth += target_trader.food_buy_price*0.75
                self.owner.money += target_trader.food_buy_price*0.25
                target_trader.trader_wealth -= target_trader.food_buy_price
                target_trader.money_made_today -= target_trader.food_buy_price
    
    def simulate_decision(self):
        if self.owner.business == None:
            self.owner.business = self
        try:
            salaryList = []
            for worker in self.workers:
                salaryList.append(worker.salary)
            self.avgsalary = sum(salaryList)/len(salaryList)
        except ZeroDivisionError:
            pass
        for worker in self.workers:
            if self.avgsalary*len(self.workers) > self.business_wealth:
                self.workers.pop(self.workers.index(worker))
                worker.job = None
        self.sell_food()
        if self.owner.alive == False:
            for child in self.owner.children:
                if child.alive == True:
                    child.money += self.business_wealth
                    self.business_wealth = 0
            del self

    



@dataclass
class Gatherer():
    name: int
    money: int
    food: int
    working_efficiency: int
    children: list
    business: GatheringJob = None
    job: int = None
    salary: int = 0
    alive: bool = True

    
    def work(self):
        
        if self.job  == None:
            food_gathered = round(random.randint(1,2)*self.working_efficiency)
            self.working_efficiency += food_gathered/1000
            self.food += food_gathered
        else:
            food_gathered = round(random.randint(1,20)*self.working_efficiency)
            self.working_efficiency += food_gathered/1000
            gatherJobs[self.job].food_resource += food_gathered
            if gatherJobs[self.job].business_wealth > self.salary:
                self.money += self.salary
                gatherJobs[self.job].business_wealth -= self.salary

    def look_for_job(self):
        #salary = round(target_job.business_wealth/100*self.working_efficiency*price_of_food)
        for i in range(3):
            target_job = random.choice(gatherJobs)
            salary = round(random.uniform(1,price_of_food*3)*self.working_efficiency)
            if salary > 0 and target_job.avgsalary*len(target_job.workers) < target_job.business_wealth:
                if salary > price_of_food*5:
                    self.job = target_job.name
                    gatherJobs[self.job].workers.append(self)
                    self.salary = salary
                    #print(f"{self.name} got a job at {target_job.name} with a salary of {salary}")
                    break
                elif salary > random.uniform(1,price_of_food*5):
                    self.job = target_job.name
                    gatherJobs[self.job].workers.append(self)
                    self.salary = salary
                    #print(f"{self.name} got a job at {target_job.name} with a salary of {salary}")
                    break


    def buy_food(self):
        for i in range(len(traders)):
            target_trader = random.choice(traders)
            try:
                if target_trader.food_sell_price < random.uniform(0,price_of_food*2) and target_trader.food_resource > 0:
                    break
            except ValueError:
                break
        for j in range(random.randint(1,10)):
            if self.money > 0 and target_trader.food_resource > 0:
                target_trader.food_resource -= 1
                self.food += 1
                self.money -= target_trader.food_sell_price
                target_trader.trader_wealth += target_trader.food_sell_price
                target_trader.money_made_today += target_trader.food_sell_price
        
        
    def simulate_decision(self):
        self.food -= random.randint(1,3)
        if self.alive:
            if self.job == None and self.business == None:
                if random.randint(1,3) == 1:
                    self.look_for_job()
            elif not self.job == None:
                if self.salary < price_of_food*4 or gatherJobs[self.job].business_wealth < 100 and self.business == None:
                      if random.randint(1,3) == 1:
                          #print(f"{self.name} resigned from {self.job}")
                          gatherJobs[self.job].workers.pop(gatherJobs[self.job].workers.index(self))
                          self.job = None
                          self.look_for_job()
            if random.randint(1,2) == 1 and self.business == None:
                self.work()
            elif not self.job == None and self.business == None:
                self.work()
            else:
                self.working_efficiency -= 0.001
                
            if random.randint(1,3) == 1:
                self.buy_food()
            if self.food <= 0 :
                self.buy_food()
                if self.food <= 0:
                    self.buy_food()
                    if self.food <= 0:
                        try:
                            gatherJobs[self.job].workers.pop(gatherJobs[self.job].workers.index(self))
                            #print(f"{self.name} resigned from {self.job}")
                            self.job = None
                        except TypeError:
                            pass
                        except ValueError:
                            pass
                        self.work()
                        if self.food <= 0:
                            print(f"{self.name} died of hunger")
                            try:
                                gatherJobs[self.job].workers.pop(gatherJobs[self.job].workers.index(self))
                            except TypeError:
                                pass
                            #except ValueError:
                            #    pass
                            self.alive = False
                for child in self.children:
                    if child.food < 3:
                        if self.food > 3:
                            self.buy_food()
                            self.food  -= 3 - child.food
                            child.food += 3 - child.food
                if random.randint(1,5) == 1 and self.money >= 20:
                    agents.append(Gatherer(len(agents),20,0,random.uniform(0.5,2),[]))
                    self.money -= 20
                    self.children.append(agents[-1])

                if random.randint(1,5) == 1 and self.money > price_of_food*100:
                    if not self.business:
                        gatherJobs.append(GatheringJob(len(gatherJobs),price_of_food*100,0,[],self))
                        self.money -= price_of_food*10
                    else:
                        self.business.business_wealth += price_of_food*100
                        self.money -= price_of_food*100



        
def populate_agents():
    global agents, gatherJobs, traders,target
    agents = [Gatherer(i,random.randint(1,1000),3,random.uniform(0.5,2),[]) for i in range(AGENT_COUNT)]
    gatherJobs = [GatheringJob(i,random.randint(100,1000),0,[],random.choice(agents)) for i in range(GATHERJOB_COUNT)]
    traders = [Trader(i,random.randint(100,10000),10) for i in range(TRADER_COUNT)]
    target = agents[TARGET_HUMAN]




def iterate_time():
    global price_of_food, counter
    priceList = []
    for job in gatherJobs:
        job.simulate_decision()
    for agent in agents:
        agent.simulate_decision()
    for x in traders:
        priceList.append(x.food_sell_price)
    price_of_food = sum(priceList)/len(priceList)
    for trader in traders:
        trader.calculate_food_price()
        if trader.trader_wealth <= 0:
            counter +=1
            traders.append(Trader(len(traders)+counter,random.randint(100,1000),10))
            try:
                traders.remove(trader)
            except ValueError:
                pass
            del trader
    print("\n")



def main():
    global target
    populate_agents()
    for job in gatherJobs:
        print(job)
    print("\n")
    for trader in traders:
        trader.calculate_food_price()
        print(trader)
    print("\n")

    while True:
        iterate_time()
        if not target.alive:
            target = agents[-1]
        population = 0
        for agent in agents:
            if agent.alive:
                population += 1
        print("\n")
        for job in gatherJobs:
            print(f"gathering job {job.name}\nowner:{job.owner.name}\nwealth:{job.business_wealth}\nfood:{job.food_resource}\nworkers:{len(job.workers)}\navg salary:{job.avgsalary}")
            print("\n")
        print("\n")
        print("\n")
        for trader in traders:
            print(f"trader {trader.name}\nwealth:{trader.trader_wealth}\nfood:{trader.food_resource}\nbuy price:{trader.food_buy_price}\nsell price:{trader.food_sell_price}\nmoney made:{trader.money_made_today}")
            trader.money_made_today = 0
            print("\n")
        print("\n")
        print(f"price of food:{price_of_food}")
        print(f"population{population}")
        print("\n")
        print(f"gatherer {target.name}\nmoney:{target.money}\nfood:{target.food}\nchildren:{len(target.children)}\njob:{target.job}\nsalary:{target.salary}\nalive:{target.alive}\nworking efficiency:{target.working_efficiency}")
        input("press enter to goto next day")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        

if __name__=="__main__":
    main()
    