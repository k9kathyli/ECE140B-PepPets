
class PepPet:
    # Metrics
    happiness = 0
    hunger = 0
    experience = 0
    level = 0

    # Info
    name = "Pep Pet 1"

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

        self.happiness += food.happiness_gain
        self.hunger += food.hunger_gain
        self.experience += food.exp

        # Stats are maxed at 10
        if (self.happiness > 10):
            self.happiness = 10

        if (self.hunger > 10):
            self.hunger = 10
            # Overfeeding makes the Pet unhappy.
            if (self.happiness != 0):
                self.happiness -= 1
            print("You overfed " + self.name)
        print("----------------------------")

        self.foods[food.name] -= 1
        self.levelUp()

    """
    Check if the Pep Pet can level up and do so if necessary
    """

    def levelUp(self):
        if (self.experience >= 100):
            self.level += 1
            self.experience = self.experience - 100

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
        print("Level:  " + str(self.level))
        print("Experience: " + str(self.experience))
        print("Foods: " + str(self.foods))
        print("----------------------------")


class Food:
    def __init__(self, name="Chicken", hunger=1, happiness=0, exp=0):
        self.name = name
        self.hunger_gain = hunger
        self.happiness_gain = happiness
        self.exp = exp


myPet = PepPet("Chonk")
myPet.showPet()
steak = Food("Steak", 3, 1, 30)
chicken = Food("Chicken")

myPet.collectFood(steak)
myPet.collectFood(steak)
myPet.collectFood(steak)
myPet.collectFood(steak)

myPet.showPet()

myPet.feed(steak)
myPet.feed(steak)
myPet.feed(steak)
myPet.feed(steak)
myPet.feed(chicken)
myPet.feed(chicken)
myPet.feed(chicken)
myPet.feed(chicken)

myPet.showPet()
