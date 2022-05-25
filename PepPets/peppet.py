from stat import FILE_ATTRIBUTE_NO_SCRUB_DATA
import time
import random
from concurrent.futures import thread
from threading import Thread

import EmailParent
from cv2 import add
from Hardware.pedometer.steps import track_steps
from Hardware.progressbar.progress_bar import progress, initpins, clear

bar1 = [4,17,27,22, 10]
bar2 = [9, 11, 5, 6, 13]
bar3 = [14, 15, 18, 23, 24]

class Food:
    def __init__(self, name="Chicken", hunger=1, happiness=0, exp=0):
        self.name = name
        self.hunger_gain = hunger
        self.happiness_gain = happiness
        self.exp = exp


walking_foods = ["nothing",
                 Food("steak", 3, 0, 5),
                 Food("fish", 1, 1, 5),
                 Food("pineapple", 1, 1, 10),
                 Food("cake", 1, 3, 15),
                 Food("bread", 2, 0, 15)]
walking_food_weights = [100, 60, 20, 15, 10, 10]

friend_foods = [Food("lollipop", 0, 1, 30),
                Food("boba", 1, 2, 15)]


class PepPet:
    # Metrics
    happiness = 0
    hunger = 10
    experience = 0
    level = 0
    face = "depressed"
    # Info
    name = "Pep Pet 1"
    global_steps = 0
    petID="999555"

    closet = []
    # Dictionary of food name values mapped to the quantity of that food
    foods = {"Chicken": 9999}
    friends = []

    # Construct a Pep Pet with a name
    def __init__(self, name):
        self.name = name

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
        self.setMood()

    def addExperience(self, value):
        # Check if the Pep Pet can level up and do so if necessary
        self.experience += value
        if self.experience >= 100:
            self.level += 1
            self.experience = self.experience - 100
            # self.levelUp()

    # def levelUp(self):
    #     print(self.name + " leveled up to level " + self.level)
    #     print("----------------------------")

    #     match self.level:
    #         case 1:
    #             self.closet.append("sunglasses")
    #         case 2:
    #             # TODO: do rest of this
    #             return

    def addHunger(self, value):
        self.hunger += value
        if self.hunger < 0:
            self.hunger = 0
        if self.hunger > 10:
            self.hunger = 10
            # Overfeeding makes the Pet unhappy.
            if self.happiness != 0:
                self.addHappiness(-1)
            print("You overfed " + self.name)
        print("----------------------------")

    def addHappiness(self, value):
        self.happiness += value
        # Stats are maxed at 10
        if self.happiness > 10:
            self.happiness = 10
        if self.happiness < 0:
            self.happiness = 0

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

    def showPet(self):
        print("Name: " + self.name)
        print("Hunger: " + str(self.hunger))
        print("Happiness: " + str(self.happiness))
        print(self.name + " is feeling " + self.face)
        print("    Level:  " + str(self.level))
        print("    Experience: " + str(self.experience))
        print("Foods: " + str(self.foods))
        print("----------------------------")

    def showPetbar(self):  
        while True:
            progress(bar3, self.hunger)
            progress(bar2, self.happiness)
            progress(bar1, int(self.experience/10))
            time.sleep(.5)


    """
    Functions to randomly fluctuate hunger/happiness over the course of the day
    The current naive implementation is to randomly decide to decrease hunger every 5 seconds.
    In the real device it should take much longer (every 5 minutes, every hour maybe)
    """

    def hungerControl(self):
        for i in range(0, 24):
            time.sleep(10)
            random_int = random.randint(0, 9)
            if random_int < 5:
                print("Fluctuate hunger now")
                self.addHunger(-1)

    def happinessControl(self):
        for i in range(0, 24):
            time.sleep(10)
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
            self.collectFood(friend_foods[0])
            EmailParent.sendEmail(self.petID)
        else:
            print("It's nice to meet " + friend + "again!")
            self.addHappiness(3)
            self.addExperience(15)
            self.collectFood(friend_foods[1])

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
        while True:
            if track_steps():
                self.global_steps += 10
                print(self.name + " has walked " + str(self.global_steps))
                self.addHappiness(1)
            if self.global_steps % 20 == 0:
                # Every 50 steps hunger goes down 1 and there is a chance to pick up a random food!
                self.addHunger(-1)
                # Pick a random food (foods have different weights)
                found_food = random.choices(
                    walking_foods, weights=walking_food_weights, k=1)[0]
                if found_food != "nothing":
                    print(self.name + " found " +
                          found_food.name + " while walking!")
                    self.collectFood(found_food)
                else:
                    print("Did not find anything")
            print("----------------------------")

    def buttonListener(self):
        # Doesn't actually take any input YET, just prints the state of pet every 7 seconds.
        while True:
            self.showPet()

            time.sleep(7)


'''
Thread 1: Hunger control: Fluctuates hunger over time
Thread 2: Happiness control: Fluctuates happiness over time
Thread 3: Pedometer/Step counter: Keeps track of steps and changes metrics depending on that
Thread 4: Button listener: Handles user input (feeding, customization, etc)
'''
initpins(bar1)
initpins(bar2)
initpins(bar3)
clear(bar1)
clear(bar2)
clear(bar3)
myPet = PepPet("Chonk")
# myPet.showPet()
# steak = Food("Steak", 3, 1, 30)
# chicken = Food("Chicken")


hungerLoss = Thread(target=myPet.hungerControl)
happinessLoss = Thread(target=myPet.happinessControl)
movementTrack = Thread(target=myPet.movementTracker)
buttonControl = Thread(target=myPet.buttonListener)
progressbar = Thread(target=myPet.showPetbar)
# Start hunger and happiness fluctuators
# hungerLoss.start()
# happinessLoss.start()
movementTrack.start()
buttonControl.start()
progressbar.start()
# # # myPet.hungerControl()
# myPet.collectFood(steak)
# myPet.collectFood(steak)
# myPet.collectFood(steak)
# # myPet.collectFood(steak)

# myPet.showPet()

# myPet.feed(steak)
# myPet.feed(steak)
# # myPet.feed(steak)
# # myPet.feed(steak)
# # # myPet.feed(chicken)
# # # myPet.feed(chicken)
# # # myPet.feed(chicken)
# # # myPet.feed(chicken)

# myPet.showPet()
