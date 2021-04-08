#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

MPU6050 acele1(0x68);  // CORRESPONDE AL ACELERÓMETRO 1, ABAJO LAS VARIABLES
int16_t ax1, ay1, az1;

MPU6050 acele2(0x69);  // CORRESPONDE AL ACELERÓMETRO 2: para que tome el ID 0x69 conectar el pin AD0 del acelerómetro a 5V. 
int16_t ax2, ay2, az2;

bool measure = false;

#define OUTPUT_BINARY_ACELE1
#define OUTPUT_BINARY_ACELE2

bool blinkState = false;


void setup() {

    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

  
  
  Serial.begin(115200);     //Inicialización de Serial Communication

  acele1.initialize();      //Inicialización de acelerometros
  acele2.initialize();

  Serial.println(acele1.testConnection() ? "_OK_" : "MPU1 FAILED");      //Verificación de conexiones
  acele1.setXAccelOffset(1596);
  acele2.setXAccelOffset(1596);

}



void loop() {



if(measure){

  acele1.getAcceleration(&ax1, &ay1, &az1);
  acele2.getAcceleration(&ax2, &ay2, &az2);

  #ifdef OUTPUT_BINARY_ACELE1
     Serial.write((uint8_t)(az1 >> 8)); Serial.write((uint8_t)(ax1 & 0xFF));
  #endif


  #ifdef OUTPUT_BINARY_ACELE2
     Serial.write((uint8_t)(az2 >> 8)); Serial.write((uint8_t)(az2 & 0xFF));
  #endif

}


//else{
  
//  measure = true;
  
//  }
}    


void serialEvent() {
 
  char inChar = (char)Serial.read();
   
  switch (inChar) {
    case 'r': //run
     
      measure = true;
      break;
      
    case 's': //stop
     
      measure = false;
      break;
 
  }
   
}
