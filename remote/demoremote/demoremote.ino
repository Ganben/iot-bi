#include <SPI.h>
#include <PubSubClient.h>
#include <ESP8266WiFi.h>
#include "OLED.h"
#include <Wire.h>

#define RST_OLED 16

const char* WIFISSID = "Xiaomi_8ADD";
const char* PASS = "Blockhouse";
const char* MQSERVER = "192.168.31.122";
const int MQPORT = 1883;
int status = WL_IDLE_STATUS ;
const int MYID = 101;

OLED display(4, 5);
WiFiClient wclient;
PubSubClient mclient(wclient);
long lastMsg = 0;
char msg[50];
char bmsg[32];
int value = 0;
int cc = 0;
//test data bytemsg;
//const char bytemsg[12] = {0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x01,0x02,0x01,0x01,0x01};
const char* hexmsg = "0000000001"; //device id
//"8fad12f5d9";
// for buttun/high-low voltage signal
const int s1Pin = 15;
const int s2Pin = 13;
const int s3Pin = 12;
const int s4Pin = 5;

int buttonState = 0;
int prevState = 0;
int signalvalue[4] = {1, 1, 1, 1};
int b1[4] = {1, 1, 1, 1}; 
int b2[4] = {1, 1, 1, 1};
int b3[4] = {1, 1, 1, 1};
int accumulate = 0;
void setup() {
  //define IO
  pinMode(s1Pin, INPUT);
  pinMode(s2Pin, INPUT);
  pinMode(s3Pin, INPUT);
  pinMode(s4Pin, INPUT);
  int signalvalue[4];
  
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
  //check for shield
  pinMode(RST_OLED, OUTPUT);
  digitalWrite(RST_OLED, LOW);   // turn D2 low to reset OLED
  delay(50);
  digitalWrite(RST_OLED, HIGH);    // while OLED is running, must set D2 in high

  //open serialport
  Serial.begin(9600);
  Serial.println("OLED test!");
  display.begin();
  display.print("test1", 4);
  display.print("Init success", 1);
  delay(1000);
  display.print("Wifi init...", 1);
  WiFi.begin(WIFISSID, PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(10000);
    Serial.print("wifi init...\n");
    display.print("Wifi con..", 1);
//    WiFi.begin(WIFISSID, PASS);
  }
//  myip = WiFi.localIP();
  Serial.println(WiFi.localIP());
  display.print("WiFi connected.", 1);
//  display.print((char)WiFi.localIP(), 3);
  delay(500);
  // con mqtt
//  display.clear
  display.print("TCP init...", 2);
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
  display.print("TCP recv...", 3);
  Serial.println();

}

int filter(int which) {

  int i;
  for (i=0; i<4; i++){
      b3[i] = b2[i];
      b2[i] = b1[i];
      b1[i] = signalvalue[i];
  }
  
  if (b1[which] + b2[which] + b3[which] < 2) {
    return which+1;
  } else {
    return -99;
  }
  
}

int signalcompare(){
  
  int i;
  for (i =0; i<4; i++) {
    //b3[i] = HIGH;
    b2[i] = HIGH;
    b1[i] = HIGH;
  }
  
  for (i = 0; i<4; i++){
    if (signalvalue[i] != b3[i] && signalvalue[i] == LOW) {
      return i;
      break;
    }
  }
  for (i = 0; i<4; i++){
    b3[i] = signalvalue[i];
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
    display.print("TCP reconn........", 2);
    // Attempt to connect
    if (mclient.connect("ESP8266Client")) {
      Serial.println("connected\n");
      // Once connected, publish an announcement...
      mclient.publish("remote", hexmsg);
      // ... and resubscribe
      //mclient.subscribe("remote");
      display.print("TCP connected", 2);
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
  
  if (!mclient.connected()) {
    reconnect();
    delay(1500);
  }
  mclient.loop();
  //display.print("TCP connected.", 2);
  
  //buttonState = digitalRead(s1Pin);
  readSignal();
  buttonState = signalcompare();
  snprintf(msg, 75, "%d%d%d%d", signalvalue[0], signalvalue[1], signalvalue[2], signalvalue[3]);
//  Serial.printf(msg);
  display.print(msg);
  // modification detection;
    //snprintf(msg, 75, "%d%d%d%d\n", signalvalue[0], signalvalue[1], signalvalue[2], signalvalue[3]);
    //Serial.printf(msg);
    //display.print(msg);
  if (buttonState < 0) {
    ;
  } else {
    display.print("***");
    Serial.print(buttonState);
    prevState = buttonState;
    //snprintf (msg, 75, "state change %s", buttonState); 
    //display.print("");
    //mclient.publish("remote", "trigger");
    //Serial.print("-X-");
    //delay(1);
    snprintf(msg, 75, "%d%d%d%d\n", signalvalue[0], signalvalue[1], signalvalue[2], signalvalue[3]);
    Serial.printf(msg);
    display.print(msg);
  // listen on button state
  if (buttonState < 0) {
    //turn LED on;
//    Serial.print("button high");
//    digitalWrite(ledPin, HIGH);
    display.print("b=H..--");
    delay(5);
    Serial.print("bs<0");
  } else {
    //turn LED off;
//    digitalWrite(ledPin, LOW);
    display.print("b=L..--");
    delay(20);
    cc = filter(buttonState);
    Serial.print(cc);
    readSignal();
    cc = filter(buttonState);
    Serial.print(cc);
    delay(80);
    
    readSignal();
    cc = filter(buttonState);
    Serial.print(cc);
    long now = millis();
    if ( cc > 0 ) {
      ++accumulate;
      Serial.print(cc);
      Serial.print("th signals --------------\n");
      snprintf(msg, 75, "%s.%d", hexmsg, cc);
      //lastMsg = now; //think about reduce this losing risk;
      mclient.publish("dev", msg);
      snprintf(msg, 75, "si=%d", cc);
      display.print(msg);
      delay(300);
    }
    
  }
  }
  long now = millis();

  if (now - lastMsg > 30000) {
    lastMsg = now;
    ++value;
    snprintf (msg, 75, "hb.%s.%ld", hexmsg, value);
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
    display.print(msg);
    
  }
}
