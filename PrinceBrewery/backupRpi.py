import serial
import time

simulation = True

# ser = serial.Serial('COM3')
# serSimPython = serial.Serial('COM4')

simHLTtemp = 20.0
simBoilTemp = 20.0
simHLTliter = 0
simMeshLiter = 0
simBoilLiter = 0

meshTempSP = 67.0
circulationTempSP = 80.0
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

rinseProcessDone = False

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

ser = serial.Serial(
        port='/dev/ttyACM0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

serSimPython = ""

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
    print("Not running RPi, can't import library")


def openV1():
    try:
        GPIO.output(v1_open, GPIO.HIGH)
        GPIO.output(v1_close, GPIO.LOW)
    except:
        print("RPI GPIO NOT EXIST")


def closeV1():
    try:
        print ("Hei Amir")
        GPIO.output(v1_open, GPIO.LOW)
        GPIO.output(v1_close, GPIO.HIGH)
        print ("Bye Amir")
    except:
        print("RPI GPIO NOT EXIST")


def setV2(i):
    try:
        if i == 1:
            GPIO.output(v2_1, GPIO.HIGH)
            GPIO.output(v2_2, GPIO.LOW)
        elif i == 2:
            GPIO.output(v2_1, GPIO.HIGH)
            GPIO.output(v2_2, GPIO.LOW)
    except:
        print("RPI GPIO NOT EXIST")


def openV3():
    try:
        GPIO.output(v3_open, GPIO.HIGH)
        GPIO.output(v3_close, GPIO.LOW)
    except:
        print("RPI GPIO NOT EXIST")


def closeV3():
    try:
        GPIO.output(v3_open, GPIO.LOW)
        GPIO.output(v3_close, GPIO.HIGH)
    except:
        print("RPI GPIO NOT EXIST")


def openV4():
    try:
        GPIO.output(v4_open, GPIO.HIGH)
        GPIO.output(v4_close, GPIO.LOW)
    except:
        print("RPI GPIO NOT EXIST")


def closeV4():
    try:
        GPIO.output(v4_open, GPIO.LOW)
        GPIO.output(v4_close, GPIO.HIGH)
    except:
        print("RPI GPIO NOT EXIST")


def openV5():
    try:
        GPIO.output(v5_open, GPIO.HIGH)
        GPIO.output(v5_close, GPIO.LOW)
    except:
        print("RPI GPIO NOT EXIST")


def closeV5():
    try:
        GPIO.output(v5_open, GPIO.LOW)
        GPIO.output(v5_close, GPIO.HIGH)
    except:
        print("RPI GPIO NOT EXIST")


def startP1():
    try:
        GPIO.output(p1, GPIO.HIGH)
    except:
        print("RPI GPIO NOT EXIST")


def stopP1():
    try:
        GPIO.output(p1, GPIO.LOW)
    except:
        print("RPI GPIO NOT EXIST")


def startP2():
    try:
        GPIO.output(p2, GPIO.HIGH)
    except:
        print("RPI GPIO NOT EXIST")


def stopP2():
    try:
        GPIO.output(p2, GPIO.LOW)
    except:
        print("RPI GPIO NOT EXIST")


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
        print("RPI GPIO NOT EXISTTT")

    ser.write(b'You shall Turn off H1\r\n')
    waitForResponseAndPrint("Turn off H1")
    waitForResponseAndPrint("turned off H1")

    ser.write(b'You shall Turn off H3\r\n')
    waitForResponseAndPrint("Turn off H3")
    waitForResponseAndPrint("turned off H3")


    temp = ser.readline()
    print ("temp" + temp)
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
    openV1()

    if simulation:
        simHLTliter += 1
        print("SimHLTliter: " + str(simHLTliter))

    if HL1 == 1 or simHLTliter == 10:
        try:
            closeV1()
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

    print ("Awesome data is:")
    print (data)


    x = data.split(b';')

    if float(x[2].split(b':')[1]) < meshTempSP -2:
        return 3
    else:
        return 4


def state4():
    global simHLTliter
    global simMeshLiter
    print("Fill mesh")
    openV3()
    startP2()

    if simulation == True:
        simMeshLiter += 1
        print("Mesh-liter: " + str(simMeshLiter))

    if HL2 == 1 or simMeshLiter == 10:
        if simulation:
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
    if simulation and simHLTliter < 10:
        simHLTliter += 1
        print("Liters in HLT: " + str(simHLTliter))

    if HL1 == 1 or simHLTliter >= 10:
        closeV1()
    return 6


def state6():
    global circulationTempSP
    print("Heating HLT " + str(circulationTempSP) + " degrees")
    global hltTemp
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
    print("The temperature in HLT " + str(meshTempSP) + " is: " + str(hltTemp))
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
        openV4()
        startP1()
        setV2(1)
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

    if (HL3 == 1 or simBoilLiter >= 10):
        stopP1()
    else:
        setV2(2)
        startP1()

        if simulation:
            simBoilLiter += 1
            print ("Boil has " + str(simBoilLiter) + " Liters ")

    if LL2 == 1 or simBoilLiter > 2:

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
    global rinseTimerStart
    global rinseProcessDone
    if simulation:

        if simMeshLiter > 1:
            simMeshLiter -= 1
            print("Remaining simMeshLiter: " + str(simMeshLiter))

    if (LL1 == 0 or simMeshLiter <= 1) and rinseTimerStart == 0.0:
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
    print ("Please open V5")
    return 12


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
