#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <WiFiClient.h>

#define PIN1 23
#define PIN2 22

String SREVERNAME = "http://398e-158-108-225-190.ngrok.io/pump";

const char* ssid = "com_x";
const char* password = "wwwcomxx111";

void setup() {
  Serial.begin(115200);
  delay(4000);
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
    http.begin(wificlient, SREVERNAME); //Specify the URL
    http.addHeader("Content-Type", "application/json");
    String wrd = "{\"data\": [" + strA + "," + strB + "]}";
    Serial.println(wrd);
    int httpCode = http.POST(wrd);                                        //Make the request
    if (httpCode > 0) { //Check for the returning code
        Serial.println("Success");
        String payload = http.getString();
        Serial.println(httpCode);
        Serial.println(payload);
      }
    else {
      Serial.println("Error on HTTP request");
    }
    http.end(); //Free the resources
  }
  

  delay(1000);
} 
