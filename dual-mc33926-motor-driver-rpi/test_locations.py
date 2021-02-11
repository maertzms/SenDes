from math import fmod as mod
import wiringpi
from time import sleep

wiringpi.wiringPiSetupGpio() # sets up to use BCM GPIO raspberry pi gpio pin numbers
pwm = 18 # one webpage says only gpio 18 will work one uses it on multiple pins (neither are 18)
i = 0

for i in range(40):
        if i == 1 or i == 2 or i == 4 or i == 6 or i == 9 or i == 14 or i == 17:
                i = i + 1
                continue
        elif i == 20 or i == 25 or i == 27 or i == 28 or i == 30 or i == 34 or i == 39:
                i = i + 1
                continue
        else:
                wiringpi.pinMode(i, 1)
                wiringpi.digitalWrite(i, 0)

wiringpi.pinMode(pwm, 2) # set to pwm mode
i = 0

while i <= 1:
        print("Iteration: ", i, end='\r')
        i = i + 0.01
        wiringpi.pwmWrite(pwm, int(i * 1024))
        sleep(0.07) # limit to 50Hz
        if i >= 1:
                wiringpi.pinMode(pwm, 1)
                wiringpi.digitalWrite(pwm, 0)
                quit()
wiringpi.pinMode(pwm, 1)
wiringpi.digitalWrite(pwm, 0)
quit()
