int IR_IN = 12;
int led = 13;

//Global Variables
unsigned long UpTime=0;
unsigned long DownTime=0;
unsigned long pulse_len=0;
unsigned long offset_start=0;
unsigned long offset_end=0;
unsigned long sweep_offset=0;
float dist_from_origin = 0.0 ;
float pos_x = 0.0 ;
float pos_y = 0.0;
int v_sweep_count = 0;
int h_sweep_count = 0;
bool syncpulse = false;
char sweep_angle = 'n';
int sweep_ttl = 3;
int Up = 0;

//Function prototypes
void pulse_classifier(unsigned long, char*, char*);
void angle_calculation(unsigned long, float*);

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
  
  if (digitalRead(IR_IN) && (Up==0)) {
        UpTime = micros();
        sweep_offset = UpTime - DownTime;
        Up=1;
      }
    
  else if (digitalRead(IR_IN) && (Up==1)){ 
        DownTime =  micros();
        pulse_len = DownTime - UpTime;  //pulse length

        pulse_classifier(pulse_len,&pulse, &angle);

        if (pulse == 's'){
            syncpulse = true;
            sweep_angle = angle;
             
        }else if ((pulse == 'p') && (syncpulse == true)){ //this condition makes sure, laser is captured after sync pulse
            syncpulse = false;
            sweep_offset = sweep_offset - pulse_len;

            if ((sweep_offset > 0) && (sweep_offset <= (8333-104))){

                angle_calculation(sweep_offset, &dist_from_origin); 

                //In below line we are assuming horizontal sweep covers X axis and vertical for Y axis
                //based on lighthouse orientation, it can change
  
                if (sweep_angle == 'h'){
                      pos_x = dist_from_origin;
                      v_sweep_count +=1;
                  }
  
                else if (sweep_angle == 'v'){
                      pos_y = dist_from_origin;
                      h_sweep_count +=1;
                  }

                if (v_sweep_count > 0 && h_sweep_count > 0 && v_sweep_count < sweep_ttl && h_sweep_count < sweep_ttl){
                    //do the robot control comes here
                    Serial.println(pos_x, pos_y);
                    
                    v_sweep_count = 0;
                    h_sweep_count = 0;

                  
                  }
                    

                else if(v_sweep_count >=sweep_ttl or h_sweep_count >=sweep_ttl){
                    Serial.println("Invalid measurement");
                    v_sweep_count = 0;
                    h_sweep_count = 0;
                  }    
              
            }
          
        }
    }
}

//Classify the pulses and process it.
void pulse_classifier(unsigned long tm_delta, char* pulse, char* angle){
      unsigned int sync_max = 135; //us
      unsigned int sync_low = 104; //us
      unsigned int sweep_max = 10; //us
      
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

// Do pose estimation; calculate distance from origin
void angle_calculation(unsigned long offset_delta, float* distance){  

  float omega = PI/(8.33* pow(10,-3)); //rad/sec : laser drum angular velocity
  float height = 2.4; // lighthouse height in meters
  *distance = 0.0;
  
  float sweep_angle = omega * (offset_delta * pow(10, -6)); // units in rad
  float angle_degree = sweep_angle * 57296/1000; //convert rad to degree
  
  if (angle_degree < 90){
       *distance = height/tan(sweep_angle); //pass angle in radians
  }

  else if (angle_degree > 90){
      *distance = height * tan((PI/2) - sweep_angle) ;
  }    
   
}
