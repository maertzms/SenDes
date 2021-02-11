from dual_mc33926_rpi import motors
import time
import pygame

motors.enable()
motors.setSpeeds(0, 0)

# Motor 1: gpio 12 pwm, gpio 24 input 1, gpio 22 input 2
# Motor 2: gpio 13 pwm, gpio 25 input 1, gpio 23 input 2
# GPIO 12 pin 32
# GPIO 24 pin 18
# GPIO 22 pin 15

# GPIO 13 pin 33
# GPIO 25 pin 22
# GPIO 23 pin 16

screen = pygame.display.set_mode([50, 50])
pygame.joystick.init()
controller = pygame.joystick.Joystick(0)
controller.init()
i = 0

while True:
#while i < 10000:
    i = i + 1
    for event in pygame.event.get():
        if event.type==pygame.JOYBUTTONDOWN:
            button = True
        elif event.type==pygame.JOYBUTTONUP:
            button = False
    l_trig = controller.get_axis(2)
    r_trig = controller.get_axis(5)

    l_stick_vert = controller.get_axis(1)
    r_stick_vert = controller.get_axis(4)

    l_speed = l_stick_vert * 480
    r_speed = r_stick_vert * 480


    print("LT: ", round(l_speed, 3), " RT: ", round(r_speed, 3), " LTrig (pwm): ", int(l_trig), "    ", end='\r')

    motors.motor1.setSpeed(int(l_speed))
    motors.motor2.setSpeed(int(r_speed))
#    motors.motor1.setSpeed(int(r_trig))

motors.setSpeeds(0,0)
motors.disable()
