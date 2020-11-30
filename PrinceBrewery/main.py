import serial
import time

simulation = True

ser = serial.Serial('COM2')
serSim = serial.Serial('COM3')

simTemp = 20.0
simHLTliter = 0

# res = s.read()
# print(res)

# OUTPUTS
v1_open = 3
v1_close = 5
v2_1 = 7
v2_2 = 11
v3_open = 13
v3_close = 15
v4_open = 19
v4_close = 21
v5_open = 23
v5_close = 29

p1 = 31
p2 = 33

# INPUTS
HL1 = 35
HL2 = 37
HL3 = 8
LL1 = 10
LL2 = 12

# ser = serial.Serial(
#         port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
#         baudrate = 9600,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE,
#         bytesize=serial.EIGHTBITS,
#         timeout=1
# )

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(v1_open, GPIO.OUT)
    GPIO.setup(v1_close, GPIO.OUT)
    GPIO.setup(v2_1, GPIO.OUT)
    GPIO.setup(v2_2, GPIO.OUT)
    GPIO.setup(v3_open, GPIO.OUT)
    GPIO.setup(v3_open, GPIO.OUT)
    GPIO.setup(v4_open, GPIO.OUT)
    GPIO.setup(v4_open, GPIO.OUT)
    GPIO.setup(v5_open, GPIO.OUT)
    GPIO.setup(v5_open, GPIO.OUT)
    GPIO.setup(p1, GPIO.OUT)
    GPIO.setup(p2, GPIO.OUT)

    GPIO.setup(HL1, GPIO.IN)
    GPIO.setup(HL2, GPIO.IN)
    GPIO.setup(HL3, GPIO.IN)
    GPIO.setup(LL1, GPIO.IN)
    GPIO.setup(LL2, GPIO.IN)
except ImportError:
    print ("Not running RPi, can't import library")

def openV1():
    GPIO.output(v1_open, GPIO.HIGH)
    GPIO.output(v1_close, GPIO.LOW)
def closeV1():
    GPIO.output(v1_open, GPIO.LOW)
    GPIO.output(v1_close, GPIO.HIGH)
def setV2(int):
    if (int ==1):
        GPIO.output(v2_1, GPIO.HIGH)
        GPIO.output(v2_2, GPIO.LOW)
    elif (int == 2):
        GPIO.output(v2_1, GPIO.HIGH)
        GPIO.output(v2_2, GPIO.LOW)
def openV3():
    GPIO.output(v3_open, GPIO.HIGH)
    GPIO.output(v3_close, GPIO.LOW)
def closeV3():
    GPIO.output(v3_open, GPIO.LOW)
    GPIO.output(v3_close, GPIO.HIGH)
def openV4():
    GPIO.output(v4_open, GPIO.HIGH)
    GPIO.output(v4_close, GPIO.LOW)
def closeV4():
    GPIO.output(v4_open, GPIO.LOW)
    GPIO.output(v4_close, GPIO.HIGH)
def openV5():
    GPIO.output(v5_open, GPIO.HIGH)
    GPIO.output(v5_close, GPIO.LOW)
def closeV5():
    GPIO.output(v5_open, GPIO.LOW)
    GPIO.output(v5_close, GPIO.HIGH)
def startP1():
    GPIO.output(p1, GPIO.HIGH)
def stopP1():
    GPIO.output(p1, GPIO.LOW)
def startP2():
    GPIO.output(p2, GPIO.HIGH)
def stopP2():
    GPIO.output(p2, GPIO.LOW)


def state1():
    print("Close all valves and pumps")
    try:
        closeV1()
        setV2(1)
        closeV3()
        closeV4()
        closeV5()
        stopP1()
        stopP2()
    except:
        print ("RPI GIIO NOT EXIST")

    # ser.write("You shall Turn off H1")
    # ser.write("You shall Turn off H2")

    print ("All valves and pumps are now closed")

    return 2
def state2():
    print("Fill HLT start")
    try:
        openV1()
    except:
        print ("Not rpi")

    if (HL1 == 1):
        try:
            closeV1()
        except:
            print("Not rpi")
    return 3
def state3():
    global simTemp
    print("Initial heating for meshing 67 degrees")
    ser.write (b'You shall start PID SP;HLT;67\r\n')
    if (simulation == True):
        print ("Simtemp = " + str(simTemp))
        dataSim = serSim.readline()

        print(dataSim)

        dataSimSplit = dataSim.split(b';')

        serSim.write(b'PID FB;' + dataSimSplit[1] + b';T1:' + bytes(str(simTemp), "utf-8") + b'\r\n')
        simTemp+=1
        # time.sleep(1)
    data = ser.readline()
    print ("the data is:")
    print (data)

    x = data.split(b';')

    if (float(x[2].split(b':')[1]) < 67):
        return 3
    else:
        return 4

def state4():
    print("Fill mesh")
    openV3()
    startP2()

    sim

    if (HL2 == 1):
        closeV3()
        stopP2()

    return 5
def state5():
    print("FILL HLT for circulation")
    return 6
def state6():
    print("Heating HLT 80 degrees")
    return 7
def state7():
    print("Execute meshing")
    return 8
def state8():
    print("Circulation")
    return 9
def state9():
    print("Fill boil and heat")
    return 10
def state10():
    print("Rinse")
    return 11
def state11():
    print("Boil 90 min")
    return 12
def state12():
    print("Fill yeast bucket")
    return 42
def default():
    print ("Brew finished")
    return "Brew finished"

switcher = {
    1: state1,
    2: state2,
    3: state3,
    4: state4,
    5: state5,
    6: state6,
    7: state7,
    8: state8,
    9: state9,
    10: state10,
    11: state11,
    12: state12
    }

def switch(state):
    return switcher.get(state, default)()

if __name__ == '__main__':
    state = 1
    while (state <= 12):
        state = switch(state)
        print("next state is: " + str(state))

