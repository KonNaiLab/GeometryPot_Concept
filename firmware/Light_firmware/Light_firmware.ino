#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>



#define LED_A D1
#define LED_B D2

String servername = "http://1e3b-2001-fb1-b9-3a35-1dcd-6e44-bf48-1939.ngrok.io/light";

int digitalReadOutputPin(uint8_t pin)
{
  uint8_t bit = digitalPinToBitMask(pin);
  uint8_t port = digitalPinToPort(pin);
  if (port == NOT_A_PIN) 
    return LOW;

  return (*portOutputRegister(port) & bit) ? HIGH : LOW;
}

void setup() {
  // put your setup code here, to run once:
  WiFiClient wificlient;
  pinMode(LED_A,OUTPUT);
  pinMode(LED_B,OUTPUT);
  //digitalWrite(LED, LOW);
  Serial.begin(115200);
  WiFi.begin("Komna", "0818723669");
  while (WiFi.status() != WL_CONNECTED) {
 
    delay(1000);
    Serial.println("Connecting..");
 
  }
  Serial.println("Connected to WiFi Network");
}

void loop() {
  // put your main code here, to run repeatedly:
  WiFiClient wificlient;
  pinMode(LED_A,OUTPUT);
  pinMode(LED_B,OUTPUT);
  int state_A = digitalReadOutputPin(LED_A);
  int state_B = digitalReadOutputPin(LED_B);
  Serial.println("working");
  Serial.println(state_A);
  Serial.println(state_B);
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
    String strA = String(state_A);
    String strB= String(state_B);
    HTTPClient https;  //Declare an object of class HTTPClient
    String hlink = servername;
    https.begin(wificlient,"http://1e3b-2001-fb1-b9-3a35-1dcd-6e44-bf48-1939.ngrok.io/light"); //Specify request destination
    https.addHeader("Content-Type", "application/json");
    String wrd = "{\"data\": [" + strA + "," + strB + "]}";
    Serial.println(wrd);
    int httpCode = https.POST(wrd); //Send the request
 
    if (httpCode > 0) { //Check the returning code
      Serial.println("Success");
      DynamicJsonDocument doc(2048);
      String payload = https.getString();   //Get the request response payload
      Serial.println(payload); //Print the response payload
      deserializeJson(doc, payload);
      float ctim = doc["Curenttime"];
      Serial.println(ctim);
      //float stim_1[2] = doc["Settingtime"][0];
      //float stim_2[2] = doc["Settingtime"][1];
      float stim_1_s = doc["Settingtime"][0][0];
      float stim_1_e = doc["Settingtime"][0][1];
      float stim_2_s = doc["Settingtime"][1][0];
      float stim_2_e = doc["Settingtime"][1][1];
      Serial.println(stim_1_s);
      //Serial.println(stim_2);
      if((stim_1_s <= ctim)&&(stim_1_e >= ctim)){
        digitalWrite(LED_A, HIGH);
      }
      else{
        digitalWrite(LED_A, LOW);
      }
      if((stim_2_s <= ctim)&&(stim_2_e >= ctim)){
        digitalWrite(LED_B, HIGH);
      }
      else{
        digitalWrite(LED_B, LOW);
      }
    }else Serial.println("An error ocurred");
    
    https.end();   //Close connection
  
  }
  delay(10000);
}
