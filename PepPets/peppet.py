#!/usr/bin/env python
from asyncio import Task
from datetime import datetime, time
import mysql.connector as mysql
import random
import time as timer
from threading import Thread
from numpy import byte
import serial
import board
import EmailParent
from Hardware.pedometer.steps import track_steps
from Hardware.OLED.menubutton import *
# from Hardware.progressbar.progress_bar import progress, initpins, clear
from tasks import TaskFactory


# ---------------- Database credential variables ----------------------
HOST = "db-mysql-sfo2-96686-do-user-11317347-0.b.db.ondigitalocean.com"
DATABASE = "peppetEMAIL"
PORT = 25060
USER = "doadmin"
PASSWORD = "AVNS_1OJ-Nk7eUgMXbec"
# db = mysql.connect(host=HOST, database=DATABASE,
#                        user=USER, password=PASSWORD, port=PORT)
# cursor = db.cursor()
# print("connected to: ", db.get_server_info())

# ---------------- Serial Port Info -----------------------------------
ser = serial.Serial(port='/dev/serial0', baudrate = 9600, timeout=1)


# ---------------- 10 Segment LED Info --------------------------------
# bar1 = [4,17,27,22, 10]
# bar2 = [9, 11, 5, 6, 13]
# bar3 = [14, 15, 18, 23, 24]

# ---------------- Global Day/Night Tracker---------------------------
NIGHT = False
COOLDOWN = False

# ---------------- Global Food and Weights----------------------------
class Food:
    def __init__(self, name="Chicken", hunger=1, happiness=0, exp=0):
        self.name = name
        self.hunger_gain = hunger
        self.happiness_gain = happiness
        self.exp = exp

WALKING_FOODS = ["nothing",
                 Food("steak", 3, 0, 5),
                 Food("fish", 1, 1, 5),
                 Food("pineapple", 1, 1, 10),
                 Food("cake", 1, 3, 15),
                 Food("bread", 2, 0, 15)]
WALKING_FOOD_WEIGHTS = [100, 60, 20, 15, 10, 10]

FRIEND_FOODS = [Food("lollipop", 0, 1, 30),
                Food("boba", 1, 2, 15)]

# ---------------- Main Pep Pet Class -------------------------------
class PepPet:
    # Metrics
    happiness = 0
    hunger = 10
    experience = 0
    level = 0
    face = "depressed"
    # Info
    name = "Pep Pet 1"
    unique_id = 1
    global_steps = 0

    tasks = {"walk": None, "feed": None, "connect": None, "sustain": None}
    closet = []
    # Dictionary of food name values mapped to the quantity of that food
    foods = {"Chicken": 9999}
    friends = []

    # Construct a Pep Pet with a name
    def __init__(self, name, id):
        self.unique_id = id
        self.name = name
        self.resetTasks()


    def resetTasks(self):
        self.tasks = dict.fromkeys(self.tasks, None)
        task_types = ["walk", "feed", "connect", "sustain"]
        types = random.sample(task_types, 3)
        for task_type in types:
            self.tasks[task_type] = TaskFactory(task_type)
    
    def rewardTask(self, task):

        if  task.done and not task.rewarded:
            task.setRewarded()
            self.addExperience(task.getReward())
            print("%s finished a task! You earned %i XP." % (self.name, task.getReward()))

    """
    Feed your Pep Pet a food. Will adjust the Pet's happiness, hunger, and exp depending on the food stats
    Arguments:
        - food : a Food object
    """

    def feed(self, food):
        if food.name not in self.foods or self.foods[food.name] == 0:
            print("Unable to eat this food")
            print("----------------------------")
            return
        print("Feeding " + self.name + " " + food.name)
        self.addHappiness(food.happiness_gain)
        self.addHunger(food.hunger_gain)
        self.addExperience(food.exp)
        self.foods[food.name] -= 1

        # Update feeding task if it exists
        feed_task = self.tasks["feed"]
        if feed_task != None:
            feed_task.addProgress(1)
            self.rewardTask(feed_task)
    

    def addExperience(self, value):
        # Check if the Pep Pet can level up and do so if necessary
        self.experience += value
        if self.experience >= 100:
            self.level += 1
            self.experience = self.experience - 100
            # self.levelUp()

    def levelUp(self):
        print(self.name + " leveled up to level " + self.level)
        print("----------------------------")

        # match self.level:
        #     case 1:
        #         self.closet.append("sunglasses")
        #     case 2:
        #         self.closet.append("eyepatch")
        #         # TODO: do rest of this
        #     case _: 
        #         return


    def addHunger(self, value):
        self.hunger += value
        if self.hunger < 0:
            self.hunger = 0
        if self.hunger > 10:
            self.hunger = 10
            # Overfeeding makes the Pet unhappy.
            self.addHappiness(-1)
            print("You overfed " + self.name)
        self.setMood()

        print("----------------------------")

    def addHappiness(self, value):
        self.happiness += value
        # Stats are maxed at 10
        if self.happiness > 10:
            self.happiness = 10
        if self.happiness < 0:
            self.happiness = 0
        self.setMood()

        sustain_task = self.tasks["sustain"]
        if sustain_task != None: 
            if self.happiness < sustain_task.threshold:
                sustain_task.failTask()

            

    """
    Add a Food item to the Pep Pet's inventory.
    Arguments:
        - food : a Food object
    """

    def collectFood(self, food):
        if food.name in self.foods:
            self.foods[food.name] += 1
        else:
            self.foods[food.name] = 1


    """
    Functions to randomly fluctuate hunger/happiness over the course of the day
    The current naive implementation is to randomly decide to decrease hunger every 5 seconds.
    In the real device it should take much longer (every 5 minutes, every hour maybe)
    """

    def hungerControl(self):
        while not NIGHT:
            timer.sleep(30)
            random_int = random.randint(0, 9)
            if random_int < 5:
                print("Decrease hunger now")
                self.addHunger(-1)

    def happinessControl(self):
        while not NIGHT:
            timer.sleep(30)
            random_int = random.randint(0, 9)
            if random_int > 5:
                print("Decrease happiness now")
                print("----------------------------")
                self.addHappiness(-1)

    '''
    Connect with another Pep Pet
    Arguments:
    - friend: A String representing the name of the Pep Pet being connected with. 
    It will get added to our Pet's friend list. Depending on if we have already met them or not,
    our Pet will gain a certain amount of experience and happiness. 
    '''

    def connectWithFriend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)
            print(self.name + "made a new friend: " + friend)
            self.addHappiness(5)
            self.addExperience(30)
            self.collectFood(FRIEND_FOODS[0])
            EmailParent.sendEmail(self.petID)
        else:
            print("It's nice to meet " + friend + "again!")
            self.addHappiness(3)
            self.addExperience(15)
            self.collectFood(FRIEND_FOODS[1])

        if self.tasks["connect"] != None:
            self.tasks["connect"].setDone()
        print("----------------------------")

    '''
    Calculate the Pet's mood according the hunger and happiness
    Logic: If hunger < 3, mood defaults to "hungry"
           If happiness < 3, mood defaults to one of "depressed", "sad", "bored", "unhappy"
            Otherwise, take the average of the 2 metrics and assign mood based on that. (index of moods list)
    '''

    def setMood(self):
        # Will have to associate with right picture in hardware
        moods = ["excited", "happy", "fine", "mischievious", "neutral",
                 "bored", "confused", "sad", "angry", "crying", "sick"]

        if self.hunger < 3:
            self.face = "hungry"
        if self.happiness < 3:
            self.face = random.choice(["depressed", "sad", "bored", "unhappy"])
        else:
            face_num = int((self.hunger + self.happiness)/2)
            self.face = moods[10 - face_num]

    def movementTracker(self):
        while not NIGHT:
            self.showPet()
            
            if track_steps():
                self.global_steps += 10
                print(self.name + " has walked " + str(self.global_steps))

                # Only get happier on a full stomach. Walking while hungry lowers happiness
                if (self.hunger == 0):
                    self.addHappiness(-1)
                else:
                    self.addHappiness(1)
            # Every 150 steps the Pet gains 1 EXP
            if self.global_steps % 150 == 0:
                self.addExperience(1)

            
            if self.global_steps % 25 == 0:
                # Every 25 steps hunger goes down 1 and there is a chance to pick up a random food!
                self.addHunger(-1)
                # Pick a random food (foods have different weights)
                found_food = random.choices(
                    WALKING_FOODS, weights=WALKING_FOOD_WEIGHTS, k=1)[0]
                if found_food != "nothing":
                    print(self.name + " found " +
                          found_food.name + " while walking!")
                    self.collectFood(found_food)
                else:
                    print("Did not find anything")

            walk_task = self.tasks["walk"]
            if walk_task != None:
                walk_task.addProgress(10)
                self.rewardTask(walk_task)
            self.setMood()
            print("----------------------------")

    # def showPetbar(self):  
    #     while not NIGHT:
    #         progress(bar3, self.hunger)
    #         progress(bar2, self.happiness)
    #         progress(bar1, int(self.experience/10))
    #         timer.sleep(.5)

    def buttonListener(self, press_idx):
        moods = {"depressed" : "/menu/madge.png",
        "unhappy" : "/menu/happy.png",
        "bored" : "/menu/happy.png",
        "sad" : "/menu/happy.png"}
        activepage = "facepage"
        activeoption = "menu"
        # Doesn't actually take any input YET, just prints the state of pet every 7 seconds.
        while not NIGHT:
            if activepage == "facepage":
                if activeoption == "menu":
                    press_idx = 1
                if activeoption == "feed":
                    press_idx = 2
                faceIdle(press_idx,"/menu/madge.png")

                if detect()[0] and activeoption == "feed":
                    activeoption = "menu"
                elif detect()[2] and activeoption == "menu":
                    activeoption = "feed"
                if detect()[1]:
                    if activeoption == "menu":
                        activepage = "menupage"
                        activeoption = "task"
                    elif activeoption == "feed":
                        activepage = "foodpage"
                        activeoption = 0
                    
                

            elif activepage == "menupage":
                # menupage()

                # cursor on task
                if activeoption == "task":
                    if detect()[1]:
                        activepage = "taskpage"
                        activeoption = "backtomenu"
                        
                    elif detect()[2]:
                        activeoption = "friends"
                        

                # cursor on friends
                elif activeoption == "friends":
                    if detect()[0]:
                        activeoption = "task"
                        
                    elif detect()[1]:
                        activepage = "friendspage"
                        activeoption = "backtomenu"
                        
                    elif detect()[2]:
                        activeoption = "back"
                        

                # cursor on back
                elif activeoption == "back":
                    if detect()[0]:
                        activeoption = "friends"
                    elif detect()[1]:
                        activepage = "facepage"
                        activeoption = "menu"
                        

            elif activepage == "taskpage":
                # taskpage()

                if detect()[1]:
                    activepage = "menupage"
                    activeoption = "task"
                    

            elif activepage == "friendspage":
                # friendspage()

                if detect()[1]:
                    activepage = "menupage"
                    activeoption = "task"

            # default cursor on chicken
            elif activepage == "foodpage":
                feedPage()
                listoffoods = list(self.foods.keys())
                lastfood = len(listoffoods) - 1

                if activeoption == 0:
                    if detect()[0]:
                        activepage = "facepage"
                        activeoption = "menu"
                    elif detect()[1]:
                        print("feeding " + listoffoods[activeoption])
                        # feed(listoffoods[activeoption])
                    elif detect()[2]:
                        activeoption += 1

                elif activeoption == lastfood:
                    if detect()[0]:
                        activeoption -= 1
                    elif detect()[1]:
                        print("feeding " + listoffoods[activeoption])
                        # feed(listoffoods[activeoption])
                    elif detect()[2]:
                        activepage = "facepage"
                        activeoption = "menu"

                else:
                    if detect()[0]:
                        activeoption -= 1
                    elif detect()[1]:
                        print("feeding " + listoffoods[activeoption])
                        # feed(listoffoods[activeoption])
                    elif detect()[2]:
                        activeoption += 1
            print(activepage)
            print(activeoption)
            time.sleep(0.1)

    def showPet(self):
        print("Name: " + self.name)
        print("Hunger: " + str(self.hunger))
        print("Happiness: " + str(self.happiness))
        print(self.name + " is feeling " + self.face)
        print("    Level:  " + str(self.level))
        print("    Experience: " + str(self.experience))
        print("Foods: " + str(self.foods))
        # print(self.tasks)
        for task in self.tasks.values():
            if task != None:
                task.printTask()
        print("----------------------------")
    
    def receiveMessage(self):
        while not COOLDOWN:
            x=ser.readline()
            print(x)
            x.encode("ascii", 'ignore')

            if x == "Chonk":
                self.connectWithFriend(x)
                COOLDOWN = True
        # TODO: Write to table that Beans is friends with Chonk and Chonk is friends with Beans  

    def writeMessage(self):
        while not NIGHT:
            ser.write(bytes(self.name, "utf-8"))
            ser.flush()
            print("sending")
            timer.sleep(1)


'''
Thread 1: Hunger control: Fluctuates hunger over time
Thread 2: Happiness control: Fluctuates happiness over time
Thread 3: Pedometer/Step counter: Keeps track of steps and changes metrics depending on that
Thread 4: Button listener: Handles user input (feeding, customization, etc)
Thread 5: Bar Control: Displays metric changes on the actual Pep Pet
Thread 6/7: Read/write data on serial port continuously for friend connections
'''
# setup()
# press_idx = 1
# # initpins(bar1)
# initpins(bar2)
# initpins(bar3)
# clear(bar1)
# clear(bar2)
# clear(bar3)
myPet = PepPet("Beans", 123456)
# myPet.showPet()
steak = Food("Steak", 3, 1, 30)
# chicken = Food("Chicken")

print("here")

hungerLoss = Thread(target=myPet.hungerControl)
happinessLoss = Thread(target=myPet.happinessControl)
movementTrack = Thread(target=myPet.movementTracker)
buttonControl = Thread(target=myPet.buttonListener, args=(press_idx,))
# progressBar = Thread(target=myPet.showPetbar)
writeID = Thread(target=myPet.writeMessage)
readID = Thread(target=myPet.receiveMessage)

# PepPetThreads = [hungerLoss, happinessLoss, movementTrack, buttonControl, progressBar, writeID, readID]

print("here2")
# Start hunger and happiness fluctuators
hungerLoss.start()
happinessLoss.start()
movementTrack.start()
buttonControl.start()
# progressBar.start()
# writeID.start()
# readID.start()

myPet.collectFood(steak)
myPet.collectFood(steak)
# while True:
#     now = datetime.now()
#     now_time = now.time()
#     if now_time >= time(13,13) and now_time <= time(13,14):
#         print(now_time)
#         print ("It's night")
#         NIGHT = True
#     else:
#         print("It's day")
#         if NIGHT: 
#             NIGHT = False
#             COOLDOWN = False
#             # The Pet passively gains 5 exp every day
#             myPet.addExperience(5)
#             # We just woke up and should reset our tasks and restart our threads
#             myPet.resetTasks()
#             hungerLoss = Thread(target=myPet.hungerControl)
#             happinessLoss = Thread(target=myPet.happinessControl)
#             movementTrack = Thread(target=myPet.movementTracker)
#             buttonControl = Thread(target=myPet.buttonListener)
#             progressBar = Thread(target=myPet.showPetbar)
#             # PepPetThreads = [movementTrack, buttonControl, progressBar]
#             movementTrack.start()
#             buttonControl.start()
#             progressBar.start()
#         NIGHT = False
    
#     #Wait an hour before checking again
#     timer.sleep(10)


# # # myPet.hungerControl()
# 

# myPet.showPet()
# myPet.feed(steak)
# # # myPet.feed(chicken)

# myPet.showPet()
