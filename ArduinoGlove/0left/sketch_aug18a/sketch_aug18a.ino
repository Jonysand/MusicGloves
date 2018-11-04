#include <SoftwareSerial.h>

SoftwareSerial mySerial(10,11);//RX,TX
int f0,f1,f2,f3,f4;
int hand = 0;//left hand
int head;// 0 ->ip 1->imformation
int id;
int ff0=0;
int ff1=0;
int ff2=0;
int ff3=0;
int ff4=0;
int result;


void setup() {
  Serial.begin(115200);
  while(!Serial){
    };
  Serial.println("Hello There!");
  head = 0;
  id = 0;
 
  head = 1;
}  
 
void loop() {
  int pressure0=analogRead(A0);
  int pressure1=analogRead(A1);
  int pressure2=analogRead(A2);
  int pressure3=analogRead(A3);
  int pressure4=analogRead(A4);
  if(pressure4>940)
    f4=0;
   else
    f4=1;
  if(pressure3>940)
    f3=0;
   else
    f3=1;
  if(pressure2>940)
    f2=0;
   else
    f2=1;
  if(pressure1>940)
    f1=0;
   else
    f1=1;
  if(pressure0>940)
    f0=0;
   else
    f0=1;
  if(f0!=ff0||f1!=ff1||f2!=ff2||f3!=ff3||f4!=ff4){
  ff0=f0;
  ff1=f1;
  ff2=f2;
  ff3=f3;
  ff4=f4;
  delay(50);

  /*数据格式为一位左右手信息+手指按压信息*/
  Serial.print(head);
  Serial.print(id);
  Serial.print(hand);
  Serial.print(ff0);
  Serial.print(ff1);
  Serial.print(ff2);
  Serial.print(ff4);
  Serial.print(ff3);}
  //if (mySerial.available()) {
    //Serial.write(mySerial.read());
  //}
  //if (Serial.available()) {
    //mySerial.write(Serial.read());
 //}
}
