# Import oled libraries
import board
import busio
from PIL import Image, ImageOps, ImageDraw, ImageFont
import Adafruit_SSD1306
import subprocess
# Import sleep module
from time import sleep

# Import json reader
import json

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
font = ImageFont.load_default()
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

while True:
    # Find image in json
    # image = Image.open('PepPets/Hardware/OLED/menu/happy.png').resize((width, height), Image.ANTIALIAS).convert('L')
    # inv_image = ImageOps.invert(image)
    # inv_image=inv_image.convert('1')

    # Display image.
    #disp.image(inv_image)
    # disp.text('Skater greater alligator', 0, 10, 0)
    draw.text((x, top+24), "Skater greater alligator",  font=font, fill=255)
    disp.image(image)
    disp.display()
    sleep(1)



