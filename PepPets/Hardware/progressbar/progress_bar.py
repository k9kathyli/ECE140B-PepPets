import RPi.GPIO as IO         # calling for header file which helps us use GPIO’s of PI
import time                             # calling for time to provide delays in program
IO.setwarnings(False)           # do not show any warnings
x=1                
IO.setmode (IO.BCM)        # programming the GPIO by BCM pin numbers. (like PIN29 as‘GPIO5’)
IO.setup(4,IO.OUT)            # initialize GPIO Pins as an output.
IO.setup(5,IO.OUT)
IO.setup(6,IO.OUT)

interval = .01

bar1 = [4,17,27,22, 10]
bar2 = [9, 11, 5, 6, 13]
bar3 = [14, 15, 18, 23, 24]

def initpins(pins):
    for x in pins:
        IO.setup(x,IO.OUT)

def clear(bar):
    for y in range(8):            # loop for counting up 8 times
        IO.output(bar[0],0)            # clear the DATA pin, to send 0
        time.sleep(interval)            # wait for 100ms
        IO.output(bar[1],1)            # pull CLOCK pin high
        time.sleep(interval)
        IO.output(bar[1],0)            # pull CLOCK pin down, to send a rising edge

    IO.output(bar[2],1)            # pull the SHIFT pin high to put the 8 bit data out parallel
 
    IO.output(bar[3],0)
    IO.output(bar[4],0)

    time.sleep(interval)
    IO.output(bar[2],0)

def allon(bar):
    for y in range(8):            # loop for counting up 8 times
        IO.output(bar[0],1)            # clear the DATA pin, to send 0
        time.sleep(interval)            # wait for 100ms
        IO.output(bar[1],1)            # pull CLOCK pin high
        time.sleep(interval)
        IO.output(bar[1],0)            # pull CLOCK pin down, to send a rising edge

    IO.output(bar[2],1)            # pull the SHIFT pin high to put the 8 bit data out parallel

    IO.output(bar[3],1)
    IO.output(bar[4],1)

    time.sleep(interval)
    IO.output(bar[2],0)

# bar - array of the pins for the LED display
# progress - number from 1 - 10 for number of leds
def progress(bar, progress):
    if progress <= 8:
        # Shift off data
        for y in range(8-progress):
            IO.output(bar[0],0)            # clear the DATA pin, to send 0
            time.sleep(interval)            # wait for 100ms
            IO.output(bar[1],1)            # pull CLOCK pin high
            time.sleep(interval)
            IO.output(bar[1],0)
        
        # Shift on data
        for y in range(progress):
            IO.output(bar[0],1)            # clear the DATA pin, to send 0
            time.sleep(interval)            # wait for 100ms
            IO.output(bar[1],1)            # pull CLOCK pin high
            time.sleep(interval)
            IO.output(bar[1],0)
            
        
        IO.output(bar[2],1)            # pull the SHIFT pin high to put the 8 bit data out parallel
        # Off led 9,10
        IO.output(bar[3],0)
        IO.output(bar[4],0)

        time.sleep(interval)
        IO.output(bar[2],0)
    else:
        

        for y in range(8):            # loop for counting up 8 times
            IO.output(bar[0],1)            # clear the DATA pin, to send 0
            time.sleep(interval)            # wait for 100ms
            IO.output(bar[1],1)            # pull CLOCK pin high
            time.sleep(interval)
            IO.output(bar[1],0)            # pull CLOCK pin down, to send a rising edge

        if progress == 9:
            IO.output(bar[3],1)
            IO.output(bar[4],0)
        elif progress == 10:
            IO.output(bar[3],1)
            IO.output(bar[4],1)

        IO.output(bar[2],1)            # pull the SHIFT pin high to put the 8 bit data out parallel
        time.sleep(interval)
        IO.output(bar[2],0)

            
initpins(bar1)
initpins(bar2)
initpins(bar3)

progress(bar1, 9)
for y in range(11):
    progress(bar1, y)
    progress(bar2, y)
    progress(bar3, y)
    print(y)
    time.sleep(.5)
for y in range(10,-1,-1):
    progress(bar1, y)
    progress(bar2, y)
    progress(bar3, y)
    print(y)
    time.sleep(.5)

