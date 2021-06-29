int IR_IN = 12;
int led = 13;
int Up = 0;

//Global Variables
unsigned long UpTime=0;
unsigned long DownTime=0;
unsigned long DeltaTime=0;
unsigned long offset_start=0;
unsigned long offset_end=0;
unsigned long offset_delta=0;
float V_hor[3] = {0.0, 0.0, 0.0};
float V_ver[3] = {0.0, 0.0, 0.0};
float U[3] = {0.0, 0.0, 0.0};
float base[3] = {5.0, 0.0, 2.0};
float current_pos[3] = {0.0, 0.0, 0.0};


//Function prototypes
float position_calculation(unsigned long);
void pulse_classifier(unsigned long, char*, char*);
void angle_calculation(unsigned long, char, float*, float*);

void setup() {
  // put your setup code here, to run once:
  pinMode(IR_IN, INPUT);
  pinMode(led, OUTPUT);
  Serial.begin(38400);
}

void loop() {
  // put your main code here, to run repeatedly:
  char pulse ='n';
  char angle ='n';
  //Serial.println(digitalRead(IR_IN));
  
  if (!digitalRead(IR_IN) && (Up==0)) {
        UpTime = micros();
        //Serial.println("High");
        //digitalWrite(led, HIGH);
        Up=1;
      }
    
  else if (digitalRead(IR_IN) && (Up==1)){ 
         DownTime = micros();
         DeltaTime= DownTime - UpTime;
         //Serial.println("Low");
         //Serial.println("DeltaTime:");
         //Serial.println(DeltaTime);
         
         ///offset calculation///
         pulse_classifier(DeltaTime, &pulse, &angle);
         //Serial.println("pulse_classifier:");
         //Serial.println(pulse);
         
         if (pulse == 's'){
             offset_start = micros();
             //Serial.println("Sync:");
             //Serial.println(DeltaTime);
             
         }else if ((pulse == 'p') && (offset_start > 0)){
             offset_end = micros();
             offset_delta = (offset_end - offset_start);//- DeltaTime;  //substracting deltatime to remove pulse width
             offset_start=0;

             ///Do position calculation
             if ((offset_delta > 0) && (offset_delta <= (8333-104-DeltaTime))){
                   Serial.println("Offset:");
                   Serial.println(offset_delta); 
            
                   //Returns V_hor, V_ver in radiants (vector)
                   angle_calculation(offset_delta, angle, V_hor, V_ver);  
                  
                   //Cross product of V_hor × V_ver
                   //U be perpendicular to both V_hor and V_ver
                   U[0] = V_hor[1] * V_ver[2] - V_hor[2] * V_ver[1];
                   U[1] = V_hor[2] * V_ver[0] - V_hor[0] * V_ver[2];
                   U[2] = V_hor[0] * V_ver[1] - V_hor[1] * V_ver[0];
            
                   //scaler multiplication and calculate current position
                   for (int i=0; i<3; i++){
                        U[i] = U[i] * 1.5; //1.5 is a random value
                        current_pos[i] = base[i] + U[i];      
                   }
                    
                   Serial.println("Current position:");
                   Serial.println(current_pos[0]);
                   Serial.println(current_pos[2]);
                           
             }else{
                Serial.println("Error offset value");
                //Serial.println(offset_delta);
             }  
         }
         digitalWrite(led, LOW);
         Up=0;
      }
  ////unsigned long peTime = micros();
  //Serial.println("loop time");
  //Serial.println(peTime - psTime);
}

//Classify the pulses and process it.
void pulse_classifier(unsigned long tm_delta, char* pulse, char* angle){
      unsigned int sync_max = 135; //us
      unsigned int sync_low = 104; //us
      unsigned int sweep_max = 55; //us
      
      if (((tm_delta >=sync_low) && (tm_delta < 110))||((tm_delta >= 120) && (tm_delta < 130))){
        *pulse = 's';
        *angle = 'h';
      
      } else if (((tm_delta >=110) && (tm_delta < 120))||((tm_delta >= 130) && (tm_delta < sync_max))){
        *pulse = 's';
        *angle = 'v';
        
      }else if(tm_delta <= sweep_max){
        *pulse = 'p';
      }
  }


void angle_calculation(unsigned long offset_delta, char angle, float* V_hor, float* V_ver){
  //<time offset in µs> ; <central time offset = 4000> ; <cycle period = 8333>
  float sweep_angle = (offset_delta - 4000) * PI / 8333;
  
  if (angle == 'h'){
    V_hor[0] = 0.0;
    V_hor[1] = cos(sweep_angle);
    V_hor[2] = sin(sweep_angle);
     
  } else if (angle == 'v'){
    V_ver[0] = cos(sweep_angle);
    V_ver[1] = 0.0;
    V_ver[2] = -sin(sweep_angle);
    
  } 
}