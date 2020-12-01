""" Test script for using pygame to read dualshock 4 (ds4) with ds4drv running as 
a daemon.

DS4 Controller axis maps:
Axis0: Left stick l-r (-1 left, 1 right)
Axis1: Left stick u-d (-1 up, ` 1 down)
Axis2: Left Trigger (-1 unpressed, 1 completely pressed)
Axis3: Right stick l-r (-1 left, 1 right)
Axis4: Right stick u-d (-1 up, 1 down)
Axis5: Right trigger (-1 unpressed, 1 completely pressed)
"""
import pygame
import wiringpi
from time import sleep

#Defines for button numbers
BUTTON_SQUARE       = 3
BUTTON_CROSS        = 0
BUTTON_CIRCLE       = 1
BUTTON_TRIANGLE     = 2
BUTTON_L1           = 4
BUTTON_R1           = 5
BUTTON_L2           = 6
BUTTON_R2           = 7
BUTTON_SHARE        = 8
BUTTON_OPTIONS      = 9
BUTTON_LEFT_STICK   = 11
BUTTON_RIGHT_STICK  = 12
BUTTON_PS           = 10
BUTTON_BUTTON_PAD   = 13

#create array to track button presses
button = {}

#initialize DS4 controller
screen = pygame.display.set_mode([100,100]) # make a 10x10 window
pygame.joystick.init() #find the joysticks
controller = pygame.joystick.Joystick(0)
controller.init()

for i in range(controller.get_numbuttons()):
    button[i] = False

if(controller.get_name()=='Wireless Controller'):
    print("DS4 connected")
else:
    print("Not a DS4")

Motor1PWM 	= 1 			# gpio pin 12 = wiringpi no 1 (BCM 18)
Motor1AIN1 	= 4 			# gpio pin 16 = wiringpi no. 4 (BCM 23)
Motor1AIN2 	= 5 			# gpio pin 18 = wiringpi no. 5 (BCM 24)
MotorStandby 	= 6 			# gpio pin 22 = wiringpi no. 6 (BCM 25)
Motor2PWM 	= 23 			# gpio pin 33 = wiringpi no. 23 (BCM 13)
Motor2BIN1 	= 21 			# gpio pin 29 = wiringpi no. 21 (BCM 5)
Motor2BIN2 	= 22 			# gpio pin 31 = wiringpi no. 22 (BCM 6)
 
# Initialize PWM output
wiringpi.wiringPiSetup()
wiringpi.pinMode(Motor1PWM,         2) 	# PWM mode
wiringpi.pinMode(Motor1AIN1,   	    1) 	# Digital out mode
wiringpi.pinMode(Motor1AIN2,   	    1) 	# Digital out mode
wiringpi.pinMode(MotorStandby, 	    1) 	# Ditial out mode
 
wiringpi.pinMode(Motor2PWM,    	    2)	# PWM mode
wiringpi.pinMode(Motor2BIN1,        1) 	# Digital out mode
wiringpi.pinMode(Motor2BIN2,        1) 	# Digital out mode
 
wiringpi.pwmWrite(Motor1PWM,        0)	# OFF
wiringpi.pwmWrite(Motor2PWM,        0)  # OFF
wiringpi.digitalWrite(Motor1AIN1,   1) 	#forward mode
wiringpi.digitalWrite(Motor1AIN2,   0) 	#forward mode
wiringpi.digitalWrite(Motor2BIN1,   1)
wiringpi.digitalWrite(Motor2BIN2,   0)
wiringpi.digitalWrite(MotorStandby, 1) 	#enabled
 
# Set Motor Speed
def motorspeed(speed1, speed2):
    wiringpi.pwmWrite(Motor1PWM, speed1) #motorspeed from -480 to 480
    wiringpi.pwmWrite(Motor2PWM, speed2) 

def Scale_Speed(speed):
    speed + 1 # speed -(-1) lowest range of measurement
    range = 1 + 1 # 1-(-1) range of measurement
    speed = speed / range
    d_range = 480 + 480 # 480 -(-480) range of target
    speed = speed * d_range
    speed = speed - 480 # initialize to lowest point
    return speed

#print("Analog Inputs:\n")
print("Button Inputs:\n")
while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            button[event.button] = True
        if event.type == pygame.JOYBUTTONUP:
            button[event.button] = False

    l_horz = controller.get_axis(0)
    l_vert = controller.get_axis(1)
    l_trig = controller.get_axis(2)
    r_horz = controller.get_axis(3)
    r_vert = controller.get_axis(4)
    r_trig = controller.get_axis(5)

    print("                                                                                                                                ", end='\r')
#    print("LV: ", round(l_vert,3), "LH: ", round(l_horz,3), "LT: ", round(l_trig,3), "RV: ", round(r_vert,3), "RH: ", round(r_horz,3), "RT: ", round(r_trig,3), end='\r')

    print("A: ", button[BUTTON_CROSS], "B: ", button[BUTTON_CIRCLE], "X: ", button[BUTTON_SQUARE], "Y: ", button[BUTTON_TRIANGLE], "L1: ", button[BUTTON_L1], "L2: ", button[BUTTON_L2], "R1: ", button[BUTTON_R1], "R2: ", button[BUTTON_R2], "LS: ", button[BUTTON_LEFT_STICK], "RS: ", button[BUTTON_RIGHT_STICK], "Shr: ", button[BUTTON_SHARE], "Opt: ", button[BUTTON_OPTIONS], "PS: ", button[BUTTON_PS], "       ", end='\r')

    speed = Scale_Speed(l_vert)

    speed1 = (speed)
    speed2 = speed1
    motorspeed(int(speed1),int(speed2))
    sleep(0.07) #limit the frequency to 50Hz


"""
DS4 Controller axis maps:
Axis0: Left stick l-r (-1 left, 1 right)
Axis1: Left stick u-d (-1 up, ` 1 down)
Axis2: Left Trigger (-1 unpressed, 1 completely pressed)
Axis3: Right stick l-r (-1 left, 1 right)
Axis4: Right stick u-d (-1 up, 1 down)
Axis5: Right trigger (-1 unpressed, 1 completely pressed)
"""
