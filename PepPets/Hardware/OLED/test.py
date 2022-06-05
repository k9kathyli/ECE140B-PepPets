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
font = ImageFont.truetype(PATH + "/arial.ttf", 9)

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
def faceIdle():
    disp.clear()

    image = Image.open("/home/pi/Desktop/ECE140B-PepPets/PepPets/Hardware/OLED/food/pizza.png").resize((disp.width, disp.height), Image.ANTIALIAS).convert('L')
    image = ImageOps.invert(image)
    image=image.convert('1')
    draw = ImageDraw.Draw(image)

    draw.text((10, y_offset+24), "Apple",  font=font, fill=255)
    draw.text((50, y_offset+24), "x100",  font=font, fill=255)
    draw.text((92, y_offset+24), "EXP: 01",  font=font, fill=255)
    disp.image(image)
    disp.display()

faceIdle()