# Import oled libraries
import board
import busio
from PIL import Image, ImageOps, ImageDraw, ImageFont
import Adafruit_SSD1306
import subprocess
# Import sleep module
from time import sleep
import RPi.GPIO as GPIO

from progress_bar import *

bar1 = [4,17,27,22, 10]
bar2 = [9, 11, 5, 6, 13]
bar3 = [14, 15, 18, 23, 24]

initpins(bar1)
initpins(bar2)
initpins(bar3)
clear(bar1)
clear(bar2)
clear(bar3)
leftArrow = 16
middleSelect = 20
rightArrow = 21

# Set buttonPin to INPUT mode with pull-up resistor
def setup():
    GPIO.setmode(GPIO.BCM)     
    GPIO.setup(leftArrow, GPIO.IN, pull_up_down=GPIO.PUD_UP)    
    GPIO.setup(middleSelect, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(rightArrow, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

setup()
# If button pressed return 1, else return 0
def detect():
    leftArrowState = 1 if GPIO.input(leftArrow) == GPIO.LOW else 0
    middleSelectState = 1 if GPIO.input(middleSelect) == GPIO.LOW else 0
    rightArrowState = 1 if GPIO.input(rightArrow) == GPIO.LOW else 0

    return "Left Arrow: " + str(leftArrowState) + "     Middle Arrow: " + str(middleSelectState) + "     Right Arrow: " + str(rightArrowState)

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
# Create the SSD1306 OLED class.
# disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
RST = None 
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Clear display.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing, mode '1' for 1-bit color.
width = disp.width
height = disp.height
# image = Image.new("1", (width, height))
image = Image.open('PepPets/Hardware/OLED/menu/happy.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('L')
image = ImageOps.invert(image)
image=image.convert('1')
draw = ImageDraw.Draw(image)
# font = ImageFont.load("PepPets/Hardware/OLED/arial.pil")
font = ImageFont.truetype("PepPets/Hardware/OLED/arial.ttf", 8)
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

pro1 = 0
pro2 = 0
pro3 = 0
buttonpress = False

def detect(buttonpress):
    button1 = 0
    button2 = 0
    button3 = 0
    
    if GPIO.input(leftArrow) == GPIO.HIGH and buttonpress == False:
        start = time.time()*1000
        buttonpress = True
    
    elif GPIO.input(leftArrow) == GPIO.LOW and buttonpress == False and time.time()*1000 > 200:
        buttonpress = False
        button1 = 1
        
    if GPIO.input(middleSelect) == GPIO.HIGH and buttonpress == False:
        start = time.time()*1000
        buttonpress = True
    
    elif GPIO.input(middleSelect) == GPIO.LOW and buttonpress == False and time.time()*1000 > 200:
        buttonpress = False
        button2 = 1

    if GPIO.input(rightArrow) == GPIO.HIGH and buttonpress == False:
        start = time.time()*1000
        buttonpress = True
    
    elif GPIO.input(rightArrow) == GPIO.LOW and buttonpress == False and time.time()*1000 > 200:
        buttonpress = False
        button3 = 1

    inputreceive = (button1,button2,button3)
    return inputreceive

while True:

    # Find image in json
    # image = Image.open('PepPets/Hardware/OLED/menu/happy.png').resize((width, height), Image.ANTIALIAS).convert('L')
    # inv_image = ImageOps.invert(image)
    # inv_image=inv_image.convert('1')

    # Display image.
    #disp.image(inv_image)
    # disp.text('Skater greater alligator', 0, 10, 0)
    draw.rectangle((x+8, top+23, x+38, top+33), outline=255, fill=0)
    draw.rectangle((x+48, top+23, x+78, top+33), outline=255, fill=0)
    draw.rectangle((x+88, top+23, x+118, top+33), outline=255, fill=0)
    draw.text((x+12, top+24), "MENU",  font=font, fill=255)
    draw.text((x+52, top+24), "FEED",  font=font, fill=255)
    draw.text((x+92, top+24), "XP:  01",  font=font, fill=255)
    disp.image(image)
    disp.display()

    buttoninput = detect(buttonpress)
    pro1 += buttoninput[0]
    pro2 += buttoninput[1]
    pro3 += buttoninput[2]
    if pro1 > 10:
        pro1 -= 10
    if pro2 > 10:
        pro2 -= 10
    if pro3 > 10:
        pro3 -= 10

    progress(bar1,pro1)
    progress(bar2,pro2)
    progress(bar3,pro3)

    # sleep(.1)



