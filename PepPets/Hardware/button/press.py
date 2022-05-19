import RPi.GPIO as GPIO
import time

leftArrow = 16
middleSelect = 20
rightArrow = 21

# Set buttonPin to INPUT mode with pull-up resistor
def setup():
    GPIO.setmode(GPIO.BCM)     
    GPIO.setup(leftArrow, GPIO.IN, pull_up_down=GPIO.PUD_UP)    
    GPIO.setup(middleSelect, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(rightArrow, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# If button pressed return 1, else return 0
def detect():
    leftArrowState = 1 if GPIO.input(leftArrow) == GPIO.LOW else 0
    middleSelectState = 1 if GPIO.input(middleSelect) == GPIO.LOW else 0
    rightArrowState = 1 if GPIO.input(rightArrow) == GPIO.LOW else 0

    return "Left Arrow: " + str(leftArrowState) + "     Middle Arrow: " + str(middleSelectState) + "     Right Arrow: " + str(rightArrowState)

# Loops detect(). give one second buffer
def loop():
    while(True):
        print(detect())
        time.sleep(.1)

# Program entrance       
if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press CTRL-C to end the program
        GPIO.cleanup()         # Release GPIO resources