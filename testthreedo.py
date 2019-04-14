#Libraries
import RPi.GPIO as GPIO
import time
import os
import random

waitTime = 0
positive = ('ProudOfYou.wav','TestudoSmile.wav','SouthernEngland.wav','GoodRubbage.wav','Socialism.wav')
negative = ('BelongsInTheTrash.wav','Planet\ Killer.wav','DestroyedThePlanet.wav','LiteralTrashCan.wav','Sea\ Turtle.wav','CoffeeCupsForTestudo.wav','Oblivion.wav','WoeIsMe.wav')

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO_BEAM = 14

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_BEAM,GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

def beambroke():
    return GPIO.input(14)


if __name__ == '__main__':
    beamState = 1
    try:
        while True:
            while True:
                dist = distance()
		prevState = beamState
                beamState = beambroke()
                print(dist)
		print(beamState)
		print()
                if (dist > 100):
                    type = 'empty'
                elif (dist > 50):
                    type = 'recycle'
                    f = random.choice(positive)
                    os.system('aplay '+f) 
                    time.sleep(waitTime)
                    break
                elif (dist > 10):	
                    type = 'compost'
                    f = random.choice(positive)
                    os.system('aplay '+f) 
                    time.sleep(waitTime)
                    break
                if beamState == 0 and prevState == 0:
                    type = 'trash'
                    f = random.choice(negative)
                    os.system('aplay '+f) 
                    time.sleep(waitTime)
                    break 
                print(type)
                time.sleep(0.1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
