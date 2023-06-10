import network
import socket
import time
from machine import Pin

# Threshold to determine joystick direction
THRESHOLD = 3000

# Resting position values for X and Y axes
REST_X = 32767
REST_Y = 32767


class Motor:
    def __init__(self, pin_nums):
        self.pins = [Pin(pin_num, Pin.OUT) for pin_num in pin_nums]
        self.state = (0, 0, 0, 0)
        self.reset()

    def reset(self):
        for pin in self.pins:
            pin.off()

    def move(self, state):
        for pin, value in zip(self.pins, state):
            pin.value(value)
        self.state = state


class Joystick:
    def __init__(self, motor):
        self.motor = motor

    def output(self, x, y, sw, btn1, btn2, btn3, btn4):
        if sw == 0:
            print("J-btn")
        if x < REST_X - THRESHOLD:
            self.motor.move((0, 0, 1, 0))
            print("Left")

        elif x > REST_X + THRESHOLD:
            self.motor.move((0, 0, 0, 1))
            print("Right")

        elif y < REST_Y - THRESHOLD:
            self.motor.move((0, 0, 1, 1))
            print("Up")

        elif y > REST_Y + THRESHOLD:
            self.motor.move((1, 1, 0, 0))
            print("Down")

        elif btn1 == 1:
            self.motor.move((1, 0, 0, 1))
            print("btn1")

        elif btn2 == 1:
            self.motor.move((0, 1, 1, 0))
            print("btn2")

        elif btn3 == 1:
            print("btn3")

        elif btn4 == 1:
            print("btn4")

        else:
            # Check if the current motor state is different from the previous state
            if self.motor.state != (0, 0, 0, 0):
                # Stop the motors if there is no active input
                self.motor.move((0, 0, 0, 0))


# Configure Wi-Fi Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP8266", password="mypassword")

# Configure the socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address_info = socket.getaddrinfo("0.0.0.0", 5006)[0][-1]
s.bind(address_info)

print("Listening on", address_info)

motor = Motor([2, 0, 4, 5])
joystick = Joystick(motor)

while True:
    try:
        data, addr = s.recvfrom(1024)
        print(data)
        x, y, sw, btn1, btn2, btn3, btn4 = map(int, data.decode().split(","))
        joystick.output(x, y, sw, btn1, btn2, btn3, btn4)
    except OSError as e:
        print("Error: ", e)
        print("Controller disconnected. Retrying...")
        time.sleep(5)  # wait for 5 seconds before retrying
