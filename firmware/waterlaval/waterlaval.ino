#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <WiFiClient.h>

#define PIN1 23//pump1
#define PIN2 22//pump2
#define PIN3 21//reraly11
#define PIN4 19//reraly12

String SREVERNAME = "http://59a6-184-22-181-23.ngrok.io";
//String SREVERNAME2 = "http://398e-158-108-225-190.ngrok.io/man_pump/<potnumber>";

const char* ssid = "com_x";
const char* password = "wwwcomxx111";

void setup() {
  Serial.begin(115200);
  pinMode(PIN3,OUTPUT);
  pinMode(PIN4,OUTPUT);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  
  Serial.println("Connected to the WiFi network");
}


void loop() {
  WiFiClient wificlient;
  int PIN_L=digitalRead(PIN1);
  int PIN_R=digitalRead(PIN2);
  Serial.println("working");
  if ((WiFi.status() == WL_CONNECTED)) { //Check the current connection status
    String strA = String(PIN_L);
    String strB= String(PIN_R);
    HTTPClient http;
    String hlink = SREVERNAME;
    http.begin(wificlient, SREVERNAME+"/pump"); //Specisqfy the URL
    http.addHeader("Content-Type", "application/json");
    String wrd = "{\"data\": [" + strA + "," + strB + "]}";
    Serial.println(wrd);
    int httpCode = http.POST(wrd);                                        //Make the request
    if (httpCode > 0) { //Check for the returning code
        Serial.println("Success");
        DynamicJsonDocument doc(2048);
        String payload = http.getString();
        Serial.println(httpCode);
        Serial.println(payload);
        deserializeJson(doc, payload);
        int water_1 = doc["Water"][0];
        int water_2 = doc["Water"][1];
        int Manual_1 = doc["Manual"][0];
        int Manual_2 = doc["Manual"][1];
        int Currenthumid_1 = doc["Currenthumid"][0];
        int Currenthumid_2 = doc["Currenthumid"][1];
        int Settinghumid_1 = doc["Settinghumid"][0];
        int Settinghumid_2 = doc["Settinghumid"][1];
        Serial.println("//////");
        Serial.println(water_1);
        Serial.println(Manual_1);
        Serial.println(water_2);
        Serial.println(Manual_2);
        if(water_1==1){
          if(Manual_1==1){
              digitalWrite(PIN3,HIGH);
            }
          else if(Currenthumid_1<Settinghumid_1){
              digitalWrite(PIN3,HIGH);
            }
          else{
              digitalWrite(PIN3,LOW);
            }
          }else{
              digitalWrite(PIN3,LOW);
            }
        if(water_2==1){
          if(Manual_2==1){
              digitalWrite(PIN4,HIGH);
            }
          else if(Currenthumid_2<Settinghumid_2){
              digitalWrite(PIN4,HIGH);
            }
          else{
              digitalWrite(PIN4,LOW);
            }
          }else{
              digitalWrite(PIN4,LOW);
            }
      }
    else {
      Serial.println("Error on HTTP request");
    }
    http.end(); //Free the resources
  }
  

  delay(10000);
}
