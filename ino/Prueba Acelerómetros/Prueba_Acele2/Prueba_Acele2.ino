#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

//MPU6050 acele1(0x68);  // CORRESPONDE AL ACELERÓMETRO 1, ABAJO LAS VARIABLES
//int16_t ax1, ay1, az1;
//int16_t gx1, gy1, gz1;

MPU6050 acele2(0x69);  // CORRESPONDE AL ACELERÓMETRO 2: para que tome el ID 0x69 conectar el pin AD0 del acelerómetro a 5V. 
int16_t ax2, ay2, az2;
int16_t gx2, gy2, gz2;

bool measure = false;

//#define OUTPUT_BINARY_ACELE1
#define OUTPUT_BINARY_ACELE2

bool blinkState = false;



//////   1: ACTIVAR TODO LO DE ACÁ ABAJO PARA VER LA RAW DATA EN EL SERIAL
//////   Se presenta en forma de tabla
//
void printTab()
{
   Serial.print(F("\t"));
}
 
void printRAW()
{
//   Serial.print(F("a1[x y z] g1[x y z]:t"));
//   Serial.print(ax1); printTab();
//   Serial.print(ay1); printTab();
//   Serial.print(az1); printTab();
//   Serial.print(gx1); printTab();
//   Serial.print(gy1); printTab();
//   Serial.println(gz1);

   Serial.print(F("a2[x y z] g2[x y z]:t"));
   Serial.print(ax2); printTab();
   Serial.print(ay2); printTab();
   Serial.print(az2); printTab();
   Serial.print(gx2); printTab();
   Serial.print(gy2); printTab();
   Serial.println(gz2);
//   
}   // FIN DE 1:



void setup() {

    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

  
  //Wire.begin();
  Serial.begin(115200);     //Inicialización de Serial Communication

  //acele1.initialize();      //Inicialización de acelerometros
  acele2.initialize();

  //Serial.println(acele1.testConnection() ? "MPU1 OK" : "MPU1 FAILED");      //Verificación de conexiones
  Serial.println(acele2.testConnection() ? "MPU2 OK" : "MPU2 FAILED");
  //acele1.setXAccelOffset(1596);
  acele2.setXAccelOffset(1596);

}



void loop() {
//acele1.getMotion6(&ax1, &ay1, &az1, &gx1, &gy1, &gz1);  //Obtención de datos de cada aceler.
acele2.getMotion6(&ax2, &ay2, &az2, &gx2, &gy2, &gz2);


////////   2: HABILITAR ESTO JUNTO CON 1: PARA VER EL RAW. (ANDANDO OK AL 14.3.20)
//
   printRAW();
   
   delay(150);   // Cada cuánto tiempo imprime valores

}    // FIN DE 2: LOOP RAW





void serialEvent() {
 
  char inChar = (char)Serial.read();
   
  switch (inChar) {
    case 'r': //run
     
      measure = true;
      break;
      
    case 's': //stop
     
      measure = false;
      break;
 
     case 'v':
      
       measure = false;
       break; 
  }
   
}
