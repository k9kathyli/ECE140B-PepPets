'''
Task types:
    - "walk" : Walk x number of steps
    - "connect": Connect with a friend or make a new friend
    - "feed" : Feed x number of times
    - "sustain": Keep above certain happiness or hunger all day 
'''


from asyncio import Task
from locale import currency
import random

STEP_COUNTS = [10, 20, 30, 40]
FOOD_COUNTS = [5, 6, 7, 8]
HAPPINESS_THRESHOLDS = [5, 6, 7, 8]

class WalkTask:
    current_steps = 0
    done = False
    def __init__(self):
        self.num_steps = random.choice(STEP_COUNTS)
    def printTask(self):
        status = "     "
        if self.done: 
            status = "DONE "
        
        print("%s - Walk %d steps. %d/%d " % (status, self.num_steps, self.current_steps, self.num_steps))
    def addProgress(self, steps):
        self.current_steps += steps
        if self.current_steps >= self.num_steps:
            self.done = True

class FeedTask:
    current_food = 0
    done = False

    def __init__(self): 
        self.feed_times = random.choice(FOOD_COUNTS)
    def printTask(self):
        status = "     "
        if self.done: 
            status = "DONE "
        
        print("%s- Eat %d non-infinite foods. %d/%d" % (status, self.feed_times, self.current_food, self.feed_times))
    def addProgress(self, num):
        self.current_food += num
        if self.current_food >= self.feed_times:
            done = True

class ConnectTask:
    def printTask(self):
        print("     - Connect with 1 friend today." )

class SustainHappinessTask: 
    def __init__(self): 
        self.threshold = random.choice(HAPPINESS_THRESHOLDS)
    def printTask(self):
        print("     - Keep your pet above " + str(self.threshold) + " happiness until bedtime.")

def TaskFactory(task_type):
    tasks = {
        "walk" : WalkTask,
        "feed" : FeedTask,
        "connect" : ConnectTask,
        "sustain" : SustainHappinessTask
    }
    return tasks[task_type]()

# Test generating some tasks using our factory.
# In order to generate a task of a type, use this syntax: wt = TaskFactory("walk")
if __name__ == "__main__": 
    wt = TaskFactory("walk")
    ft = TaskFactory("feed")
    ct = TaskFactory("connect")
    st = TaskFactory("sustain")

    wt.printTask()
    wt.addProgress(69)
    wt.printTask()
    # ft.printTask()
    # ct.printTask()
    # st.printTask()

