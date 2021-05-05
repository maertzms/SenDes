from dual_mc33926_rpi import motors
import time
import pygame
import pigpio
import wiringpi
import sys

MAXSPEED = 100
weapon_pin = 20
weapon_freq = 500
pi1 = pigpio.pi()
pi1.set_PWM_frequency(weapon_pin,weapon_freq)
pi1.set_PWM_range(weapon_pin,MAXSPEED)

motors.enable()
motors.setSpeeds(0, 0)

tank = False
steering_power = 100 #0-100
speed = 100 #Range 0-100. ESC takes 0-480, picks up at 240. A speed of zero here gives 120 to be sure we can kill drives.

steering_power = steering_power/50
speed = (speed*2.4)+120
# Motor 1: gpio 12 pwm, gpio 24 input 1, gpio 22 input 2
# Motor 2: gpio 13 pwm, gpio 25 input 1, gpio 23 input 2
# GPIO 12 pin 32
# GPIO 24 pin 18
# GPIO 22 pin 15

motor1_dir_1 = 24
motor1_dir_2 = 22
motor1_pwm = 12

motor2_dir_1 = 25
motor2_dir_2 = 23
motor2_pwm = 13

# GPIO 13 pin, 33
# GPIO 25 pin 22
# GPIO 23 pin 16

# Initialize 5V and GND for weapon module
wiringpi.digitalWrite(2,0)
wiringpi.digitalWrite(3,1)
screen = pygame.display.set_mode([50, 50])
pygame.joystick.init()
controller = pygame.joystick.Joystick(0)
controller.init()
i = 0
while True:
    i = i + 1
    for event in pygame.event.get():
        if event.type==pygame.JOYBUTTONDOWN:
            button = True
        elif event.type==pygame.JOYBUTTONUP:
            button = False
            
    l_trig = controller.get_axis(2)
    r_trig = controller.get_axis(5)

    l_stick_vert = controller.get_axis(1)*-1
    r_stick_vert = controller.get_axis(4)*-1
    
    l_stick_horz = controller.get_axis(0)
    r_stick_horz = controller.get_axis(3)

   # if controller.get_button(0):
#        print("button 0")
#    elif controller.get_button(1):
#        print("button 1")
#    elif controller.get_button(2):
#        print("button 2")
#    elif controller.get_button(3):
#        print("button 3") 
#    elif controller.get_button(4):
#        print("button 4")
#    elif controller.get_button(5):
#        print("button 5")
#    elif controller.get_button(6):
#        print("button 6")
#    elif controller.get_button(7):
#        print("button 7")
##    elif controller.get_button(8):
#        print("button 8")
#    elif controller.get_button(9):
#        print("button 9")

    #Weapon Motor
    duty_cycle = int((r_trig*25)+75)
    pi1.set_PWM_dutycycle(weapon_pin,duty_cycle)
    
    #Switch Driving Modes, and Exit Code. Based on button pushes
    if controller.get_button(3):
        tank = True #Square Button to enter tank control mode
    if controller.get_button(1):
        tank = False #Circle Button to enter normal steering mode
    if controller.get_button(8):
        motors.setSpeeds(0,0)
        motors.disable()
        pi1.set_PWM_dutycycle(weapon_pin,50)
        sys.exit(1) #"SHARE" button to exit program.

        
    if tank: #tank steering selected
        l_speed = l_stick_vert * speed
        r_speed = r_stick_vert * speed

        print("L_SPD: ", int(l_speed), " L_DIR: ", l_dir, "  R_SPD: ", int(r_speed), " R_DIR: ", r_dir, end='\r')
        if l_speed > 0:
            l_dir = 0
        else:
            l_dir = 1

        if r_speed > 0: #this is switched since the right wheel
                        #is the other direction on the bot
                        #clockwise means backwards now.
            r_dir = 1
        else:
            r_dir = 0
    
        if l_dir == 1:
            wiringpi.digitalWrite(motor1_dir_1, 1)
            wiringpi.digitalWrite(motor1_dir_2, 0)
            wiringpi.pwmWrite(motor1_pwm, 120+int(abs(l_speed)))
        else:
            wiringpi.digitalWrite(motor1_dir_1, 0)
            wiringpi.digitalWrite(motor1_dir_2, 1)
            wiringpi.pwmWrite(motor1_pwm, 120+int(abs(l_speed)))

        if r_dir == 1:
            wiringpi.digitalWrite(motor2_dir_1, 1)
            wiringpi.digitalWrite(motor2_dir_2, 0)
            wiringpi.pwmWrite(motor2_pwm, 120+int(abs(r_speed)))
        else:
            wiringpi.digitalWrite(motor2_dir_1, 0)
            wiringpi.digitalWrite(motor2_dir_2, 1)
            wiringpi.pwmWrite(motor2_pwm, 120+int(abs(r_speed)))
    
    else: #steering mode selected
        
        #initialize speeds of both wheels just from gas stick
        l_speed = speed*r_stick_vert
        r_speed = speed*r_stick_vert
        #get steering value from steering stick
        steering = l_stick_horz
        
        #reduce speed in one wheel to steer according to steering value
        if steering < 0: #turn left
            l_speed = l_speed*(1-steering_power*abs(steering))
        else:  #turn right
            r_speed = r_speed*(1-steering_power*abs(steering))
            
        #get directions for wheels, forward or reverse. 1 is clockwise looking down at the motor shaft.
        if l_speed > 0:
            l_dir = 0
        else:
            l_dir = 1
        if r_speed > 0:
            r_dir = 1
        else:
            r_dir = 0


        if l_dir == 1:
            wiringpi.digitalWrite(motor1_dir_1, 1)
            wiringpi.digitalWrite(motor1_dir_2, 0)
            wiringpi.pwmWrite(motor1_pwm, 120+int(abs(l_speed)))
        else:
            wiringpi.digitalWrite(motor1_dir_1, 0)
            wiringpi.digitalWrite(motor1_dir_2, 1)
            wiringpi.pwmWrite(motor1_pwm, 120+int(abs(l_speed)))

        if r_dir == 1:
            wiringpi.digitalWrite(motor2_dir_1, 1)
            wiringpi.digitalWrite(motor2_dir_2, 0)
            wiringpi.pwmWrite(motor2_pwm, 120+int(abs(r_speed)))
        else:
            wiringpi.digitalWrite(motor2_dir_1, 0)
            wiringpi.digitalWrite(motor2_dir_2, 1)
            wiringpi.pwmWrite(motor2_pwm, 120+int(abs(r_speed)))
            
        print ("L_SPD: ", int(l_speed), " L_DIR: ", l_dir, "  R_SPD: ", int(r_speed), " R_DIR: ", r_dir, end='\r')
