from asyncio import Task
from locale import currency
import random

from friends import check_friend, add_friend
from parent_tasks import get_task

'''
Task types:
    - "walk" : Walk x number of steps
    - "connect": Connect with a friend or make a new friend
    - "feed" : Feed x number of times
    - "sustain": Keep above certain happiness or hunger all day 
'''

STEP_COUNTS = [10, 20, 30, 40]
FOOD_COUNTS = [5, 6, 7, 8]
HAPPINESS_THRESHOLDS = [5, 6, 7, 8]
EXP_REWARD = [5, 10, 15, 20, 25]

class Task:
    done = False
    rewarded = False
    def __init__(self, user): 
        self.reward = random.choice(EXP_REWARD)
        print(self.reward)
    def setDone(self):
        self.done = True
    def setRewarded(self):
        self.rewarded = True
    def getReward(self):
        return self.reward

class WalkTask(Task):
    current_steps = 0
    def __init__(self, user):
        Task.__init__(self, user)
        self.num_steps = random.choice(STEP_COUNTS)
    def printTask(self):
        if self.done: 
            status = "DONE"
        return ("Walk %d steps. %d/%d" % (self.num_steps, self.current_steps, self.num_steps))
    def addProgress(self, steps):
        self.current_steps += steps
        if self.current_steps >= self.num_steps:
            self.done = True

class FeedTask(Task):
    current_food = 0
    def __init__(self, user): 
        Task.__init__(self, user)
        self.feed_times = random.choice(FOOD_COUNTS)
    def printTask(self):
        status = "    "
        if self.done: 
            status = "DONE"
        return ("Eat %d non-infinite foods. %d/%d" % (self.feed_times, self.current_food, self.feed_times))
    def addProgress(self, num):
        self.current_food += num
        if self.current_food >= self.feed_times:
            done = True

class ConnectTask(Task):
    def checkIfFriend(self, user, friend):
        if(check_friend(user, friend)):
            print("You have already connected with this friend")
    def addNewFriend(self, user, friend):
        if(not(check_friend(user, friend))):
            add_friend(user, friend)
            print("Connected with new friend")
    def printTask(self):
        return ("Connect with 1 friend today." )

class SustainHappinessTask(Task): 
    success = True
    def __init__(self, user): 
        Task.__init__(self, user)
        self.threshold = random.choice(HAPPINESS_THRESHOLDS)
    def printTask(self):
        if self.done: 
            status = "DONE"
        if not self.success:
            status = "FAIL"
        return ("Keep your pet above %i happiness until bedtime." % (self.threshold))
    def failTask(self):
        success = False

class CustomTask(Task):
    taskstring = ""
    def __init__(self, user): 
        Task.__init__(self, user)
        self.retrieveTask(user)
    def retrieveTask(self, user):
        self.taskstring = get_task(user)

    def printTask(self):
        return self.taskstring

def TaskFactory(task_type, user):
    tasks = {
        "walk" : WalkTask,
        "feed" : FeedTask,
        "connect" : ConnectTask,
        "sustain" : SustainHappinessTask,
        "custom"  : CustomTask
    }
    return tasks[task_type](user)

# Test generating some tasks using our factory.
# In order to generate a task of a type, use this syntax: wt = TaskFactory("walk")
if __name__ == "__main__": 
    wt = TaskFactory("walk")
    ft = TaskFactory("feed")
    ct = TaskFactory("connect")
    st = TaskFactory("sustain")

    wt.printTask()
    wt.addProgress()
    wt.printTask()
    # ft.printTask()
    # ct.printTask()
    # st.printTask()

