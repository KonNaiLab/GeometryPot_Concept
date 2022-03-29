#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <WiFiClient.h>


#define PIN1 36 //g1
#define PIN2 39 //g2

String SREVERNAME = "http://11f2-184-22-167-181.ngrok.io/other";

const char* ssid = "Komna";
const char* password = "0818723669";

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

void loop() {
  
  WiFiClient wificlient;
  int PIN_Lx=analogRead(PIN1);
  int PIN_L=100-map(PIN_Lx, 0, 4094, 0, 100);
  int PIN_Rx=analogRead(PIN2);
  int PIN_R=100-map(PIN_Rx, 0, 4094, 0, 100);
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

  delay(10000);
}
