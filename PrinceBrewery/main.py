import serial
import time

simulation = True

ser = serial.Serial('COM2')
serSimPhyton = serial.Serial('COM3')

simHLTtemp = 20.0
simBoilTemp = 20.0
simHLTliter = 0
simMeshLiter = 0
simBoilLiter = 0

meshTimerStart = 0.0
meshTimerEnd = 0.0

hltTemp = 0.0

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
    try:
        GPIO.output(v1_open, GPIO.HIGH)
        GPIO.output(v1_close, GPIO.LOW)
    except:
        print ("RPI GIIO NOT EXIST")
def closeV1():
    try:
        GPIO.output(v1_open, GPIO.LOW)
        GPIO.output(v1_close, GPIO.HIGH)
    except:
        print ("RPI GIIO NOT EXIST")
def setV2(int):
    try:
        if (int ==1):
            GPIO.output(v2_1, GPIO.HIGH)
            GPIO.output(v2_2, GPIO.LOW)
        elif (int == 2):
            GPIO.output(v2_1, GPIO.HIGH)
            GPIO.output(v2_2, GPIO.LOW)
    except:
        print ("RPI GIIO NOT EXIST")
def openV3():
    try:
        GPIO.output(v3_open, GPIO.HIGH)
        GPIO.output(v3_close, GPIO.LOW)
    except:
        print ("RPI GIIO NOT EXIST")
def closeV3():
    try:
        GPIO.output(v3_open, GPIO.LOW)
        GPIO.output(v3_close, GPIO.HIGH)
    except:
        print ("RPI GIIO NOT EXIST")
def openV4():
    try:
        GPIO.output(v4_open, GPIO.HIGH)
        GPIO.output(v4_close, GPIO.LOW)
    except:
        print ("RPI GIIO NOT EXIST")
def closeV4():
    try:
        GPIO.output(v4_open, GPIO.LOW)
        GPIO.output(v4_close, GPIO.HIGH)
    except:
        print ("RPI GIIO NOT EXIST")
def openV5():
    try:
        GPIO.output(v5_open, GPIO.HIGH)
        GPIO.output(v5_close, GPIO.LOW)
    except:
        print ("RPI GIIO NOT EXIST")
def closeV5():
    try:
        GPIO.output(v5_open, GPIO.LOW)
        GPIO.output(v5_close, GPIO.HIGH)
    except:
        print ("RPI GIIO NOT EXIST")
def startP1():
    try:
        GPIO.output(p1, GPIO.HIGH)
    except:
        print ("RPI GIIO NOT EXIST")
def stopP1():
    try:
        GPIO.output(p1, GPIO.LOW)
    except:
        print ("RPI GIIO NOT EXIST")
def startP2():
    try:
        GPIO.output(p2, GPIO.HIGH)
    except:
        print ("RPI GIIO NOT EXIST")
def stopP2():
    try:
        GPIO.output(p2, GPIO.LOW)
    except:
        print ("RPI GIIO NOT EXIST")


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
    global simHLTliter
    print("Fill HLT start")
    try:
        openV1()
    except:
        print ("Not rpi")

    if (simulation):
        simHLTliter+=1
        print ("SimHLTliter: " + str(simHLTliter))

    if (HL1 == 1 or simHLTliter == 10):
        try:
            closeV1()
            return 3
        except:
            print("Not rpi")
    else:
        return 2
def state3():
    global simHLTtemp
    print("Initial heating for meshing 67 degrees")
    ser.write (b'You shall start PID SP;HLT;67\r\n')
    if (simulation == True):
        print ("Simtemp = " + str(simHLTtemp))
        dataSim = serSimPhyton.readline()

        print(dataSim)

        dataSimSplit = dataSim.split(b';')

        serSimPhyton.write(b'PID FB;' + dataSimSplit[1] + b';T1:' + bytes(str(simHLTtemp), "utf-8") + b'\r\n')
        simHLTtemp+=1
        time.sleep(0)
    data = ser.readline()
    print ("the data is:")
    print (data)

    x = data.split(b';')

    if (float(x[2].split(b':')[1]) < 67):
        return 3
    else:
        return 4

def state4():
    global simHLTliter
    global simMeshLiter
    print("Fill mesh")
    openV3()
    startP2()

    if (simulation == True):
        simMeshLiter+=1
        print("HLT-liter: " + str(simMeshLiter))



    if (HL2 == 1 or simMeshLiter == 10):
        if (simulation):
            simHLTliter = 0
        closeV3()
        stopP2()
        return 5
    else:
        return 4
def state5():
    print("Re-filling HLT")
    global simHLTliter
    openV1()
    if (simulation and simHLTliter < 10):
        simHLTliter+=1
        print ("Liters in HLT: " + str(simHLTliter))

    if (HL1 == 1 or simHLTliter >= 10):
        closeV1()
    return 6

def state6():
    print("Heating HLT 80 degrees")
    global hltTemp
    ser.write(b'You shall start PID SP;HLT;80\r\n')
    if (simulation == True):
        global simHLTtemp
        print("Simtemp = " + str(simHLTtemp))
        dataSim = serSimPhyton.readline()

        print(dataSim)

        dataSimSplit = dataSim.split(b';')

        serSimPhyton.write(b'PID FB;' + dataSimSplit[1] + b';T1:' + bytes(str(simHLTtemp), "utf-8") + b'\r\n')
        if (simHLTtemp < 80):
            simHLTtemp += 1

    data = ser.readline()
    print("the data is:")
    print(data)

    x = data.split(b';')
    hltTemp = float(x[2].split(b':')[1])
    print ("The temperature in HLT 80 is: " + str(hltTemp))

    # if (float(x[2].split(b':')[1]) < 67):
    #     return 3
    # else:
    #     return 4
    return 7
def state7():
    global hltTemp
    global meshTimerStart
    print("Execute meshing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    currentTime = time.time()
    if (meshTimerStart == 0.0):
        meshTimerStart = time.time()
        print ("Start time: " + str(meshTimerStart))
        return 5
    elif (currentTime - meshTimerStart < 10):
        print ("Still meshing at time: " + str(currentTime - meshTimerStart))
        return 5
    elif (currentTime-meshTimerStart >= 10 and hltTemp >= 80):
        print ("Reached 80 degrees, continuing!")
        return 8
    else:
        print ("Looping while waiting for something to finish...")
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
    while (state <= 14):
        state = switch(state)
        print("next state is: " + str(state))

