from dual_mc33926_rpi import motors, MAX_SPEED
import time

wait_time = 1 # time is seconds
print("wait time is ", wait_time, "seconds\n")
change = input("would you like to change the wait time? Y/n\n")
if change == 'Y' or change == 'y':
	wait_time = int(input("Enter time to wait before speed change in seconds.fracs_of_seconds\n"))

print("Motor 1 forward test")
speed = 0
while speed < MAX_SPEED + 1:
	motors.motor1.setSpeed(speed)
#	time.sleep(wait_time)
	speed = speed + 1

cont = "n"
cont = input("cont? Y/n\n")

if cont == 'N' or cont == 'n':
	quit()

print("Motor 1 backward test")
speed = 0
while speed > -MAX_SPEED - 1:
	motors.motor1.setSpeed(speed)
#	time.sleep(wait_time)
	speed = speed + 1

cont = "n"
cont = input("cont? Y/n\n")

if cont == 'N' or cont == 'n':
	quit()

print("Motor 2 forward test")
speed = 0
while speed < MAX_SPEED + 1:
	motors.motor2.setSpeed(speed)
#	time.sleep(wait_time)
	speed = speed + 1

cont = "n"
cont = input("cont? Y/n\n")

if cont == 'N' or cont == 'n':
	quit()

print("Motor 2 backward test")
speed = 0
while speed > -MAX_SPEED - 1:
	motors.motor2.setSpeed(speed)
#	time.sleep(wait_time)
	speed = speed + 1
