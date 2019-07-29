#include <SPI.h>
#include <PubSubClient.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiAP.h>
#include <ESP8266WiFiGeneric.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266WiFiScan.h>
#include <ESP8266WiFiSTA.h>
#include <ESP8266WiFiType.h>
#include <WiFiClient.h>
#include <WiFiClientSecure.h>
#include <WiFiServer.h>
#include <WiFiUdp.h>
// #include "OLED.h"
#include <Wire.h>

// #define RST_OLED 16

const char* WIFISSID = "LY1688";
const char* PASS = "admin85259297";
const char* MQSERVER = "iot.aishe.org.cn";
const int MQPORT = 1883;
int status = WL_IDLE_STATUS ;
//char MYID[48];

WiFiClient wclient;
PubSubClient mclient(wclient);
long lastMsg = 0;
char msg[50];
char bmsg[32];
int value = 0;
int cc = 0;
//test data bytemsg;
//const char bytemsg[12] = {0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x01,0x02,0x01,0x01,0x01};
uint8_t macarry[6];// = "00000001"; //device id
char macchar[12];
//"8fad12f5d9";
// for buttun/high-low voltage signal
const int s1Pin = 1;
const int s2Pin = 3;
const int s3Pin = 13;
const int s4Pin = 15;

int buttonState = 0;
int prevState = 0;
int signalvalue[4] = {1, 1, 1, 1};
int b1[4] = {1, 1, 1, 1}; 
int b2[4] = {1, 1, 1, 1};
int b3[4] = {1, 1, 1, 1};
int b4[4] = {1, 1, 1, 1};
char sigState[32];  //state of signal in format 1010 alike;
int accumulate = 0;
void setup() {
  //define IO
  pinMode(s1Pin, INPUT);
  pinMode(s2Pin, INPUT);
  pinMode(s3Pin, INPUT);
  pinMode(s4Pin, INPUT);
  int signalvalue[4];
  Wire.begin(0, 2); // define i2c bus in Wire lib;

  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
  //check for shield
  //pinMode(RST_OLED, OUTPUT);
  //digitalWrite(RST_OLED, LOW);   // turn D2 low to reset OLED
  delay(50);
  //digitalWrite(RST_OLED, HIGH);    // while OLED is running, must set D2 in high

  //open serialport
  Serial.begin(9600);
  Serial.println("OLED test!");
  
  WiFi.macAddress(macarry);
  for (int i = 0; i < sizeof(macarry); ++i){
    sprintf(macchar,"%s%02x",macchar,macarry[i]);
  }
  
  delay(1000);
  
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
  int n = WiFi.scanNetworks();
  
  Serial.print("scanned: \n");
  Serial.print(n);
  Serial.print(" wifis \n");

  WiFi.begin(WIFISSID, PASS);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(10000);
//    Serial.print(macchar);
    WiFi.begin(WIFISSID, PASS);
  }
//  myip = WiFi.localIP();
  Serial.println(WiFi.localIP());
  delay(500);
  // con mqtt
  mclient.setServer(MQSERVER,MQPORT);
  
  mclient.setCallback(callback);
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived![");
  Serial.print(topic);
  Serial.print("]:");

  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

}

int filter(int which) {

  int i;
  for (i=0; i<4; i++){
      b4[i] = b3[i];
      b3[i] = b2[i];
      b2[i] = b1[i];
      b1[i] = signalvalue[i];
  }
  
  if (b1[which] + b2[which] + b3[which] > 2) {
    return which+1;
  } else {
    return -99;
  }
  
}

int signalcompare(){
  
  int i;
  for (i =0; i<4; i++) {
    b3[i] = LOW;
    b2[i] = LOW;
    b1[i] = LOW;
  }
  
  for (i = 0; i<4; i++){
    if (signalvalue[i] != b4[i] && signalvalue[i] == HIGH) {
      return i;
      break;
    }
  }
  for (i = 0; i<4; i++){
    b4[i] = signalvalue[i];
    //update b3 for state compare
  }
  return -9;
}

void readSignal(){
    signalvalue[0] = digitalRead(s1Pin);
    signalvalue[1] = digitalRead(s2Pin);
    signalvalue[2] = digitalRead(s3Pin);
    signalvalue[3] = digitalRead(s4Pin);
}

void reconnect() {
  // Loop until we're reconnected
  while (!mclient.connected()) {
    Serial.print("Attempting MQTT connection...\n");
    // Attempt to connect
    if (mclient.connect(macchar, "devuser","devpass")) {
      Serial.println("connected\n");
      // Once connected, publish an announcement...
      mclient.publish("remote", macchar);
      //snprintf(msg, 75, "%s.%s", signalvalue[0], signalvalue[1], signalvalue[2], signalvalue[3]);
      // ... and resubscribe
      //mclient.subscribe("remote");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mclient.state());
      Serial.println(" try again in 5 seconds\n");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  byte error, address;
  int nDevices;   //i2c device addresses

  // scan ddresses
  for (address = 1; address < 127; address ++)
  {
    // The i2c_scanner uses the return value of
    // the Write.endTransmisstion to see if
    // a device did acknowledge to the address.
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    // error = 0; found address;
    // address can be found
    // error = 4; not found
  }

  if (!mclient.connected()) {
    reconnect();
    delay(1500);
  }


  mclient.loop();
  
  //buttonState = digitalRead(s1Pin);
  readSignal();
  buttonState = signalcompare();
  snprintf(msg, 75, "%d%d%d%d", signalvalue[0], signalvalue[1], signalvalue[2], signalvalue[3]);
//  Serial.printf(msg);
  // modification detection;
    //snprintf(msg, 75, "%d%d%d%d\n", signalvalue[0], signalvalue[1], signalvalue[2], signalvalue[3]);
    //Serial.printf(msg);
  if (buttonState < 0) {
    ;
  } else {
    Serial.print(buttonState);
    prevState = buttonState;
    //snprintf (msg, 75, "state change %s", buttonState); 
    //mclient.publish("remote", "trigger");
    //Serial.print("-X-");
    //delay(1);
    snprintf(msg, 75, "%d%d%d%d\n", signalvalue[0], signalvalue[1], signalvalue[2], signalvalue[3]);
    Serial.printf(msg);
  // listen on button state
  if (buttonState < 0) {
    //turn LED on;
//    Serial.print("button high");
//    digitalWrite(ledPin, HIGH);
    delay(5);
    Serial.print("bs<0");
  } else {
    //turn LED off;
//    digitalWrite(ledPin, LOW);
    Serial.print(buttonState);
    readSignal();
    delay(20);
    cc = filter(buttonState);
    Serial.print(cc);
    readSignal();
    cc = filter(buttonState);
    Serial.print(cc);
    delay(80);
    
    readSignal();
    cc = filter(buttonState);
    delay(20);
    readSignal();
    cc = filter(buttonState);
    Serial.print(cc);
    long now = millis();
    if ( cc > 0 ) {
      ++accumulate;
      Serial.print(cc);
      Serial.print("th signals --------------\n");
      snprintf(msg, 75, "%s.%d", macchar, cc);
      //lastMsg = now; //think about reduce this losing risk;
      mclient.publish("dev", msg);
      snprintf(msg, 75, "si=%d", cc);
      delay(300);
    }
    
  }
  }
  long now = millis();
  //interval = 60s
  if (now - lastMsg > 180000) {
    lastMsg = now;
    ++value;
    // kw=hb, str=device_id, ld=time_stamp, str=status 1111
    snprintf(sigState, 32, "%d%d%d%d", signalvalue[0], signalvalue[1], signalvalue[2], signalvalue[3]);
    snprintf (msg, 75, "hb.%s.%ld.%s", macchar, value, sigState);
    Serial.print("heartbeat:");
    Serial.println(msg);
//    if (value % 3 == 0) {
//      bytemsg = ;
//      int imsg[4] = {1,0,2,0};
//    lets make it hex string to avoid 0x00;　　　　
//      //mclient.publish("dev", hexmsg, 32);
//      delay(0);
//    }
    mclient.publish("remote", msg);
    snprintf(msg, 75, "%d%d%d%d\n", signalvalue[0], signalvalue[1], signalvalue[2], signalvalue[3]);
    Serial.printf(msg);
    
  }
}
