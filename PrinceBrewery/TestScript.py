from time import sleep  # Import the sleep function from the time module

# OUTPUTS
from pip._vendor.distlib.compat import raw_input

v1_close = 3
v1_open = 5
v2_circulation = 37  # 7
v2_boil = 11
v3_HLT = 13
v3_mesh = 15
# v4_open = 19
# v4_close = 21
v5_open = 23
v5_close = 29

p1 = 31
p2 = 33

try:
    import RPi.GPIO as GPIO

    GPIO.setwarnings(False)  # Ignore warning for now

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(v1_open, GPIO.OUT)
    GPIO.setup(v1_close, GPIO.OUT)
    GPIO.setup(v2_circulation, GPIO.OUT)
    GPIO.setup(v2_boil, GPIO.OUT)
    GPIO.setup(v3_HLT, GPIO.OUT)
    GPIO.setup(v3_mesh, GPIO.OUT)
    #   GPIO.setup(v4_open, GPIO.OUT)
    #   GPIO.setup(v4_open, GPIO.OUT)
    GPIO.setup(v5_open, GPIO.OUT)
    GPIO.setup(v5_close, GPIO.OUT)

    GPIO.setup(p1, GPIO.OUT)
    GPIO.setup(p2, GPIO.OUT)

    GPIO.setup(35, GPIO.OUT)
    GPIO.setup(38, GPIO.OUT)
    GPIO.output(35, GPIO.HIGH)
    GPIO.output(38, GPIO.HIGH)

except ImportError:
    print("Not running RPi, can't import library")


def openV1():
    try:
        print("opening v1")
        GPIO.output(v1_open, GPIO.HIGH)
        sleep(0.001)
        GPIO.output(v1_close, GPIO.LOW)
        sleep(0.001)
        print("end opening v1")
    except:
        print("RPI GPIO1 NOT EXIST")


def closeV1():  # vi mA start pump1
    try:
        print("closing v1")
        GPIO.output(v1_open, GPIO.LOW)
        sleep(0.1)
        GPIO.output(v1_close, GPIO.HIGH)
        sleep(0.1)
        print("end closing v1")
    except:
        print("RPI GPIO2 NOT EXIST")


def setV2(i):
    try:
        if i == 1:
            print("set_v2_circulation")
            GPIO.output(v2_circulation, GPIO.HIGH)
            sleep(0.1)
            GPIO.output(v2_boil, GPIO.LOW)
            print("end set_v2_circulation")
        elif i == 2:
            print("set_v2_boil")
            GPIO.output(v2_circulation, GPIO.LOW)
            sleep(0.1)
            GPIO.output(v2_boil, GPIO.HIGH)
            print("end set_v2_boil")
        sleep(0.2)
    except:
        print("RPI GPIO3 NOT EXIST")


def setV3Mesh():
    try:
        print("open v3")
        GPIO.output(v3_HLT, GPIO.LOW)
        sleep(0.1)
        GPIO.output(v3_mesh, GPIO.HIGH)
        sleep(0.2)
        print("end open v3")
    except:
        print("RPI GPIO4 NOT EXIST")


def setV3HLT():
    try:
        print("closing v3")
        GPIO.output(v3_HLT, GPIO.HIGH)
        sleep(0.1)
        GPIO.output(v3_mesh, GPIO.LOW)
        sleep(0.2)
        print("end closing v3")
    except:
        print("RPI GPIO5 NOT EXIST")


# def openV4():
# try:
# print ("open v4")
# GPIO.output(v4_open, GPIO.HIGH)
# sleep(1)
# GPIO.output(v4_close, GPIO.LOW)
# sleep(5)
# print ("end open v4")
# except:
# print("RPI GPIO6 NOT EXIST")


# def closeV4():
# try:
# print ("closing v4")
# GPIO.output(v4_open, GPIO.LOW)
# sleep(1)
# GPIO.output(v4_close, GPIO.HIGH)
# sleep(5)
# print ("end closing v4")
# except:
# print("RPI GPIO7 NOT EXIST")


def openV5():
    try:
        print("open v5")
        GPIO.output(v5_open, GPIO.HIGH)
        sleep(0.1)
        GPIO.output(v5_close, GPIO.LOW)
        sleep(0.2)
        print("end open v5")
    except:
        print("RPI GPIO8 NOT EXIST")


def closeV5():
    try:
        print("closing v5")
        GPIO.output(v5_open, GPIO.LOW)
        sleep(0.1)
        GPIO.output(v5_close, GPIO.HIGH)
        sleep(0.2)
        print("end closing v5")
    except:
        print("RPI GPIO9 NOT EXIST")


def startP1():
    try:
        print("Start p1")
        GPIO.output(p1, GPIO.LOW)
        print("End start p1")
    except:
        print("RPI GPIO10 NOT EXIST")


def stopP1():
    try:
        print("Stop p1")
        GPIO.output(p1, GPIO.HIGH)
    except:
        print("RPI GPIO11 NOT EXIST")


def startP2():
    try:
        print("Start p2")
        GPIO.output(p2, GPIO.LOW)
    except:
        print("RPI GPIO12 NOT EXIST")


def stopP2():
    try:
        print("Stop p2")
        GPIO.output(p2, GPIO.HIGH)
    except:
        print("RPI GPIO13 NOT EXIST")


while True:  # Run forever
    value = raw_input("Please enter a string:\n")

    if "openV1" in str(value):
        openV1()

    elif "closeV1" in str(value):
        closeV1()

    elif "setV2Circ" in str(value):
        setV2(1)

    elif "setV2Boil" in str(value):
        setV2(2)

    elif "setV3Mesh" in str(value):
        setV3Mesh()

    elif "setV3HLT" in str(value):
        setV3HLT()

    elif "openV5" in str(value):
        openV5()

    elif "closeV5" in str(value):
        closeV5()

    elif "startP1" in str(value):
        startP1()

    elif "stopP1" in str(value):
        stopP1()

    elif "startP2" in str(value):
        startP2()

    elif "stopP2" in str(value):
        stopP2()

    elif "reset" in str(value):
        closeV1()
        sleep(1)
        setV2(1)
        sleep(1)
        setV3HLT()
        sleep(1)
        closeV5()
        sleep(1)
        stopP1()
        sleep(1)
        stopP2()
        sleep(1)

    else:
        print("Invalid command! Try again...")

## GPIO.output(3, GPIO.LOW) # Turn on
# sleep(1) # Sleep for 1 second
# GPIO.output(5, GPIO.HIGH) # Turn on

# sleep(5) # Sleep for 1 second


# GPIO.output(3, GPIO.HIGH) # Turn off
# sleep(1) # Sleep for 1 second
# GPIO.output(5, GPIO.LOW) # Turn off

# sleep(5) # Sleep for 1 second

