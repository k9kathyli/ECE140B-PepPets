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

def feedPage():
    disp.clear()

    image = Image.open(PATH + '/menu/happy.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('L')
    image = ImageOps.invert(image)
    image=image.convert('1')
    print("here")
    disp.image(image)
    disp.display()
    # time.sleep(2)

    # image = Image.open('PepPets/Hardware/OLED/menu/happy.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('L')
    # image = ImageOps.invert(image)
    # image=image.convert('1')

    # disp.display()

# Set buttonPin to INPUT mode with pull-up resistor
def setup():
    GPIO.setmode(GPIO.BCM)     
    GPIO.setup(leftArrowPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    
    GPIO.setup(middleSelectPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(rightArrowPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# If button pressed return 1, else return 0
def detect():
    leftArrowState = 1 if GPIO.input(leftArrowPin) == GPIO.LOW else 0
    middleSelectState = 1 if GPIO.input(middleSelectPin) == GPIO.LOW else 0
    rightArrowState = 1 if GPIO.input(rightArrowPin) == GPIO.LOW else 0

    return (leftArrowState, middleSelectState, rightArrowState)

setup()
press_idx = 1
# activepage = "facepage"
# activeoption = "menu"
# foods = {"Chicken": 9999, "steak": 2, "sauce": 45, "stuff": 7}

# while True:
    
#     if activepage == "facepage":
#         if activeoption == "menu":
#             press_idx = 1
#         if activeoption == "feed":
#             press_idx = 2
#         faceIdle(press_idx,"/menu/madge.png")

#         if detect()[0] and activeoption == "feed":
#             activeoption = "menu"
#         elif detect()[2] and activeoption == "menu":
#             activeoption = "feed"
#         if detect()[1]:
#             if activeoption == "menu":
#                 activepage = "menupage"
#                 activeoption = "task"
#             elif activeoption == "feed":
#                 activepage = "foodpage"
#                 activeoption = 0
            
        

#     elif activepage == "menupage":
#         # menupage()

#         # cursor on task
#         if activeoption == "task":
#             if detect()[1]:
#                 activepage = "taskpage"
#                 activeoption = "backtomenu"
                
#             elif detect()[2]:
#                 activeoption = "friends"
                

#         # cursor on friends
#         elif activeoption == "friends":
#             if detect()[0]:
#                 activeoption = "task"
                
#             elif detect()[1]:
#                 activepage = "friendspage"
#                 activeoption = "backtomenu"
                
#             elif detect()[2]:
#                 activeoption = "back"
                

#         # cursor on back
#         elif activeoption == "back":
#             if detect()[0]:
#                 activeoption = "friends"
#             elif detect()[1]:
#                 activepage = "facepage"
#                 activeoption = "menu"
                

#     elif activepage == "taskpage":
#         # taskpage()

#         if detect()[1]:
#             activepage = "menupage"
#             activeoption = "task"
            

#     elif activepage == "friendspage":
#         # friendspage()

#         if detect()[1]:
#             activepage = "menupage"
#             activeoption = "task"

#     # default cursor on chicken
#     elif activepage == "foodpage":
#         feedPage()
#         listoffoods = list(foods.keys())
#         lastfood = len(listoffoods) - 1

#         if activeoption == 0:
#             if detect()[0]:
#                 activepage = "facepage"
#                 activeoption = "menu"
#             elif detect()[1]:
#                 print("feeding " + listoffoods[activeoption])
#                 # feed(listoffoods[activeoption])
#             elif detect()[2]:
#                 activeoption += 1

#         elif activeoption == lastfood:
#             if detect()[0]:
#                 activeoption -= 1
#             elif detect()[1]:
#                 print("feeding " + listoffoods[activeoption])
#                 # feed(listoffoods[activeoption])
#             elif detect()[2]:
#                 activepage = "facepage"
#                 activeoption = "menu"

#         else:
#             if detect()[0]:
#                 activeoption -= 1
#             elif detect()[1]:
#                 print("feeding " + listoffoods[activeoption])
#                 # feed(listoffoods[activeoption])
#             elif detect()[2]:
#                 activeoption += 1




            




#     print(activepage)
#     print(activeoption)
#     print("-----------------------------")
#     time.sleep(1)
