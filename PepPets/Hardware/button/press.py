import RPi.GPIO as GPIO

leftArrowPin = 16
middleSelectPin = 20
rightArrowPin = 21

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