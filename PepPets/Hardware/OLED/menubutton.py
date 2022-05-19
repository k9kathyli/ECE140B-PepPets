import board
import busio
from PIL import Image, ImageOps, ImageDraw, ImageFont
import Adafruit_SSD1306
import subprocess
# Import sleep module
from time import sleep
import RPi.GPIO as GPIO

# buttons
leftArrow = 16
middleSelect = 20
rightArrow = 21

def setup():
    GPIO.setmode(GPIO.BCM)     
    GPIO.setup(leftArrow, GPIO.IN, pull_up_down=GPIO.PUD_UP)    
    GPIO.setup(middleSelect, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(rightArrow, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

setup()

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
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# face
def facePage():
    image = Image.open('PepPets/Hardware/OLED/menu/happy.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('L')
    image = ImageOps.invert(image)
    image=image.convert('1')
    draw = ImageDraw.Draw(image)
    draw.line((x+12, top+33, x+36, top+33), fill=255)
    draw.text((x+12, top+24), "MENU",  font=font, fill=255)
    draw.text((x+52, top+24), "FEED",  font=font, fill=255)
    draw.text((x+92, top+24), "LVL: 01",  font=font, fill=255)
    disp.image(image)
    disp.display()


# menu
menus = ["face", "menu", "closet", "friends"]
def menupage():
    currentPage = "face"
    while True:
        match currentPage:
            case "face":
                facePage()
                return
            case "menu":
                return
            case "closet":
                return
            case "friends":
                return
            case _:
                return


