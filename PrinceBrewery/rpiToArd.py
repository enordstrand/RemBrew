import serial
import time
from time import sleep  # Import the sleep function from the time module

# ser = serial.Serial('COM3')
# serSimPython = serial.Serial('COM4')

simulation = False

state2_firstRun = True
state5_firstRun_open = True
state5_firstRun_close = True
state9_firstRun = True

simHLTtemp = 20.0
simBoilTemp = 20.0
simHLTliter = 0
simMeshLiter = 0
simBoilLiter = 0

#meshTempSP = 67.0
meshTempSP = 37.0
circulationTempSP = 45.0
boilTempSP = 80.0

meshTimerStart = 0.0
circulationTimerStart = 0.0
rinseTimerStart = 0.0
boilTimerStart = 0.0

meshTime = 10
circulationTime = 5
rinseTime = 10
boilTime1 = 30
boilTime2 = 50

hltTemp = 0.0
highLevel = 0.0

rinseProcessDone = False

# OUTPUTS
v1_close = 3
v1_open = 5
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
# HL2 = 37
HL3 = 8
# LL1 = 10
# LL2 = 12

ser = serial.Serial(
    port='/dev/ttyACM0',  # Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

serSimPython = ""

try:
    import RPi.GPIO as GPIO

    GPIO.setwarnings(False)  # Ignore warning for now

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(v1_open, GPIO.OUT)
    GPIO.setup(v1_close, GPIO.OUT)
    GPIO.setup(v2_1, GPIO.OUT)
    GPIO.setup(v2_2, GPIO.OUT)
    GPIO.setup(v3_open, GPIO.OUT)
    GPIO.setup(v3_close, GPIO.OUT)
    GPIO.setup(v4_open, GPIO.OUT)
    GPIO.setup(v4_open, GPIO.OUT)
    GPIO.setup(v5_open, GPIO.OUT)
    GPIO.setup(v5_close, GPIO.OUT)
    GPIO.setup(p1, GPIO.OUT)
    GPIO.setup(p2, GPIO.OUT)

#    GPIO.setup(HL1, GPIO.IN)
#    GPIO.setup(HL2, GPIO.IN)
#    GPIO.setup(HL3, GPIO.IN)
#    GPIO.setup(LL1, GPIO.IN)
#    GPIO.setup(LL2, GPIO.IN)
except ImportError:
    print("Not running RPi, can't import library")


def openV1():
    try:
        print("opning v1")
        GPIO.output(v1_open, GPIO.HIGH)
        sleep(1)
        GPIO.output(v1_close, GPIO.LOW)
        sleep(5)
        print("end opning v1")
    except:
        print("RPI GPIO1 NOT EXIST")


def closeV1():  # vi mA starte pump1
    try:
        print("closing v1")
        GPIO.output(v1_open, GPIO.LOW)
        sleep(1)
        GPIO.output(v1_close, GPIO.HIGH)
        sleep(5)
        print("end closing v1")
    except:
        print("RPI GPIO2 NOT EXIST")


def setV2(i):
    try:
        if i == 1:
            print("set_v2_1")
            GPIO.output(v2_1, GPIO.HIGH)
            sleep(1)
            GPIO.output(v2_2, GPIO.LOW)
            print("end set_v2_1")
        elif i == 2:
            print("set_v2_2")
            GPIO.output(v2_1, GPIO.LOW)
            sleep(1)
            GPIO.output(v2_2, GPIO.HIGH)
            print("end set_v2_2")
        sleep(5)
    except:
        print("RPI GPIO3 NOT EXIST")


def openV3():
    try:
        print("open v3")
        GPIO.output(v3_open, GPIO.LOW)
        sleep(1)
        GPIO.output(v3_close, GPIO.HIGH)
        sleep(5)
        print("end open v3")
    except:
        print("RPI GPIO4 NOT EXIST")


def closeV3():
    try:
        print("closing v3")
        GPIO.output(v3_open, GPIO.HIGH)
        sleep(1)
        GPIO.output(v3_close, GPIO.LOW)
        sleep(5)
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
        sleep(1)
        GPIO.output(v5_close, GPIO.LOW)
        sleep(5)
        print("end open v5")
    except:
        print("RPI GPIO8 NOT EXIST")


def closeV5():
    try:
        print("closing v5")
        GPIO.output(v5_open, GPIO.LOW)
        sleep(1)
        GPIO.output(v5_close, GPIO.HIGH)
        sleep(5)
        print("end closing v5")
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
    print("Close all valves and pumps")
    try:
        closeV1()
        ###print("end close V1")
        setV2(1)
        ###print("end setV2(1)")
        closeV3()
        ###print("end close V3")
        # closeV4()
        # print ("end close v4")
        closeV5()
        print("end close v5")
        stopP1()
        print("end stop p1")
        stopP2()
        print("end stop p2")
    except:
        print("RPI GPIO NOT EXISTTT")

    print("start serial write")
    ser.write(b'You shall Turn off H1\r\n')
    print("end serial write")
    waitForResponseAndPrint("Turn off H1")
    print("end wait for response")
    waitForResponseAndPrint("turned off H1")

    ser.write(b'You shall Turn off H3\r\n')
    waitForResponseAndPrint("Turn off H3")
    waitForResponseAndPrint("turned off H3")

    temp = ser.readline()
    print("temp" + temp)
    print("All valves and pumps are now closed")

    return 2
    # return 8


def waitForResponseAndPrint(expectedMessage):
    while (True):
        confirmation = ser.readline()
        if (expectedMessage in confirmation):
            print("response: " + confirmation)
            return confirmation
            # break


def state2():
    print("Fill HLT start")
    global simHLTliter
    global state2_firstRun
    global highLevel

    print("start serial write to get high level HLT")
    ser.write(b'You shall Give HL1\r\n')
    print("end serial write")
    waitForResponseAndPrint("Give HL1")
    print("end wait for response")
    temp = waitForResponseAndPrint("gave HL1")

    if "HL1" in temp:
        data = temp

    highLevel = float(data.split(b':')[1])
    print("The number of liters in HLT is: " + str(highLevel))
    if highLevel > 400:
        startP1()
    if state2_firstRun:
        openV1()
        state2_firstRun = False

    if simulation:
        simHLTliter += 1
        print("SimHLTliter: " + str(simHLTliter))
        time.sleep(1)

    if highLevel > 1100.0 or simHLTliter == 10:
        try:
            closeV1()
            ###         startP1()
            return 3
        except:
            print("Not rpi")
    else:
        return 2


def state3():
    global simHLTtemp
    global meshTempSP
    print("Initial heating for meshing " + str(meshTempSP) + " degrees")
    # ser.write(b'You shall start PID SP;HLT;' + bytes(str(meshTempSP), "utf-8") + b'\r\n')
    ser.write(b'You shall start PID SP;HLT;' + bytes(str(meshTempSP)) + b'\r\n')

    # ser.write(b'test\r\n')
    # if simulation:
    #     print("Sim HLT temp = " + str(simHLTtemp))
    #     # dataSim = serSimPython.readline()
    #     dataSim = ser.readline()
    #
    #     print(dataSim)
    #
    #     dataSimSplit = dataSim.split(b';')
    #
    #     ser.write(b'PID FB;' + dataSimSplit[1] + b';T1:' + bytes(str(simHLTtemp)) + b'\r\n')
    #     # serSimPython.write(b'PID FB;' + dataSimSplit[1] + b';T1:' + bytes(str(simHLTtemp), "utf-8")
    #     simHLTtemp += 1
    #     time.sleep(0)
    temp = ser.readline()
    print("the temp1 is:")
    print(temp)
    if not "sent me" in temp:
        data = temp

    temp = ser.readline()
    print("the temp2 is:")
    print(temp)
    if not "sent me" in temp:
        data = temp

    print("Awesome data is:")
    print(data)

    x = data.split(b';')

    # Maybe remove minus 2
    if float(x[2].split(b':')[1]) < meshTempSP -2:
        return 3
    else:
        print("start serial write")
        ser.write(b'You shall Turn off H1\r\n')
        print("end serial write")
        waitForResponseAndPrint("Turn off H1")
        print("end wait for response")
        waitForResponseAndPrint("turned off H1")
        return 4


def state4():
    global simHLTliter
    global simMeshLiter
    global highLevel

    print("start serial write to get high level HLT")
    ser.write(b'You shall Give HL1\r\n')
    print("end serial write")
    waitForResponseAndPrint("Give HL1")
    print("end wait for response")
    temp = waitForResponseAndPrint("gave HL1")

    if "HL1" in temp:
        data = temp

    highLevel = float(data.split(b':')[1])
    print("The number of liters in HLT is: " + str(highLevel))
    print("Fill mesh")
    openV3()

    if simulation == True:
        simMeshLiter += 1
        print("Mesh-liter: " + str(simMeshLiter))

    if highLevel < 950.0 or simMeshLiter == 10:
        if simulation:
            simHLTliter = 0
        closeV3()
        return 5
    else:
        return 4


def state5():
    print("Re-filling HLT")
    global simHLTliter
    global state5_firstRun_open
    global state5_firstRun_close
    global highLevel

    print("start serial write to get high level HLT")
    ser.write(b'You shall Give HL1\r\n')
    print("end serial write")
    waitForResponseAndPrint("Give HL1")
    print("end wait for response")
    temp = waitForResponseAndPrint("gave HL1")

    if "HL1" in temp:
        data = temp

    highLevel = float(data.split(b':')[1])



    if state5_firstRun_open:
        openV1()
        state5_firstRun_open = False
    if simulation and simHLTliter < 10:
        simHLTliter += 1
        print("Liters in HLT: " + str(simHLTliter))

    if highLevel > 1100.0 or simHLTliter >= 10:
        if state5_firstRun_close:
            closeV1()
            state5_firstRun_close = False
    return 6


def state6():
    global circulationTempSP
    print("Heating HLT " + str(circulationTempSP) + " degrees")
    global hltTemp
    #global highLevel
    ser.write(b'You shall start PID SP;HLT;' + bytes(str(circulationTempSP)) + b'\r\n')
    # if simulation == True:
    #     global simHLTtemp
    #     print("Sim HLT temp = " + str(simHLTtemp))
    #     dataSim = serSimPython.readline()
    #
    #     print(dataSim)
    #
    #     dataSimSplit = dataSim.split(b';')
    #
    #     serSimPython.write(b'PID FB;' + dataSimSplit[1] + b';T1:' + bytes(str(simHLTtemp), "utf-8") + b'\r\n')
    #     if simHLTtemp < circulationTempSP:
    #         simHLTtemp += 1

    temp = ser.readline()
    print("the temp1 is:")
    print(temp)
    if not "sent me" in temp:
        data = temp

    temp = ser.readline()
    print("the temp2 is:")
    print(temp)
    if not "sent me" in temp:
        data = temp

    print("Awesome data is:")
    print(data)

    x = data.split(b';')
    hltTemp = float(x[2].split(b':')[1])
    #highLevel = float(x[5].split(b':')[1])
    print("The temperature in HLT " + str(circulationTempSP) + " is: " + str(hltTemp))
    #print("Liters in HLT: " + str(highLevel))
    return 7


def state7():
    global hltTemp
    global meshTimerStart
    global circulationTempSP
    global meshTime
    currentTime = time.time()
    if meshTimerStart == 0.0:
        meshTimerStart = time.time()
        print("Mesh timer started...")
        return 5
    elif currentTime - meshTimerStart < meshTime:
        print("Still meshing at time: " + str(currentTime - meshTimerStart))
        return 5
    elif currentTime - meshTimerStart >= meshTime and hltTemp >= circulationTempSP - 2:
        print("Reached " + str(circulationTempSP) + " degrees and " + str(meshTime / 60.0) + " minutes, continuing!")
        return 8
    else:
        print("Looping while waiting for something to finish...")
        return 5


def state8():
    global circulationTimerStart
    print("Circulation")
    currentTime = time.time()
    if circulationTimerStart == 0.0:
        startP1()
        circulationTimerStart = time.time()
        print("circulation timer started...")
        return 8
    elif currentTime - circulationTimerStart < circulationTime:
        print("Still circulating at time: " + str(currentTime - circulationTimerStart))
        return 8
    elif currentTime - circulationTimerStart >= circulationTime:
        print("Reached 80 minutes circulation at 80 degrees. Continuing!")
        return 9


def state9():
    print("Fill boil and heat")
    global rinseProcessDone
    global simBoilLiter
    global hltTemp
    global boilTempSP
    global highLevel

    print("start serial write to get high level HLT")
    ser.write(b'You shall Give HL3\r\n')
    print("end serial write")
    waitForResponseAndPrint("Give HL3")
    print("end wait for response")
    temp = waitForResponseAndPrint("gave HL3")

    if "HL3" in temp:
        data = temp

    highLevel = float(data.split(b':')[1])

    if (highLevel > 1000.0 or simBoilLiter >= 10):
        stopP1()  # Maybe we can remove this.
    else:
        if state9_firstRun:
            setV2(2)
            # startP1()

        if simulation:
            simBoilLiter += 1
            print("Boil has " + str(simBoilLiter) + " Liters ")

    if highLevel > 600 or simBoilLiter > 2:

        # WE NEED TO CALIBRATE OR FIX BOIL SENSOR SO THAT IT IS CORRECT ON 100 DEGREES
        ser.write(b'You shall start PID SP;Boil;80\r\n')
        waitForResponseAndPrint("PID SP;Boil")
        temp = waitForResponseAndPrint("PID FB")

        # if simulation:
        #     global simBoilTemp
        #     print("Sim boil temp = " + str(simBoilTemp))
        #     dataSim = serSimPython.readline()
        #
        #     print(dataSim)
        #
        #     dataSimSplit = dataSim.split(b';')
        #
        #     serSimPython.write(b'PID FB;' + dataSimSplit[1] + b';T1:' + bytes(str(simBoilTemp), "utf-8") + b'\r\n')
        #     if simBoilTemp < 100:
        #         simBoilTemp += 1

        # temp3 = ser.readline()
        # print("the temp3 is:")
        # print(temp3)
        # temp = ser.readline()
        # print("the temp is:")
        # print(temp)
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
            print("The vurth is now boiling. Remember to add 60' hops!")
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
    global simMeshLiter
    global rinseTimerStart  # Rinse timer can later be changed to Flow Controller
    global rinseProcessDone
    global highLevel

    print("start serial write to get high level HLT")
    ser.write(b'You shall Give HL1\r\n')
    print("end serial write")
    waitForResponseAndPrint("Give HL1")
    print("end wait for response")
    temp = waitForResponseAndPrint("gave HL1")

    if "HL1" in temp:
        data = temp

    highLevel = float(data.split(b':')[1])
    startP1()

    if simulation:

        if simMeshLiter > 1:
            simMeshLiter -= 1
            print("Remaining simMeshLiter: " + str(simMeshLiter))

    if (highLevel < 800 or simMeshLiter <= 1) and rinseTimerStart == 0.0:
        openV3()
        startP2()
        rinseTimerStart = time.time()
        print("The rinse timer has started")
    current_time = time.time()
    if rinseTimerStart > 0.0 and rinseProcessDone == False:
        print("The rinse process has last for: " + str(current_time - rinseTimerStart) + " seconds.")
    if rinseTimerStart > 0.0 and (current_time - rinseTimerStart > rinseTime):
        closeV3()
        stopP2()
        print("rinseProcessDone")
        rinseProcessDone = True

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
