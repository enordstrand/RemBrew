
#include <PID_v1.h>

static const int relayPin1 = 12;
static const int relayPin2 = 11;
static const int TempProbe1 = A2;
static const int TempProbe2 = A4;
static const int windowSize = 5000;

double setpoint1, input1, output1;
double setpoint2, input2, output2;
double kp=30000, ki=0, kd=0;
long now, windowStartTime;
long counter = 0;
double sensorValue1 = 0;
double sensorValue2 = 0;
double meansensorValue1 = 0;
double meansensorValue2 = 0;
double temp1 = 0;
double temp2 = 0;
const int numberOfSamples = 200;
float R1_1;
float R1_2;
const double R2 = 10000;

int samples1[numberOfSamples];
int samples2[numberOfSamples];


PID myPID1(&temp1, &output1, &setpoint1, kp, ki, kd, DIRECT);
PID myPID2(&temp2, &output2, &setpoint2, kp, ki, kd, DIRECT);

void setup() {
    Serial.begin(115200);
    pinMode(relayPin1, OUTPUT);
    pinMode(TempProbe1, INPUT);
    pinMode(relayPin2, OUTPUT);
    pinMode(TempProbe2, INPUT);
    //input1 = analogRead(0);
    myPID1.SetMode(AUTOMATIC);
    myPID1.SetOutputLimits(0, windowSize);
    myPID2.SetMode(AUTOMATIC);
    myPID2.SetOutputLimits(0, windowSize);

    // connect AREF to 3.3V and use that as VCC, less noisy!
    //analogReference(EXTERNAL);

    //initialize the variables we're linked to
    setpoint1 = 20;
    setpoint2 = 20;
}

void loop() {
    uint8_t i;
    float averageAnalogRead_1;
    float averageAnalogRead_2;
//    float R1_1;
//    float temp1;

    // take N samples in a row, with a slight delay
    //Serial.println(analogRead(A3));
    //Serial.println(analogRead(TempProbe1));
    for (i=0; i< numberOfSamples; i++) {
     samples1[i] = analogRead(TempProbe1);
     samples2[i] = analogRead(TempProbe2);
//     delay(10);
    }

    // average all the samples out
    averageAnalogRead_1 = 0;
    averageAnalogRead_2 = 0;
    for (i=0; i< numberOfSamples; i++) {
       averageAnalogRead_1 += samples1[i];
       averageAnalogRead_2 += samples2[i];
    }
    averageAnalogRead_1 /= numberOfSamples;
    averageAnalogRead_2 /= numberOfSamples;

    // convert the value to resistance
    //Serial.print("kake: ");
    //Serial.println(averageAnalogRead_1);
    R1_1 = (10000*(1023-averageAnalogRead_1))/averageAnalogRead_1;
    R1_2 = (10000*(1023-averageAnalogRead_2))/averageAnalogRead_2;

    Serial.println(R1_1);

//     float A = 0.001555166246;
//     float B = 0.0001492204118;
//     float C = 0.0000005397917219;

    float A = 0.001574139714;
    float B = 0.0001721193602;
    float C = 0.0000002569643515;

    temp1 = 1/(A+B*log(R1_1)+C*(log(R1_1))*(log(R1_1))*(log(R1_1)))-273.15;
    temp2 = 1/(A+B*log(R1_2)+C*(log(R1_2))*(log(R1_2))*(log(R1_2)))-273.15;

    doPid();
}

void doPid() {
    myPID1.Compute();
    myPID2.Compute();

    now = millis();
    if (now - windowStartTime > windowSize) {
        windowStartTime += windowSize;
    }


    if ((output1 > now - windowStartTime) && output1 > 100 && temp1 > -1) {
        digitalWrite(relayPin1, HIGH);
        Serial.print("H1 ");
    } else {
        digitalWrite(relayPin1, LOW);
        Serial.print("L1 ");
    }

    Serial.print("T1: ");
    Serial.print(temp1);
    Serial.print(" W1: ");
    Serial.print(output1);

    if ((output2 > now - windowStartTime) && output2 > 100 && temp2 > -1) {
        digitalWrite(relayPin2, HIGH);
        Serial.print("   H2 ");
    } else {
        digitalWrite(relayPin2, LOW);
        //Serial.print("   L2 ");
    }
    //Serial.print("T2: ");
    //Serial.print(temp2);
    //Serial.print(" W2: ");
    //Serial.println(output2);
}