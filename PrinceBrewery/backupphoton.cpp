// This #include statement was automatically added by the Particle IDE.
#include <pid.h>

static const int H1 = D0;
static const int H3 = D1;
static const int T1 = A0;
static const int T2 = A1;
static const int T3 = A2;
static const int windowSize = 5000;
static const float gain = (100 - 0.9)/(3700-75);

double setpoint1, input1, output1;
double setpoint3, input3, output3;
double kp=300, ki=0, kd=0;
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
char HState;
String firstVal, secondVal, thirdVal;

String data;
PID myPID1(&temp1, &output1, &setpoint1, kp, ki, kd, PID::DIRECT);
PID myPID3(&temp3, &output3, &setpoint3, kp, ki, kd, PID::DIRECT);


void setup() {
    Serial.begin(9600);
    pinMode (T3, INPUT);
    pinMode(H1, OUTPUT);
    pinMode(H3, OUTPUT);
    pinMode(H1, OUTPUT);
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
        int tempBucket = 0;
        if (secondVal == "HLT") {
            tempSensor = T1;
        } else if (secondVal == "Boil") {
            tempSensor = T3;
        }
        for(int j = 1 ; j<=200 ;  j++) {  
            int temp = analogRead(tempSensor);
            tempBucket = tempBucket + temp;  
        }
        
        int sp = thirdVal.toInt();
        int tempValue = tempBucket/200;
        if (secondVal == "HLT") {
            temp1 = tempValue * gain;
            
            
            setpoint1 = sp;
        } else if (secondVal == "Boil") {
            temp3 = tempValue * gain;
            setpoint3 = sp;
        }
        
        doPid(secondVal);
    
        
    } else {
       
        //Spark.publish("toRpi","Error from photon");
        //Serial.println(", Error from photon1");
        //delay(1000);
    }
    
    if (data.indexOf("start PID SP;") > 0) {
        
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
        Serial.print('\n');
        //delay(1000);
    }
     
}
