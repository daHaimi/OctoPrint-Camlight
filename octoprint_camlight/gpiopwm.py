# coding=utf-8
import time
from optparse import OptionParser
import RPi.GPIO as GPIO
import socket
import os, os.path

sockpath = "/var/run/gpio.sock"
frequency = 100
gpio_pin = 13
gpio_resource = 0

def setup_gpio():
    global gpio_pin
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(gpio_pin, GPIO.OUT)

def shutdown_gpio():
    global gpio_resource
    if gpio_resource <> 0:
        gpio_resource.stop()
        GPIO.cleanup()
        
def start_gpio(speed):
    global gpio_pin
    global frequency
    global gpio_resource
    gpio_resource = GPIO.PWM(gpio_pin, frequency)
    gpio_resource.start(speed)
    
def change_gpio(speed):
    global gpio_resource
    gpio_resource.ChangeDutyCycle(speed)

if os.path.exists(sockpath):
    os.remove(sockpath)

server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
server.bind(sockpath)
os.chmod(sockpath, 0777)

while True:
    datagram = server.recv(1024)
    if not datagram:
        break
    else:
        if datagram == "exit":
            break
        else:
            parts = datagram.split()
            if parts[0] == "set":
                if gpio_resource == 0:
                    setup_gpio()
                    start_gpio(float(parts[1]))
                else:
                    change_gpio(float(parts[1]))
            elif parts[0] == "stp":
                change_gpio(0)
                    
shutdown_gpio()
server.close()
os.remove(sockpath)
