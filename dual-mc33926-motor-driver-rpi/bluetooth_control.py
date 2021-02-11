""" Test script for using pygame to read dualshock 4 (ds4) with ds4drv running as a daemon.

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

Axis0 = 0
Axis1 = 1
Axis2 = 2
Axis3 = 3
Axis4 = 4
Axis5 = 5
LStickHorz 	= Axis0
LStickVert 	= Axis1
LTrigg 		= Axis2
RStickHorz 	= Axis3
RStickVert 	= Axis4
RTrigg 		= Axis5

#create array to track button presses
button = {}

#initialize DS4 controller
screen = pygame.display.set_mode([50,50]) # make a 10x10 window
pygame.joystick.init() #find the joysticks
controller = pygame.joystick.Joystick(0)
controller.init()

for i in range(controller.get_numbuttons()):
    button[i] = False

if(controller.get_name()=='Wireless Controller'):
    print("DS4 connected")
else:
    print("Not a DS4")

def Scale_Speed(speed):
    speed + 1 # speed -(-1) lowest range of measurement
    range = 1 + 1 # 1-(-1) range of measurement
    speed = speed / range
    d_range = 480 + 480 # 480 -(-480) range of target
    speed = speed * d_range
    speed = speed - 480 # initialize to lowest point
    return speed

#init wiringpi
wiringpi.wiringPiSetupGpio()
pwm = 18
i = 0

for i in range(40):
    if i == 1 or i == 2 or i == 4 or i == 6 or i == 9 or i == 14 or i == 17 or i == 20 or i == 25 or i == 27:
        i = i + 1
        continue
    elif i == 28 or i == 30 or i == 34 or i == 39:
        i = i + 1
        continue
    else:
        wiringpi.pinMode(i, 1)
        wiringpi.digitalWrite(i, 0)
wiringpi.pinMode(pwm, 2)

print("Analog Inputs:")
#print("Button Inputs:")
while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            button[event.button] = True
        if event.type == pygame.JOYBUTTONUP:
            button[event.button] = False

    if button[BUTTON_TRIANGLE]:
        wiringpi.pinMode(pwm, 1)
        wiringpi.digitalWrite(pwm, 0)
        quit()
    print("reading axes")
    l_horz = controller.get_axis(0)
    l_vert = controller.get_axis(1)
    l_trig = controller.get_axis(2)
    r_horz = controller.get_axis(3)
    r_vert = controller.get_axis(4)
    r_trig = controller.get_axis(5)
    print("r trig: ", r_trig)
    print("axes read")

    if l_vert < 0:
        scaled_l = int(l_vert * -480)
    elif l_vert > 0:
        scaled_l = int(l_vert * 480)
    elif l_vert == 0:
        scaled_l = 0

    if r_vert < 0:
        scaled_r = int(r_vert * -480)
    elif r_vert > 0:
        scaled_r = int(r_vert * -480)
    elif r_vert == 0:
        scaled_r = 0

#    print("LV: ", round(l_vert,3), "LH: ", round(l_horz,3), "LT: ", round(l_trig,3), "RV: ", round(r_vert,3), "RH: ", round(r_horz,3), "RT: ", round(r_trig,3))
#    print("LV: ", round(l_vert,3), "LH: ", round(l_horz,3), "LT: ", round(l_trig,3), "RV: ", round(r_vert,3), "RH: ", round(r_horz,3), "RT: ", round(r_trig,3), "      ", end='\r')
#    print("A: ", button[BUTTON_CROSS], "B: ", button[BUTTON_CIRCLE], "X: ", button[BUTTON_SQUARE], "Y: ", button[BUTTON_TRIANGLE], "L1: ", button[BUTTON_L1], "L2: ", button[BUTTON_L2], "R1: ", button[BUTTON_R1], "R2: ", button[BUTTON_R2], "LS: ", button[BUTTON_LEFT_STICK], "RS: ", button[BUTTON_RIGHT_STICK], "Shr: ", button[BUTTON_SHARE], "Opt: ", button[BUTTON_OPTIONS], "PS: ", button[BUTTON_PS], "   ", end='\r')

    print("scaled r: ", scaled_r)
#    wiringpi.pwmWrite(pwm, int(scaled_r))

    sleep(1) #limit the frequency to 1Hz
