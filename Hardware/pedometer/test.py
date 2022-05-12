# Import oled libraries
import board
import busio
from PIL import Image,ImageFont
from adafruit_display_text import label
import adafruit_ssd1306

# Import sleep module
from time import sleep

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

while True:
	disp.text("hello world", 50, 25, 1)
	disp.show()