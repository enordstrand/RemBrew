 // This #include statement was automatically added by the Particle IDE.
#include <pid.h>

static const int H1 = D0;
static const int H3 = D2;
static const int T1 = A1;
static const int T2 = A0;
static const int T3 = A2;
static const int HL1 = A5;
static const int HL3 = A3;
static const int windowSize = 5000;
static const float gain = (100 - 0.9)/(3700-75);

double setpoint1, input1, output1;
double setpoint3, input3, output3;
double kp=1700, ki=0, kd=0;
long now, windowStartTime;
long counter = 0;
double sensorValue1 = 0;
double sensorValue2 = 0;
double sensorValue3 = 0;
double meansensorValue1 = 0;
double meansensorValue2 = 0;
double meansensorValue3 = 0;
double temp1 = 0;
double temp2 = 0;
double temp3 = 0;
double highLevel = 0;
char HState;
String firstVal, secondVal, thirdVal;

String data;
PID myPID1(&temp1, &output1, &setpoint1, kp, ki, kd, PID::DIRECT);
PID myPID3(&temp3, &output3, &setpoint3, kp, ki, kd, PID::DIRECT);


void setup() {
    Serial.begin(9600);
    pinMode (T1, INPUT);
    pinMode (T3, INPUT);
    pinMode (HL1, INPUT);
    pinMode (HL3, INPUT);
    pinMode(H1, OUTPUT);
    pinMode(H3, OUTPUT);
    myPID1.SetMode(PID::AUTOMATIC);
    myPID1.SetOutputLimits(0, windowSize);
    myPID3.SetMode(PID::AUTOMATIC);
    myPID3.SetOutputLimits(0, windowSize);
    digitalWrite(H1, LOW);
    digitalWrite(H3, LOW);
}
void loop() {
    bool dataReceived = false;
    if (Serial.available() > 0) {
        data = Serial.readStringUntil('\n');
        Serial.print("RPi sent me(photon): ");
        Serial.print(data);
        Serial.print('\n');
        dataReceived = true;


    }

    if (data.indexOf("Turn off H1") > 0 && dataReceived) {
        digitalWrite(H1, LOW);
        Serial.println("photon turned off H1");
        //delay(1000);

    } else if (data.indexOf("Turn off H3") > 0 && dataReceived) {
        digitalWrite(H3, LOW);
        Serial.println("photon turned off H3");
        //delay(1000);
    } else if (data.indexOf("Give HL") > 0 && dataReceived) {
        int manometer;
        int highLevelBucket = 0;
        String manometerId;
        if (data.indexOf("HL1") > 0) {
            manometer = HL1;
            manometerId = "HL1";
        } else if (data.indexOf("HL3") > 0) {
            manometer = HL3;
            manometerId = "HL3";
        } else {
            Serial.println("Syntax Error HL");
        }

        for(int j = 1 ; j<=30000 ;  j++) {
            int highLevelTemp = analogRead(manometer);
            highLevelBucket = highLevelBucket + highLevelTemp;
        }

        int highLevelValue = highLevelBucket/30000;
        highLevel = highLevelValue; // Convert this value to liter
        Serial.println("photon gave " + manometerId + ":" + String(highLevel));

    } else if (data.indexOf("start PID SP;") > 0 && dataReceived) {
        //int tempBucket = 0;
        //String firstVal, secondVal, thirdVal;

        for (int i = 0; i < data.length(); i++) {
          if (data.substring(i, i+1) == ";") {
            firstVal = data.substring(0, i);
            for (int j = i+1; j < data.length(); j++) {
                if (data.substring(j,j+1) == ";") {
                    secondVal = data.substring(i+1, j);
                    thirdVal = data.substring(j+1);
                    break;
                }
            }

            break;
          }
        }

        int tempSensor;
        //int manometer;
        int tempBucket = 0;
        //int highLevelBucket = 0;
        if (secondVal == "HLT") {
            tempSensor = T1;
            //manometer = HL1;
        } else if (secondVal == "Boil") {
            tempSensor = T3;
            //manometer = HL3;
        }
        for(int j = 1 ; j<=10000 ;  j++) {
            int temperatureTemp = analogRead(tempSensor);
            //int highLevelTemp = analogRead(manometer);
            tempBucket = tempBucket + temperatureTemp;
            //highLevelBucket = highLevelBucket + highLevelTemp;
        }

        int sp = thirdVal.toInt();
        int tempValue = tempBucket/10000;
        //int highLevelValue = highLevelBucket/200;
        if (secondVal == "HLT") {
            temp1 = tempValue * gain;
            //highLevel1 = highLevelValue; // Convert this value to liter


            setpoint1 = sp;
        } else if (secondVal == "Boil") {
            temp3 = tempValue * gain;
            //highLevel3 = highLevelValue; // Convert this value to liter
            setpoint3 = sp;
        }

        doPid(secondVal);


    } else {

        Spark.publish("toRpi","Error from photon");
        //Serial.println(", Error from photon1");
        //delay(1000);
    }
}

void doPid(String secondVal) {
    double windowOpening;
    double tempVal;
    if (secondVal == "HLT") {
        myPID1.Compute();
        windowOpening = output1;
        tempVal = temp1;
    } else if (secondVal == "Boil") {
        myPID3.Compute();
        windowOpening = output3;
        tempVal = temp3;
    }
    now = millis();
    if (now - windowStartTime > windowSize) {
        windowStartTime = now;
    }

    if (secondVal == "HLT") {
        if ((windowOpening > now - windowStartTime) && windowOpening > 100 && tempVal > -1) {
        digitalWrite(H1, HIGH);
        HState = 'H';
        } else {
            digitalWrite(H1, LOW);
            HState = 'L';
        }
        Serial.print("PID FB;HLT;T1:" + String(temp1) + ";W1:" + String(output1) + ";H1State:" + String(HState));
        //Serial.print("PID FB;HLT;T1:" + String(temp1) + ";W1:" + String(output1) + ";H1State:" + String(HState) + ";HL1:" + String(highLevel1));
        Serial.print('\n');
        //delay(1000);

    } else if (secondVal == "Boil") {
        //digitalWrite(H3, LOW);
        if ((windowOpening > now - windowStartTime) && windowOpening > 100 && tempVal > -1) {
            digitalWrite(H3, HIGH);
            HState = 'H';
        } else {
            //digitalWrite(H3, LOW);
            HState = 'L';
        }
        Serial.print("PID FB;Boil;T3:" + String(temp3) + ";W3:" + String(output3) + ";H3State:" + String(HState));
        //Serial.print("PID FB;Boil;T3:" + String(temp3) + ";W3:" + String(output3) + ";H3State:" + String(HState) + ";HL3:" + String(highLevel3));
        Serial.print('\n');
        //delay(1000);
    }

}
