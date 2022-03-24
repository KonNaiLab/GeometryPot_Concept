#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>


#define PIN1 D1 //g1
#define PIN2 D2 //g2

String SREVERNAME = "http://61c3-184-22-181-208.ngrok.io/other";

const char* ssid = "com_x";
const char* password = "wwwcomxx111";

void setup() {
  Serial.begin(115200); // set up serial port for 9600 baud (speed)
  //delay(500); // wait for display to boot up
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
}
/*
void setup() {
  Serial.begin(115200); // set up serial port for 9600 baud (speed)
    delay(1000);
}
*/
void loop() {
  
  WiFiClient wificlient;
  //int PIN_=digitalRead(PIN1);
  int PIN_L=map(PIN1, 0, 1023, 0, 100);
  //int PIN_R=digitalRead(PIN2);
  int PIN_R=map(PIN2, 0, 1023, 0, 100);
  Serial.println("working");


  if ((WiFi.status() == WL_CONNECTED)) { //Check the current connection status
    String strA = String(PIN_L);
    String strB= String(PIN_R);
    HTTPClient http;
    String hlink = SREVERNAME;
    http.begin(wificlient, SREVERNAME); //Specisqfy the URL
    http.addHeader("Content-Type", "application/json");
    String wrd = "{\"data\": [" + strA + "," + strB + "]}";
    
    Serial.println(wrd);
    int httpCode = http.POST(wrd);//Make the request
    if (httpCode > 0) { //Check for the returning code
        Serial.println("Success");
        String payload = http.getString();
        Serial.println(httpCode);
        Serial.println(payload);
    }
    http.end(); //Free the resources
  }
  /*
  int sensorValue;
  sensorValue = analogRead(PIN1);
  sensorValue = map(sensorValue, 0, 1023, 0, 100);
  sensorValue=100-(sensorValue/10);
  Serial.println("Analog Value : ");
  
  Serial.println(sensorValue);
  
  delay(500); //wait for half a second, so it is easier to read
  
  delay(10000);
  */
  delay(10000);
}
