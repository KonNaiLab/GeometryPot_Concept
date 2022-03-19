#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

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
  if ((WiFi.status() == WL_CONNECTED)) { //Check the current connection status
    HTTPClient http;
    http.begin("http://6364-2406-3100-1018-2-5a-0-f92c-6eeb.ngrok.io/test"); //Specify the URL
    int httpCode = http.GET();                                        //Make the request
    if (httpCode > 0) { //Check for the returning code
        String payload = http.getString();
        Serial.println(httpCode);
        Serial.println(payload);

        StaticJsonBuffer<256> JSONBuffer;
        JsonObject& parsed=JSONBuffer.parseObject(payload);

        const char * test=parsed["x"];

        Serial.println(test);
        Serial.println()
      }
    else {
      Serial.println("Error on HTTP request");
    }
    http.end(); //Free the resources
  }
  delay(10000);
}
