#Libraries
import RPi.GPIO as GPIO
import time
import os
import random

waitTime = 0
positive = ('ProudOfYou.wav','TestudoSmile.wav','SouthernEngland.wav','GoodRubbage.wav','Socialism.wav')
negative = ('BelongsInTheTrash.wav','Planet\ Killer.wav','DestroyedThePlanet.wav','LiteralTrashCan.wav','Sea\ Turtle.wav','CoffeeCupsForTestudo.wav','Oblivion.wav','WoeIsMe.wav')
instrucs = ('Compost.wav','recycling.wav','Trash.wav')

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

#when is the beam broken
def beambroke():
    return GPIO.input(14)


if __name__ == '__main__':
    beamState = 1
    target = 1
    distArray = []
    try:
        while True: #loop for the whole system
           target += 1 #0 comp, 1 recyc, 2 trash
	   if target > 2:
		target = 0
           os.system('aplay ' + instrucs[target]) #play instructions 
	   distArray = [700, 700, 700]
	   while True: #loop to keep taking data
		distRaw = distance()
		distArray.append(distRaw)
		if len(distArray) > 3:
			del distArray[0]
		dist = 0
		for d in distArray: dist += d
		dist /= len(distArray)
		print("{} {}".format(distRaw, dist))
		prevState = beamState
                beamState = beambroke()
		print(beamState)
                if (dist > 100):
                    arrow = -1
                elif (dist > 50):
                    arrow = 1
                    break
                elif (dist > 10):	
                    arrow = 0
                    break
                if beamState == 0 and prevState == 0:
                    arrow = 2
                    break 
                time.sleep(0.1)
           if target == arrow:
                os.system('aplay ' + random.choice(positive))
           else:
                os.system('aplay ' + random.choice(negative))
	   time.sleep(0.5) #wait before asking again
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
