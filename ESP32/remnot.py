import machine
import network
import socket
import time

# Joystick pins configuration
JOYSTICK_X_PIN = 26
JOYSTICK_Y_PIN = 27
JOYSTICK_SW_PIN = 15

# Buttons configuration
BUTTON_1_PIN = 10
BUTTON_2_PIN = 11
BUTTON_3_PIN = 12
BUTTON_4_PIN = 13

# Set up the ADC for X and Y axes
adc_x = machine.ADC(machine.Pin(JOYSTICK_X_PIN))
adc_y = machine.ADC(machine.Pin(JOYSTICK_Y_PIN))

# Set up the joystick button with a pull-up resistor
joystick_button = machine.Pin(JOYSTICK_SW_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# Set up additional buttons with pull-up resistors
button1 = machine.Pin(BUTTON_1_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
button2 = machine.Pin(BUTTON_2_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
button3 = machine.Pin(BUTTON_3_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
button4 = machine.Pin(BUTTON_4_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)


def read_joystick_and_buttons():
    x = adc_x.read_u16()
    y = adc_y.read_u16()
    sw = joystick_button.value()
    btn1 = button1.value()
    btn2 = button2.value()
    btn3 = button3.value()
    btn4 = button4.value()

    return x, y, sw, btn1, btn2, btn3, btn4


# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("ESP32")

while not wlan.isconnected():
    print("Connecting to Wi-Fi...")
    time.sleep(1)

print("Connected to Wi-Fi")

# Wait for a brief moment after the Wi-Fi connection is established
time.sleep(2)

# Configure the socket
addr = socket.getaddrinfo("192.168.4.1", 5005)[0][-1]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    if wlan.isconnected():
        x, y, sw, btn1, btn2, btn3, btn4 = read_joystick_and_buttons()
        data = "{},{},{},{},{},{},{}".format(x, y, sw, btn1, btn2, btn3, btn4)
        print(data)
        s.sendto(data.encode(), addr)
    else:
        print("Wi-Fi not connected. Retrying...")
        wlan.connect("ESP32")
    time.sleep(0.1)
