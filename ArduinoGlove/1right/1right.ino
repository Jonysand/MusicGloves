#include <SoftwareSerial.h>

SoftwareSerial mySerial(10,11);//RX,TX
int f0,f1,f2,f3,f4;
int hand = 1;//right hand
int head;// 0 ->ip 1->imformation
int id=1;
int ff0=0;
int ff1=0;
int ff2=0;
int ff3=0;
int ff4=0;
int result;


void setup() {
  //Serial.begin(115200);
  //while(!Serial){
    //};
  //Serial.println("Hello There!");
  mySerial.begin(115200);
  delay(5000);
  mySerial.println("AT+CWMODE=3");
  delay(5000);
  mySerial.flush();
  mySerial.println("AT+RST");
  delay(5000);
  mySerial.flush();
  mySerial.println("AT+CWJAP=\"TP-LINK_950E52\",\"\"");
  delay(5000);
  mySerial.flush();
  mySerial.println("AT+CIPSTART=\"TCP\",\"192.168.1.101\",10000");
  delay(5000);
  mySerial.flush();
  mySerial.println("AT+CIPSEND=2");
  delay(50);
  head = 0;
  mySerial.print(head);
  mySerial.print(id);
  head = 1;
}  
 
void loop() {
  delay(30);
  int pressure0=analogRead(A0);
  int pressure1=analogRead(A1);
  int pressure2=analogRead(A2);
  int pressure3=analogRead(A3);
  int pressure4=analogRead(A4);
  if(pressure4>700)
    f4=0;
   else
    f4=1;
  if(pressure3>700)
    f3=0;
   else
    f3=1;
  if(pressure2>700)
    f2=0;
   else
    f2=1;
  if(pressure1>700)
    f1=0;
   else
    f1=1;
  if(pressure0>700)
    f0=0;
   else
    f0=1;
  if(f0!=ff0||f1!=ff1||f2!=ff2||f3!=ff3||f4!=ff4){
  ff0=f0;
  ff1=f1;
  ff2=f2;
  ff3=f3;
  ff4=f4;
  mySerial.println("AT+CIPSEND=8");
  delay(30);

  /*数据格式为一位左右手信息+手指按压信息*/
  mySerial.print(head);
  mySerial.print(id);
  mySerial.print(hand);
  mySerial.print(ff0);
  mySerial.print(ff1);
  mySerial.print(ff2);
  mySerial.print(ff3);
  mySerial.print(ff4);}
  //if (mySerial.available()) {
    //Serial.write(mySerial.read());
  //}
  //if (Serial.available()) {
    //mySerial.write(Serial.read());
 //}
}
