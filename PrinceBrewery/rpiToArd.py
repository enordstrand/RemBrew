import serial
import time
from time import sleep

state2_firstRun = True
state5_firstRun_open = True
state5_firstRun_close = True
state9_firstRun = True


meshTempSP = 20.0
circulationTempSP = 25.0
boilTempSP = 30.0
heightLevelMinimumSP = 600.0
heightLevelMaximumSP = 620.0
refillHLTSP = 630.0
rinseLiter = 50.0

meshTimerStart = 0.0
circulationTimerStart = 0.0
rinseTimerStart = 0.0
boilTimerStart = 0.0

meshTime = 200.0
circulationTime = 60.0
rinseTime = 300.0
boilTime1 = 300.0
boilTime2 = 300.0

hltTemp = 0.0
heightLevel = 0.0

rinseProcessDone = False

# OUTPUTS
v1_close = 3
v1_open = 5
v2_circulation = 29
v2_boil = 11
v3_HLT = 13
v3_mesh = 15
v5_open = 23
v5_close = 29

p1 = 31
p2 = 33

# INPUTS
HL1 = 35
HL3 = 8

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

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
    GPIO.setup(v5_open, GPIO.OUT)
    GPIO.setup(v5_close, GPIO.OUT)
    GPIO.setup(p1, GPIO.OUT)
    GPIO.setup(p2, GPIO.OUT)
except ImportError:
    print("Not running RPi, can't import library")


def openV1():
    try:
        GPIO.output(v1_open, GPIO.HIGH)
        GPIO.output(v1_close, GPIO.LOW)
    except:
        print("RPI GPIO1 NOT EXIST")


def closeV1():
    try:
        GPIO.output(v1_open, GPIO.LOW)
        GPIO.output(v1_close, GPIO.HIGH)
    except:
        print("RPI GPIO2 NOT EXIST")


def setV2(i):
    try:
        if i == 1:
            GPIO.output(v2_circulation, GPIO.HIGH)
            GPIO.output(v2_boil, GPIO.LOW)
        elif i == 2:
            GPIO.output(v2_circulation, GPIO.LOW)
            GPIO.output(v2_boil, GPIO.HIGH)
    except:
        print("RPI GPIO3 NOT EXIST")


def setV3Mesh():
    try:
        GPIO.output(v3_HLT, GPIO.LOW)
        GPIO.output(v3_mesh, GPIO.HIGH)
    except:
        print("RPI GPIO4 NOT EXIST")


def setV3HLT():
    try:
        GPIO.output(v3_HLT, GPIO.HIGH)
        GPIO.output(v3_mesh, GPIO.LOW)
    except:
        print("RPI GPIO5 NOT EXIST")

def openV5():
    try:
        GPIO.output(v5_open, GPIO.HIGH)
        GPIO.output(v5_close, GPIO.LOW)
    except:
        print("RPI GPIO8 NOT EXIST")


def closeV5():
    try:
        GPIO.output(v5_open, GPIO.LOW)
        GPIO.output(v5_close, GPIO.HIGH)
    except:
        print("RPI GPIO9 NOT EXIST")


def startP1():
    try:
        GPIO.output(p1, GPIO.LOW)
    except:
        print("RPI GPIO10 NOT EXIST")


def stopP1():
    try:
        GPIO.output(p1, GPIO.HIGH)
    except:
        print("RPI GPIO11 NOT EXIST")


def startP2():
    try:
        GPIO.output(p2, GPIO.LOW)
    except:
        print("RPI GPIO12 NOT EXIST")


def stopP2():
    try:
        GPIO.output(p2, GPIO.HIGH)
    except:
        print("RPI GPIO13 NOT EXIST")


def state1():
    print("State 1: Close all valves and pumps")
    try:
        closeV1()
        setV2(1)
        setV3HLT()
        closeV5()
        stopP1()
        stopP2()
    except:
        print("RPI GPIO NOT EXIST")

    ser.write(b'You shall Turn off H1\r\n')
    waitForResponse("Turn off H1")
    waitForResponse("turned off H1")

    ser.write(b'You shall Turn off H3\r\n')
    waitForResponse("Turn off H3")
    waitForResponse("turned off H3")

    temp = ser.readline()
    print("temp" + str(temp))
    print("All valves and pumps are now closed")

    return 2

def waitForResponse(expectedMessage):
    while True:
        confirmation = ser.readline()
        if expectedMessage in confirmation:
            return confirmation

def state2():
    print("State 2: Fill HLT start")
    global state2_firstRun
    global heightLevel

    ser.write(b'You shall Give HL1\r\n')
    waitForResponse("Give HL1")
    temp = waitForResponse("gave HL1")

    if "HL1" in temp:
        data = temp

    heightLevel = float(data.split(b':')[1])
    print("The number of liters in HLT is: " + str(heightLevel))
    if state2_firstRun:
        openV1()
        state2_firstRun = False

    if heightLevel > heightLevelMinimumSP:
        startP1()
    else:
        stopP1()

    if heightLevel > heightLevelMaximumSP:
        try:
            closeV1()
            return 3
        except:
            print("Not rpi")
    else:
        return 2


def state3():
    global meshTempSP
    print("State 3: Initial heating for mesh.")
    ser.write(b'You shall start PID SP;HLT;' + bytes(str(meshTempSP)) + b'\r\n')
    temp = ser.readline()
    print("SP: " + str(meshTempSP) + " degrees, FB: " + str(temp) + " degrees.")
    if "sent me" in temp is False:
        data = temp

    temp = ser.readline()
    print("the temp2 is: " + str(temp))
    if not "sent me" in temp:
        data = temp

    print("Awesome data is: " + str(data))

    x = data.split(b';')

    if float(x[2].split(b':')[1]) < meshTempSP:
        return 3
    else:
        ser.write(b'You shall Turn off H1\r\n')
        waitForResponse("Turn off H1")
        waitForResponse("turned off H1")
        return 4


def state4():
    global heightLevel
    print("State 4: Pump water from HLT to Mesh.")
    ser.write(b'You shall Give HL1\r\n')
    waitForResponse("Give HL1")
    temp = waitForResponse("gave HL1")

    if "HL1" in temp:
        data = temp

    heightLevel = float(data.split(b':')[1])
    print("The number of liters in HLT is: " + str(heightLevel))
    setV3Mesh()

    if heightLevel < 580.0:
        setV3HLT()
        stopP1()
        return 5
    else:
        return 4


def state5():
    print("State 5: Re-filling HLT")
    global state5_firstRun_open
    global state5_firstRun_close
    global heightLevel
    global refillHLTSP

    ser.write(b'You shall Give HL1\r\n')
    waitForResponse("Give HL1")
    temp = waitForResponse("gave HL1")

    if "HL1" in temp:
        data = temp

    heightLevel = float(data.split(b':')[1])
    print("The number of liters in HLT is: " + str((heightLevel/7)-54.71))

    if state5_firstRun_open:
        openV1()
        state5_firstRun_open = False
    if heightLevel > 600.0:
        if state5_firstRun_close:
            startP1()

    if heightLevel > refillHLTSP:
        if state5_firstRun_close:
            closeV1()
            state5_firstRun_close = False
    return 6


def state6():
    global circulationTempSP
    print("State 6: Heating HLT for Circulation")
    global hltTemp
    ser.write(b'You shall start PID SP;HLT;' + bytes(str(circulationTempSP)) + b'\r\n')
    temp = ser.readline()
    print("HLT SP: " + str(circulationTempSP) + "FB: " + str(temp))
    if not "sent me" in temp:
        data = temp

    temp = ser.readline()
    print("the temp2 is: " + str(temp))
    if not "sent me" in temp:
        data = temp

    print("Awesome data is: " + str(data))

    x = data.split(b';')
    hltTemp = float(x[2].split(b':')[1])
    print("The HLT SP: " + str(circulationTempSP) + ", FB: " + str(hltTemp))
    return 7


def state7():
    global hltTemp
    global meshTimerStart
    global circulationTempSP
    global meshTime
    print("State 7: Start mesh timer")
    currentTime = time.time()
    if meshTimerStart == 0.0:
        meshTimerStart = time.time()
        print("Mesh timer started...")
        return 5
    elif currentTime - meshTimerStart < meshTime:
        print("Meshing time: " + str(currentTime - meshTimerStart))
        return 5
    elif currentTime - meshTimerStart >= meshTime and hltTemp >= circulationTempSP - 2:
        print("Reached " + str(circulationTempSP) + " degrees and " + str(meshTime / 60.0) + " minutes, continuing!")
        return 8
    else:
        print("Looping while waiting for something to finish...")
        print(meshTime)
        return 5


def state8():
    global circulationTimerStart
    print("State 8: Start circulation timer")
    currentTime = time.time()
    if circulationTimerStart == 0.0:
        circulationTimerStart = time.time()
        startP2()
        setV2(1)
        print("circulation timer started...")
        return 8
    elif currentTime - circulationTimerStart < circulationTime:
        print("Still circulating at time: " + str(currentTime - circulationTimerStart))
        return 6
    elif currentTime - circulationTimerStart >= circulationTime:
        print("Reached 80 minutes circulation at 80 degrees. Continuing!")
        return 9


def state9():
    print("State 9: Fill boil and heat")
    global rinseProcessDone
    global hltTemp
    global boilTempSP
    global heightLevel
    global state9_firstRun

    ser.write(b'You shall Give HL3\r\n')
    waitForResponse("Give HL3")
    temp = waitForResponse("gave HL3")

    if "HL3" in temp:
        data = temp

    heightLevel = float(data.split(b':')[1])

    if heightLevel > 800.0: # 620.0
        print("INSIDE IF")
        stopP2()  # Maybe we can remove this.
    else:
        print("INSIDE ELSE")
        if state9_firstRun:
            startP2() #Redundant
            print("INSIDE ELSE IF")
            setV2(2)
            #state9_firstRun = False
    if heightLevel > 730.0:
#   WE NEED TO CALIBRATE OR FIX BOIL SENSOR SO THAT IT IS CORRECT ON 100 DEGREES
        ser.write(b'You shall start PID SP;Boil;' + bytes(str(boilTempSP)) + b'\r\n')
        waitForResponse("PID SP;Boil")
        temp = waitForResponse("PID FB")

        if "Boil" in temp:
            data = temp

        temp = ser.readline()
        print("the temp2 is:")
        print(temp)
        if "Boil" in temp:
            data = temp

        print("Awesome data is:")
        print(data)

        x = data.split(b';')
        boilTemp = float(x[2].split(b':')[1])
        print("The temperature in Boil 100 is: " + str(boilTemp))

        if boilTemp >= boilTempSP:
            print("The wort is now boiling. Remember to add 60' hops!")
            if rinseProcessDone:
                return 11

        print("The rinseProcess done is: ")
        print(rinseProcessDone)
        if rinseProcessDone:
            return 9
        else:
            return 10
    else:
        return 9


def state10():
    print("Rinse")
    global rinseTimerStart  # Rinse timer can later be changed to Flow Controller
    global rinseProcessDone
    global heightLevel
    global rinseLiter

    print("start serial write to get high level HLT")
    ser.write(b'You shall Give HL1\r\n')
    print("end serial write")
    waitForResponse("Give HL1")
    print("end wait for response")
    temp = waitForResponse("gave HL1")

    if "HL1" in temp:
        data = temp

    heightLevel = float(data.split(b':')[1])

    if heightLevel < refillHLTSP-rinseLiter and rinseProcessDone == False:
        stopP1()
        rinseProcessDone = True
        print("Done pumping fresh water to mesh")
    else:
        setV3Mesh()
        startP1()

    return 9


def state11():
    print("Boil 60 min")
    global boilTimerStart

    if boilTimerStart == 0.0:
        boilTimerStart = time.time()

    currentTime = time.time()
    if currentTime - boilTimerStart < boilTime1:
        print("Waiting for the second Hops to be inserted. Time: " + str(currentTime - boilTimerStart))
        return 11
    elif boilTime1 <= currentTime - boilTimerStart < boilTime2:
        print("Waiting for the boil process to finish. Time: " + str(currentTime - boilTimerStart))
        return 11
    elif currentTime - boilTimerStart >= boilTime2:
        print("Done with the boiling")
        return 12


def state12():
    print("Fill yeast bucket")
    print("Please open V5")
    return 12
    # print("clean up")
    # GPIO.cleanup() # cleanup all GPIO


def default():
    print("Brew finished")
    return 42


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
    12: state12,
    13: default
}


def switch(brewState):
    return switcher.get(brewState, default)()


if __name__ == '__main__':
    state = 1
    while state <= 13:
        state = switch(state)
        print("next state is: " + str(state))
