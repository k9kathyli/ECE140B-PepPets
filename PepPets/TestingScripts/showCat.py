# Import oled libraries
import board
import busio
from PIL import Image, ImageOps
import adafruit_ssd1306

# Import sleep module
from time import sleep

# Import json reader
import json

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
# Create the SSD1306 OLED class.
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing, mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Open json
with open('PepPets/Hardware/OLED/emote.json') as json_file:
    json_data = json.load(json_file)

index = 0
while True:
    # Find image in json
    image = Image.open('PepPets/Hardware/OLED/' + json_data[index % len(json_data)]['path']).resize((width, height), Image.ANTIALIAS).convert('L')
    inv_image = ImageOps.invert(image)
    inv_image=inv_image.convert('1')

    # Display image.
    disp.image(inv_image)
    disp.show()
    sleep(1)

    print(json_data[index % len(json_data)]['emote'])
    index += 1


