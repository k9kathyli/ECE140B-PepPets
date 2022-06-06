import board
import busio
from PIL import Image, ImageOps, ImageDraw, ImageFont
import Adafruit_SSD1306
import RPi.GPIO as GPIO
import time

leftArrowPin = 16
middleSelectPin = 20
rightArrowPin = 21
PATH = "/home/pi/Desktop/ECE140B-PepPets/PepPets/Hardware/OLED"

# 128 x 64 pixel display

# Default font
font = ImageFont.truetype(PATH + "/arial.ttf", 8)

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
# Create the SSD1306 OLED class.
disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)

# Clear display.
disp.begin()
disp.clear()
disp.display()

# Create blank image for drawing, mode '1' for 1-bit color.
width = disp.width
height = disp.height
y_offset = -2

# Face
def faceIdle(press_idx, mood):
    disp.clear()

    image = Image.open(PATH + mood).resize((disp.width, disp.height), Image.ANTIALIAS).convert('L')
    image = ImageOps.invert(image)
    image=image.convert('1')
    draw = ImageDraw.Draw(image)

    if(press_idx % 2 == 1):
        draw.line((12, y_offset+33, 36, y_offset+33), fill=255)
    else:
        draw.line((52, y_offset+33, 72, y_offset+33), fill=255)

    draw.text((12, y_offset+24), "MENU",  font=font, fill=255)
    draw.text((52, y_offset+24), "FEED",  font=font, fill=255)
    draw.text((92, y_offset+24), "LVL: 01",  font=font, fill=255)
    disp.image(image)
    disp.display()

FOODS= {"canned_food" : ("canned_food" , 1, 2, 3),
        "apple" : ("apple", 2, 0, 5),
        "chicken" : ("chicken", 2, 2, 10),
        "mushroom" : ("pineamushroompple", 1, 0, 15),
        "pineapple": ("pineapple", 4, 5, 15),
        "steak" : ("steak", 5, 2, 15),
        "lollipop" : ("lollipop", 0, 1, 30),
        "pizza" : ("pizza", 5, 3, 15),
        "taco" : ("taco", 5, 5, 15)
}

def feedPage(foodItem, foodDict):
    disp.clear()
    foodQuant = foodDict[foodItem]
    image = Image.open(PATH + '/food/' + foodItem + '.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('L')
    image = ImageOps.invert(image)
    image=image.convert('1')
    draw = ImageDraw.Draw(image)

    if int(time.time() * 2) % 12 < 6:
        draw.text((10, y_offset+26), displayString(foodItem),  font=font, fill=255)
        draw.text((80, y_offset+26), displayString("x"+str(foodQuant)),  font=font, fill=255)
        
    else:
        draw.text((8, y_offset+26), displayString("HPY:" + str(FOODS[foodItem][1])),  font=font, fill=255)
        draw.text((50, y_offset+26), displayString("FD:" + str(FOODS[foodItem][2])),  font=font, fill=255)
        draw.text((94, y_offset+26), displayString("EXP:" + str(FOODS[foodItem][2])),  font=font, fill=255)
    # print(foodItem)
    # print(foodQuant)
    # print(FOODS[foodItem][1])
    # print(FOODS[foodItem][2])
    # print(FOODS[foodItem][3])

    disp.image(image)
    disp.display()

def friendsPage(friends):
    showFriend = ["No Friends Yet",""]
    friendsLength = len(friends)

    for i in range(friendsLength):
        showFriend[i] = friends[i]
    disp.clear()
    
    image = Image.open(PATH + "/menu/blank.png").resize((disp.width, disp.height), Image.ANTIALIAS).convert('L')
    image = ImageOps.invert(image)
    image=image.convert('1')
    draw = ImageDraw.Draw(image)

    draw.text((12, y_offset+4), displayString(showFriend[0]),  font=font, fill=255)
    draw.text((12, y_offset+14), displayString(showFriend[1]),  font=font, fill=255)
    draw.text((12, y_offset+24), "B A C K",  font=font, fill=255)
    disp.image(image)
    disp.display()

def taskPage(Tasks):
    # 128 x 64 pixel display
    showTasks = ["",""]
    for i in range(2):
        showTasks[i] = Tasks[i]
    disp.clear()
    
    image = Image.open(PATH + "/menu/blank.png").resize((disp.width, disp.height), Image.ANTIALIAS).convert('L')
    image = ImageOps.invert(image)
    image=image.convert('1')
    draw = ImageDraw.Draw(image)

    draw.text((12, y_offset+4), displayString(showTasks[0]),  font=font, fill=255)
    draw.text((12, y_offset+14), displayString(showTasks[1]),  font=font, fill=255)
    draw.text((12, y_offset+24), "B A C K",  font=font, fill=255)
    disp.image(image)
    disp.display()

def menuPage(press_idx):
    disp.clear()
    
    image = Image.open(PATH + "/menu/blank.png").resize((disp.width, disp.height), Image.ANTIALIAS).convert('L')
    image = ImageOps.invert(image)
    image=image.convert('1')
    draw = ImageDraw.Draw(image)

    if(press_idx == 1):
        draw.line((12, y_offset+13, 72, y_offset+13), fill=255)
    elif(press_idx == 2):
        draw.line((12, y_offset+23, 72, y_offset+23), fill=255)
    elif(press_idx == 3):
        draw.line((12, y_offset+33, 72, y_offset+33), fill=255)

    draw.text((12, y_offset+4), "D A I L Y    T A S K S",  font=font, fill=255)
    draw.text((12, y_offset+14), "F R I E N D S",  font=font, fill=255)
    draw.text((12, y_offset+24), "B A C K",  font=font, fill=255)
    disp.image(image)
    disp.display()

def displayString(text):
    text = text.replace(" ","  ")
    text = " ".join(text)
    return text




# Set buttonPin to INPUT mode with pull-up resistor
def setup():
    GPIO.setmode(GPIO.BCM)     
    GPIO.setup(leftArrowPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    
    GPIO.setup(middleSelectPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(rightArrowPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# If button pressed return 1, else return 0
def detect():
    leftArrowState = middleSelectState = rightArrowState = 0
    
    if GPIO.input(leftArrowPin) == GPIO.LOW:
        startTime = time.time() * 1000
        while GPIO.input(leftArrowPin) == GPIO.LOW:
            time.sleep(.01)
            # print("left")
        leftArrowState = 1
    if GPIO.input(middleSelectPin) == GPIO.LOW:
        startTime = time.time() * 1000
        while GPIO.input(middleSelectPin) == GPIO.LOW:
            time.sleep(.01)
            # print("select")
        middleSelectState = 1
    if GPIO.input(rightArrowPin) == GPIO.LOW:
        startTime = time.time() * 1000
        while GPIO.input(rightArrowPin) == GPIO.LOW:
            time.sleep(.01)
            # print("right")
        rightArrowState = 1

    return (leftArrowState, middleSelectState, rightArrowState)

def connecting():
    # Default font
    font = ImageFont.truetype(PATH + "/arial.ttf", 15)
    disp.clear()

    image = Image.open("/home/pi/Desktop/ECE140B-PepPets/PepPets/Hardware/OLED/connect/connecting.png").resize((disp.width, disp.height), Image.ANTIALIAS).convert('L')
    image = ImageOps.invert(image)
    image=image.convert('1')
    draw = ImageDraw.Draw(image)

    draw.text((28, 7), "Connecting",  font=font, fill=255)
    disp.image(image)
    disp.display()

    font = ImageFont.truetype(PATH + "/arial.ttf", 8)

def new_friend():
    # Default font
    font = ImageFont.truetype(PATH + "/arial.ttf", 12)
    disp.clear()

    image = Image.open("/home/pi/Desktop/ECE140B-PepPets/PepPets/Hardware/OLED/connect/connecting.png").resize((disp.width, disp.height), Image.ANTIALIAS).convert('L')
    image = ImageOps.invert(image)
    image=image.convert('1')
    draw = ImageDraw.Draw(image)

    draw.text((40, 2), "You have",  font=font, fill=255)
    draw.text((34, 11), "connected a",  font=font, fill=255)
    draw.text((52, 21), "friend",  font=font, fill=255)
    disp.image(image)
    disp.display()

    font = ImageFont.truetype(PATH + "/arial.ttf", 8)

setup()
press_idx = 1
activepage = "facepage"
activeoption = "menu"

# while True:

#     buttonPress = detect()
#     if activepage == "facepage":
#         if activeoption == "menu":
#             press_idx = 1
#         if activeoption == "feed":
#             press_idx = 2
#         faceIdle(press_idx,"/menu/madge.png")

#         if buttonPress[0] and activeoption == "feed":
#             activeoption = "menu"
#         elif buttonPress[2] and activeoption == "menu":
#             activeoption = "feed"
#         if buttonPress[1]:
#             if activeoption == "menu":
#                 activepage = "menupage"
#                 activeoption = "task"
#             elif activeoption == "feed":
#                 activepage = "foodpage"
#                 activeoption = 0
            
        

#     elif activepage == "menupage":
#         if activeoption == "task":
#             press_idx = 1
#         if activeoption == "friends":
#             press_idx = 2
#         if activeoption == "back":
#             press_idx = 3
#         menuPage(press_idx)

#         # cursor on task
#         if activeoption == "task":
#             if buttonPress[1]:
#                 activepage = "taskpage"
#                 activeoption = "backtomenu"
                
#             elif buttonPress[2]:
#                 activeoption = "friends"
                

#         # cursor on friends
#         elif activeoption == "friends":
#             if buttonPress[0]:
#                 activeoption = "task"
                
#             elif buttonPress[1]:
#                 activepage = "friendspage"
#                 activeoption = "backtomenu"
                
#             elif buttonPress[2]:
#                 activeoption = "back"
                

#         # cursor on back
#         elif activeoption == "back":
#             if buttonPress[0]:
#                 activeoption = "friends"
#             elif buttonPress[1]:
#                 activepage = "facepage"
#                 activeoption = "menu"
                

#     elif activepage == "taskpage":
#         taskPage()

#         if buttonPress[1]:
#             activepage = "menupage"
#             activeoption = "task"
            

#     elif activepage == "friendspage":
#         # friendspage()

#         if buttonPress[1]:
#             activepage = "menupage"
#             activeoption = "task"

#     # default cursor on chicken
#     elif activepage == "foodpage":
#         feedPage()
#         listoffoods = list(foods.keys())
#         lastfood = len(listoffoods) - 1

#         if activeoption == 0:
#             if buttonPress[0]:
#                 activepage = "facepage"
#                 activeoption = "menu"
#             elif buttonPress[1]:
#                 print("feeding " + listoffoods[activeoption])
#                 # feed(listoffoods[activeoption])
#             elif buttonPress[2]:
#                 activeoption += 1

#         elif activeoption == lastfood:
#             if buttonPress[0]:
#                 activeoption -= 1
#             elif buttonPress[1]:
#                 print("feeding " + listoffoods[activeoption])
#                 # feed(listoffoods[activeoption])
#             elif buttonPress[2]:
#                 activepage = "facepage"
#                 activeoption = "menu"

#         else:
#             if buttonPress[0]:
#                 activeoption -= 1
#             elif buttonPress[1]:
#                 print("feeding " + listoffoods[activeoption])
#                 # feed(listoffoods[activeoption])
#             elif buttonPress[2]:
#                 activeoption += 1

#     # print(activepage)
#     # print(activeoption)
#     # print("-----------------------------")
#     time.sleep(.01)
