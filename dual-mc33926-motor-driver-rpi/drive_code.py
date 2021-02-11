from dual_mc33926_rpi import motors, MAX_SPEED
import pygame
import wiringpi

"""
DS4 Controller axis maps:
Axis0: Left stick l-r (-1 left, 1 right)
Axis1: Left stick u-d (-1 up, ` 1 down)
Axis2: Left Trigger (-1 unpressed, 1 completely pressed)
Axis3: Right stick l-r (-1 left, 1 right)
Axis4: Right stick u-d (-1 up, 1 down)
Axis5: Right trigger (-1 unpressed, 1 completely pressed)
"""

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

#Defines for analog inputs
LStickHorz 	= 0
LStickVert 	= 1
LTrigg 		= 2
RStickHorz 	= 3
RStickVert 	= 4
RTrigg 		= 5

def Init_Controller():
    screen = pygame.display.set_mode([50,50])
    pygame.joystick.init()  # find the joysticks
    controller = pygame.joystick.Joystick(0)
    controller.init()
    assert controller.get_init()
#    print(controller.get_numbuttons())
    #print(controller)
    return controller


def Init_Drive_ESC():
    global l_drive
    l_drive = 0
    global r_drive
    r_drive = 0
    wiringpi.wiringPiSetup()
    global Motor1PWM
    Motor1PWM = 1     # gpio pin 12 = wiringpi no 1   (BCM 18)
    global Motor1AIN1
    Motor1AIN1 = 4     # gpio pin 16 = wiringpi no. 4  (BCM 23)
    global Motor1AIN2
    Motor1AIN2 = 5     # gpio pin 18 = wiringpi no. 5  (BCM 24)
    global MotorStandby
    MotorStandby = 6     # gpio pin 22 = wiringpi no. 6  (BCM 25)
    global  Motor2PWM
    Motor2PWM = 23    # gpio pin 33 = wiringpi no. 23 (BCM 13)
    global Motor2AIN1
    Motor2AIN1 = 21    # gpio pin 29 = wiringpi no. 21 (BCM 5)
    global Motor2AIN2
    Motor2AIN2 = 22    # gpio pin 31 = wiringpi no. 22 (BCM 6)

    wiringpi.pinMode(Motor1PWM,         2) 	# PWM mode
    wiringpi.pinMode(Motor1AIN1,   	    1) 	# Digital out mode
    wiringpi.pinMode(Motor1AIN2,   	    1) 	# Digital out mode
    # wiringpi.pinMode(MotorStandby, 	    1) 	# Ditial out mode
    wiringpi.pinMode(Motor2PWM,    	    2)  # PWM mode
    wiringpi.pinMode(Motor2AIN1,        1) 	# Digital out mode
    wiringpi.pinMode(Motor2AIN2,        1) 	# Digital out mode


def Normalize(minimum, maximum, value):
    num = value - minimum
    den = maximum - minimum
    return num / den


def Get_Trigg_Vals(controller):
    LEFT_Trigg = -controller.get_axis(2)
    RIGHT_Trigg = -controller.get_axis(5)
#    print("Leftdrive: ", LEFT_Trigg, "   Rightdrive: ", RIGHT_Trigg, end='\r')
    return LEFT_Trigg, RIGHT_Trigg

def Get_Stick_Vals(controller):
    Left_Vert = -controller.get_axis(LStickVert)
    Left_Horz = -controller.get_axis(LStickHorz)
    Right_Vert = -controller.get_axis(RStickVert)
    Right_Horz = -controller.get_axis(RStickHorz)
#    print("LVert: ", Left_Vert, "    LHorz: ", Left_Horz, "    RVert: ", Right_Vert, "    RHorz: ", Right_Horz, "      ", end='\r')
    return Left_Vert, Left_Horz, Right_Vert, Right_Horz

def Send_Drive_Commands(cont):
    for event in pygame.event.get():
        button = True
        #if event.type == pygame.JOYBUTTONDOWN:
        #    button = True
        #if event.type == pygame.JOYBUTTONUP:
        #    button = False
     
    ltrigg, rtrigg = Get_Trigg_Vals(cont)        
    #l_drive = ltrigg
    #r_drive = rtrigg
    #l_drive, r_drive = Get_Trigg_Vals(cont)
    lvert, lhorz, rvert, rhorz = Get_Stick_Vals(cont)
    print("LTrig: ", round(ltrigg,2), "    RTrig: ", round(rtrigg,2), "    LVert: ", round(lvert,2), "    LHorz: ", round(lhorz,2), "    RVert: ", round(rvert,2), "    RHorz: ", round(rhorz,2), "          ", end='\r')
#    print("Leftstick: ", l_drive, "   Rightstick: ", r_drive, "              ", end='\r')
    if l_drive < 0:
        scaled_l = l_drive * -480
        wiringpi.pwmWrite(Motor1PWM, scaled_l)
        wiringpi.digitalWrite(Motor1AIN1, 1)
        wiringpi.digitalWrite(Motor1AIN2, 0)
    elif l_drive > 0:
        scaled_l = l_drive * 480
        wiringpi.pwmWrite(Motor1PWM, scaled_l)
        wiringpi.digitalWrite(Motor1AIN1, 1)
        wiringpi.digitalWrite(Motor1AIN2, 0)
    elif l_drive == 0:
        scaled_l = 0
        wiringpi.pwmWrite(Motor1PWM, scaled_l)
        wiringpi.digitalWrite(Motor1AIN1, 1)
        wiringpi.digitalWrite(Motor1AIN2, 0)

    if r_drive < 0:
        scaled_r = r_drive * -480
        wiringpi.pwmWrite(Motor2PWM, scaled_r)
        wiringpi.digitalWrite(Motor2AIN1, 0)
        wiringpi.digitalWrite(Motor2AIN2, 1)
    elif r_drive > 0:
        scaled_r = r_stick * 480
        wiringpi.pwmWrite(Motor2PWM, scaled_r)
        wiringpi.digitalWrite(Motor2AIN1, 0)
        wiringpi.digitalWrite(Motor2AIN2, 1)
    elif r_drive == 0:
        scaled_r = 0
        wiringpi.pwmWrite(Motor2PWM, scaled_r)
        wiringpi.digitalWrite(Motor2AIN1, 0)
        wiringpi.digitalWrite(Motor2AIN2, 1)

    wiringpi.digitalWrite(MotorStandby, 0)

print("Running")
cont = Init_Controller()
Init_Drive_ESC()
while True:
#Get_Stick_Vals(cont)
    Send_Drive_Commands(cont)
