int IR_IN = 12;
int led = 13;
int Up = 0;

unsigned long UpTime=0;
unsigned long DownTime=0;
unsigned long DeltaTime=0;
unsigned long offset_delta =0;


void setup() {
  // put your setup code here, to run once:
  pinMode(IR_IN, INPUT);
  pinMode(led, OUTPUT);
  Serial.begin(38400);
  //digitalWrite(led, HIGH);
}

void loop() {
  //Serial.println(digitalRead(IR_IN));
  // put your main code here, to run repeatedly:
  //UpTime=0;
  //DownTime=0;
  //DeltaTime=0;
  if (!digitalRead(IR_IN) && (Up==0)) {
        UpTime = micros();
        offset_delta = UpTime - DownTime;
        Serial.println("offset");
        Serial.println(offset_delta);
        Serial.println("High");
        digitalWrite(led, HIGH);
        Up=1;
      }
    //digitalWrite(led, LOW);   // LED on  
    //delay(500);                  // Slow blink
  else if (digitalRead(IR_IN) && (Up==1)){ 
         DownTime = micros();
         DeltaTime= DownTime - UpTime;
         Serial.println("Low");
         digitalWrite(led, LOW);
         Up=0;
         Serial.println("Delta:");
         Serial.println(DeltaTime);
      }
         //digitalWrite(led, HIGH);   // LED off
         //Serial.println("Low");
}