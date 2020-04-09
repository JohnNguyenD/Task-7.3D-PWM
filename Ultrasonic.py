import RPi.GPIO as GPIO
import time

#GPIO Mode
GPIO.setmode(GPIO.BCM)

#set GPIO pins
GPIO_TRIGGER = 17
GPIO_ECHO = 4
led = 18

#set GPIO direction
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(led, GPIO.OUT)

#Set up pwm
pwm = GPIO.PWM(led, 100)
pwm.start(0)

def distance():

    #set Trigger to High
    GPIO.output(GPIO_TRIGGER, True)

    #set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    startTime = time.time()
    stopTime = time.time()

    #save startTime
    while GPIO.input(GPIO_ECHO) == 0:
        startTime = time.time()

    #save time of arrival:
    while GPIO.input(GPIO_ECHO) == 1:
        stopTime = time.time()

    #time difference between start and arrival
    TimeElapsed = stopTime - startTime
    #Multiply with the sonic speed (34300 cm/s)
    #and divide by 2, because there and back
    distance = (TimeElapsed *34300)/2

    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            if dist < 10:
                pwm.ChangeDutyCycle(100)
            elif dist > 10 and dist < 50:
                pwm.ChangeDutyCycle(50)
            elif dist >50:
                pwm.ChangeDutyCycle(20)
            else:
                pwm.ChangeDutyCycle(10)
    except KeyboardInterrupt:
        print("Measure stopped")
        GPIO.cleanup()
