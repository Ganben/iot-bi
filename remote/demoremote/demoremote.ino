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
const char* hexmsg = "0000000001";
//"8fad12f5d9";
// for buttun/high-low voltage signal
const int s1Pin = 15;
const int s2Pin = 13;
const int s3Pin = 12;
const int s4Pin = 14;
int buttonState = 0;
int prevState = 0;
int b1 = 0;
int b2 = 0;
int b3 = 0;
int accumulate = 0;
void setup() {
  //define IO
  pinMode(s1Pin, INPUT);
  pinMode(s2Pin, INPUT);
  pinMode(s3Pin, INPUT);
  pinMode(s4Pin, INPUT);
  
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

void reconnect() {
  // Loop until we're reconnected
  while (!mclient.connected()) {
    Serial.print("Attempting MQTT connection...\n");
    display.print("TCP reconn........", 2);
    // Attempt to connect
    if (mclient.connect("ESP8266Client")) {
      Serial.println("connected\n");
      // Once connected, publish an announcement...
      mclient.publish("remote", "hello world");
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
  
  buttonState = digitalRead(s1Pin);
  // modification detection;
  if (prevState == buttonState) {
    ;
  } else {
    display.print("-X-");
    prevState = buttonState;
    //snprintf (msg, 75, "state change %s", buttonState); 
    //display.print("");
    //mclient.publish("remote", "trigger");
    //Serial.print("-X-");
    //delay(1);
  
  // listen on button state
  if (buttonState == HIGH) {
    //turn LED on;
//    Serial.print("button high");
//    digitalWrite(ledPin, HIGH);
    display.print("b=H..");
    delay(5);
  } else {
    //turn LED off;
//    digitalWrite(ledPin, LOW);
    display.print("b=L..");
    delay(30);
    cc = 0;
    b1 = digitalRead(s1Pin);
    if (b1 == LOW){
      ++cc;
    }
    delay(50);
    b2 = digitalRead(s1Pin);
    if (b2 == LOW){
      ++cc;
    }
    delay(50);
    b3 = digitalRead(s1Pin);
    if (b3 == LOW){
      ++cc;
    }
    if ( cc >= 2 ) {
      ++accumulate;
      Serial.print(accumulate);
      Serial.print("th signals ---------------------\n");
      mclient.publish("remote", "-X-");
      display.print("-X SENT-");
      delay(200);
    }
    
  }
  }
  
  long now = millis();
  if (now - lastMsg > 180000) {
    lastMsg = now;
    ++value;
    snprintf (msg, 75, "hb #+%ld min", value*3);
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
  }
}
