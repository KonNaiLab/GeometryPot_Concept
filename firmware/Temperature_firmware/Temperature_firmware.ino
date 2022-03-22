#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define DHT_SENSOR_PIN_1 18 // ESP32 pin GIOP22 connected to DHT11 sensor
#define DHT_SENSOR_PIN_2 19 // ESP32 pin GIOP23 connected to DHT11 sensor
#define DHT_SENSOR_TYPE DHT11

DHT dht_sensor1(DHT_SENSOR_PIN_1, DHT_SENSOR_TYPE);
DHT dht_sensor2(DHT_SENSOR_PIN_2, DHT_SENSOR_TYPE);
String servername = "http://1e3b-2001-fb1-b9-3a35-1dcd-6e44-bf48-1939.ngrok.io/fan";

const char* ssid = "pluem";
const char* password = "55483667";

void choose_fan(){
  
}

void setup() {
  Serial.begin(115200);
  dht_sensor1.begin(); // initialize the DHT sensor
  dht_sensor2.begin(); // initialize the DHT sensor
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  
  Serial.println("Connected to the WiFi network");

}

void loop() {
    float humi1  = dht_sensor1.readHumidity(); // read temperature in Celsius
    float tempC1 = dht_sensor1.readTemperature(); // read temperature in Fahrenheit
    float tempF1 = dht_sensor1.readTemperature(true);
  
    float humi2  = dht_sensor2.readHumidity(); // read temperature in Celsius
    float tempC2 = dht_sensor2.readTemperature(); // read temperature in Fahrenheit
    float tempF2 = dht_sensor2.readTemperature(true);
    // check whether the reading is successful or not
    if ( isnan(tempC1) || isnan(tempF1) || isnan(humi1)) {
      Serial.println("Failed to read from DHT sensor1!");
    } else {
      Serial.println("Abled to read from DHT sensor1!");
      Serial.print("Humidity: ");
      Serial.print(humi1);
      Serial.print("%");
  
      Serial.print("  |  ");
  
      Serial.print("Temperature: ");
      Serial.print(tempC1);
      Serial.print("°C  ~  ");
      Serial.print(tempF1);
      Serial.println("°F");
    }
  
    if ( isnan(tempC2) || isnan(tempF2) || isnan(humi2)) {
      Serial.println("Failed to read from DHT sensor2!");
    } else {
      Serial.println("Abled to read from DHT sensor2!");
      Serial.print("Humidity: ");
      Serial.print(humi2);
      Serial.print("%");
  
      Serial.print("  |  ");
  
      Serial.print("Temperature: ");
      Serial.print(tempC2);
      Serial.print("°C  ~  ");
      Serial.print(tempF2);
      Serial.println("°F");
    } 
    if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
      String strC1 = String(tempC1);
      String strC2 = String(tempC2);
      HTTPClient https;  //Declare an object of class HTTPClient
      String hlink = servername;
      https.begin(servername); //Specify request destination
      https.addHeader("Content-Type", "application/json");
      String wrd = "{\"data\": [" + strC1 + "," + strC2 + "]}";
      Serial.println(wrd);
      int httpCode = https.POST(wrd); //Send the request
   
      if (httpCode > 0) { //Check the returning code
        Serial.println("Success");
        DynamicJsonDocument doc(2048);
        String payload = https.getString();   //Get the request response payload
        Serial.println(payload); //Print the response payload
        deserializeJson(doc, payload);
        float ctim = doc["Curenttemp"];
        Serial.println(ctim);
      }
      https.end();   //Close connection
    }
    delay(10000);// wait a 2 seconds between readings   
}
