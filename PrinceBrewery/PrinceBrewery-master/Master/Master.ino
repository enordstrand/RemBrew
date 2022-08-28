const int v1 = 0;
const int v2 = 1;
const int v3 = 2;
const int v4 = 3;
const int v5 = 4;

const int p1 = 5;
const int p2 = 6;

const int h1 = 7;
const int h2 = 8;

const bool hL1 = 9;
const bool hL2 = 10;
const bool hL3 = 11;
const bool lL1 = 12;
const bool lL2 = 13;

const int t1 = A0;
const int t2 = A1;
const int t3 = A2;

int state = 1;
void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  
  pinMode(v1, OUTPUT);
  pinMode(v2, OUTPUT);
  pinMode(v3, OUTPUT);
  pinMode(v4, OUTPUT);
  pinMode(v5, OUTPUT);
  pinMode(p1, OUTPUT);
  pinMode(p2, OUTPUT);
  pinMode(h1, OUTPUT);
  pinMode(h2, OUTPUT);
  
  pinMode(hL1, INPUT);
  pinMode(hL2, INPUT);
  pinMode(hL3, INPUT);
  pinMode(lL1, INPUT);
  pinMode(lL2, INPUT);
  pinMode(t1,  INPUT);
  pinMode(t2,  INPUT);
  pinMode(t3,  INPUT);
}

void loop() {
  switch (state) {
    case 1:    
      initialSetup();
      break;
      
    case 2:    
      fillHltStart();
      break;
      
    case 3:   
      initialHeatinigForMeshing();
      break;
      
    case 4:   
      fillMesh();
      break;
   
    case 5:    
      fillHltForCirculation();
      break;
      
    case 6:    
      heatingHltForCirculation();
      break;
      
    case 7:   
      executeMeshing();
      break;
      
    case 8:  
      circulation();
      break;
     
    case 9:    
      fillBoilAndHeat();
      break;
       
    case 10:  
      rinse();
      break;
      
    case 11:    
      boil();
      break;
      
    case 12:  
      fillYeastBucket();
      break;
      
    case 100:
      Serial.println("Finish");
      delay(10000);
      break;
  }
  delay(1);       
}

void initialSetup() {
  Serial.println("setup. Close All Valves and Pumps");
  digitalWrite(v1, LOW);   
  delay(20000);
  digitalWrite(v2, LOW);
  delay(20000);
  digitalWrite(v3, LOW);
  delay(20000);
  digitalWrite(v4, LOW);
  delay(20000);
  digitalWrite(v5, LOW);
  delay(20000);
  
  digitalWrite(p1, LOW);
  delay(1000);
  digitalWrite(p2, LOW);
  delay(1000);

  digitalWrite(h1, LOW);
  delay(1000);
  digitalWrite(h2, LOW);
  delay(1000);
  
  
  state = 2;
}

void fillHltStart() {
  Serial.println("Fill HLT Start");
  digitalWrite(v1, HIGH);
  if ( hL1 == true ) {
    digitalWrite(v1, LOW);
    delay(20000);         
    state = 3;
  }
}

void initialHeatinigForMeshing() {
  Serial.println("Initial Heating");
  digitalWrite(h1, HIGH);
  int t1Value = analogRead(t1);
  int t1Temperature = t1Value * 42;  // use mapping
  if (t1Temperature >= 67) {
    //PID 67 degree regulator
    state = 4;
  }
  
}

void fillMesh() {
  Serial.println("Fill Mesh");
  digitalWrite(v3, HIGH);
  delay(20000);             //Only run once 
  digitalWrite(p2, HIGH);
  if (hL2 == true) {
    digitalWrite(p2, LOW);
    digitalWrite(v3, LOW);
  }
  state = 5;
}

void fillHltForCirculation() {
  Serial.println("Fill HLT Ciculation");
  digitalWrite(v1, HIGH);
  if (hL1 == true) {
    digitalWrite(v1, LOW);
  }
  state = 6;
}

void heatingHltForCirculation() {
  Serial.println("Heating For Circulation");
  state = 7;
}

void executeMeshing() {
  Serial.println("Execute Meshinig");
  state = 8;
}

void circulation() {
  Serial.println("Circulation");
  state = 9;
}

void fillBoilAndHeat() {
  Serial.println("Fill Boil and Heat");
  state = 10;
}

void rinse() {
  Serial.println("Rinse");
  state = 11;
}

void boil() {
  
  Serial.println("Boil");
  state = 12;
}

void fillYeastBucket() {
  Serial.println("Fill Yeast Bucket");
  state = 100;
}













  
