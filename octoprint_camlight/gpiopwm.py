# coding=utf-8

from optparse import OptionParser
import RPi.GPIO as GPIO

# Min and Max Values
speed_min = 50
speed_max = 5000
gpio_pin = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(gpio_pin, GPIO.OUT)

on_or_off = 0
speed = 50

parser = OptionParser()
parser.add_option("--speed", dest="speed", help="PWM Speed percentage")
parser.add_option("--lon", dest="on_or_off", help="Define if lights are turned on or off")
(options, args) = parser.parse_args()

if options.speed:
    speed = float(options.speed)
if options.on_or_off:
    on_or_off = options.on_or_off

if on_or_off == "true":
    frequency = speed_min + (((speed_max - speed_min) / 100) * speed)
    print "Starte PWM auf GPIO" + str(gpio_pin) + " mit " + str(frequency) + " Hz"
    p = GPIO.PWM(gpio_pin, frequency)
    p.start(1)
else:
    p = GPIO.PWM(gpio_pin, 1)
    print "Stoppe PWM auf GPIO" + str(gpio_pin)
    p.stop()
    GPIO.cleanup()
