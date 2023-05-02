import machine
import network
import socket
import time

# Joystick pins configuration
JOYSTICK_X_PIN = 26
JOYSTICK_Y_PIN = 27
JOYSTICK_SW_PIN = 16

# Set up the ADC for X and Y axes
adc_x = machine.ADC(machine.Pin(JOYSTICK_X_PIN))
adc_y = machine.ADC(machine.Pin(JOYSTICK_Y_PIN))

# Set up the button with a pull-up resistor
button = machine.Pin(JOYSTICK_SW_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

def read_joystick():
    x = adc_x.read_u16()
    y = adc_y.read_u16()
    sw = button.value()

    return x, y, sw

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('ESP8266', 'mypassword')

while not wlan.isconnected():
    print('Connecting to Wi-Fi...')
    time.sleep(1)

print('Connected to Wi-Fi')

# Configure the socket
addr = socket.getaddrinfo('192.168.4.1', 5005)[0][-1]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    x, y, sw = read_joystick()
    data = "{},{},{}".format(x, y, sw)
    s.sendto(data.encode(), addr)
    time.sleep(0.1)
