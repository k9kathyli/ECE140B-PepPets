import time
import random
from concurrent.futures import thread
from threading import Thread
from Hardware.pedometer.steps import track_steps


class Food:
    def __init__(self, name="Chicken", hunger=1, happiness=0, exp=0):
        self.name = name
        self.hunger_gain = hunger
        self.happiness_gain = happiness
        self.exp = exp


edibles = [Food("chicken", 1),
           Food("steak", 3, 0, 5),
           Food("fish", 1, 1, 5),
           Food("pineapple", 2, 1, 10)]


class PepPet:
    # Metrics
    happiness = 0
    hunger = 0
    experience = 0
    level = 0
    face = "depressed"
    # Info
    name = "Pep Pet 1"
    global_steps = 0

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
            print(self.name + " leveled up!")
            print("----------------------------")

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
                myPet.showPet()

    # Calculate the Pet's mood according the hunger and happiness

    def setMood(self):
        # Will have to associate with right picture in hardware
        moods = ["excited", "happy", "fine", "mischievious", "neutral",
                 "bored", "confused", "sad", "angry", "crying", "sick"]

        # Logic: If hunger < 3, mood defaults to "hungry"
        #        If happiness < 3, mood defaults to one of "depressed", "sad", "bored", "unhappy"
        #        Otherwise, take the average of the 2 metrics and assign mood based on that. (index of moods list)
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
                print("----------------------------")
                self.addHappiness(1)

    def buttonListener(self):
        # Doesn't actually take any input, just prints the state of pet every 7 seconds.
        while True:
            self.showPet()

            time.sleep(7)


'''
Thread 1: Hunger control: Fluctuates hunger over time
Thread 2: Happiness control: Fluctuates happiness over time
Thread 3: Pedometer/Step counter: Keeps track of steps and changes metrics depending on that
Thread 4: Button listener: Handles user input (feeding, customization, etc)
'''

myPet = PepPet("Chonk")
# myPet.showPet()
# steak = Food("Steak", 3, 1, 30)
# chicken = Food("Chicken")


hungerLoss = Thread(target=myPet.hungerControl)
happinessLoss = Thread(target=myPet.happinessControl)
movementTrack = Thread(target=myPet.movementTracker)
buttonControl = Thread(target=myPet.buttonListener)
# Start hunger and happiness fluctuators
# hungerLoss.start()
# happinessLoss.start()
movementTrack.start()
buttonControl.start()
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
