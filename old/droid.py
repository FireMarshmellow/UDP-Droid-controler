import network
import socket
import time
from machine import Pin, PWM

# Configure Wi-Fi Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP8266', password='mypassword')

# Wait for the access point to start
time.sleep(2)

# Configure the socket
addr = socket.getaddrinfo('0.0.0.0', 5005)[0][-1]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(addr)

print('Listening on', addr)

# Initialize continuous servos
servo1_pin = Pin(14)
servo2_pin = Pin(4)
regular_servo_pin = Pin(0)

regular_servo = PWM(regular_servo_pin, freq=40)
servo1 = PWM(servo1_pin, freq=50)
servo2 = PWM(servo2_pin, freq=50)

# Function to control servos
def control_servos(servo1_speed, servo2_speed):
    servo1.duty(servo1_speed)
    servo2.duty(servo2_speed)

def control_regular_servo(angle):
    duty_cycle = int(40 + (angle * 100 / 180))
    regular_servo.duty(duty_cycle)

# Threshold to determine joystick direction
THRESHOLD = 3000

# Resting position values for X and Y axes
REST_X = 32767
REST_Y = 32767

def joystick_output(x, y, sw):
    if sw == 0:
        if x < REST_X - THRESHOLD or x > REST_X + THRESHOLD:
            angle = int((x / (2 * REST_X)) * 180)
            control_regular_servo(angle)
    else:
        control_regular_servo(90)
        if x < REST_X - THRESHOLD:
            print("Left")
            control_servos(40, 40)
        elif x > REST_X + THRESHOLD:
            print("Right")
            control_servos(100, 100)
        elif y < REST_Y - THRESHOLD:
            print("Up")
            control_servos(100, 40)
        elif y > REST_Y + THRESHOLD:
            print("Down")
            control_servos(40, 100)
        else:
            control_servos(0, 0)

while True:
    data, addr = s.recvfrom(1024)
    #print('Received:', data)

    x, y, sw = map(int, data.decode().split(','))
    joystick_output(x, y, sw)

