import board
import busio
from PIL import Image, ImageOps, ImageDraw, ImageFont
import Adafruit_SSD1306
import RPi.GPIO as GPIO
import time

leftArrowPin = 16
middleSelectPin = 20
rightArrowPin = 21

# Default font
font = ImageFont.truetype("PepPets/Hardware/OLED/arial.ttf", 8)

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
def faceIdle(press_idx):
    disp.clear()

    image = Image.open('PepPets/Hardware/OLED/menu/happy.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('L')
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

    image = Image.open('PepPets/Hardware/OLED/menu/madge.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('L')
    image = ImageOps.invert(image)
    image=image.convert('1')

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

while True:
    press_idx += 1 if detect()[0] == 1 or detect()[2] == 1 else 0
    faceIdle(press_idx)
    if(detect()[1] == 1):
        feedPage()
    time.sleep(0.1)
