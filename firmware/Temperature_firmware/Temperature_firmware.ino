#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define DHT_SENSOR_PIN_1 5 // ESP32 pin GIOP22 connected to DHT11 sensor
#define DHT_SENSOR_PIN_2 19 // ESP32 pin GIOP23 connected to DHT11 sensor
#define DHT_SENSOR_TYPE DHT11

#define Fan_1 23
#define Fan_2 22

DHT dht_sensor1(DHT_SENSOR_PIN_1, DHT_SENSOR_TYPE);
DHT dht_sensor2(DHT_SENSOR_PIN_2, DHT_SENSOR_TYPE);
String servername = "http://11f2-184-22-167-181.ngrok.io/fan";

const char* ssid = "Komna";
const char* password = "0818723669";

void choose_fan(){
  
}

void setup() {
  Serial.begin(115200);
  dht_sensor1.begin(); // initialize the DHT sensor
  dht_sensor2.begin(); // initialize the DHT sensor
  WiFi.begin(ssid, password);
  pinMode(Fan_1, OUTPUT);
  pinMode(Fan_2, OUTPUT);
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
        float ctmp1 = doc["Currenttemp"][0];
        float ctmp2 = doc["Currenttemp"][1];
        float stmp1 = doc["SettingTemp"][0];
        float stmp2 = doc["SettingTemp"][1];
        int man1 = doc["Manual"][0];
        int man2 = doc["Manual"][1];
        Serial.println(man1);
        Serial.println(ctmp1);
        if(man1 == 2){
          Serial.println("Fan 1 on");
          digitalWrite(Fan_1, HIGH);
        }
        else if(man1 == 1){
          digitalWrite(Fan_1, LOW);
          Serial.println("Fan 1 off");
        }
        else{
          if(ctmp1 > stmp1){
            digitalWrite(Fan_1, HIGH);
          }
          else{
            digitalWrite(Fan_1, LOW);
          }
        }
        if(man2 == 2){
          digitalWrite(Fan_2, HIGH);
        }
        else if(man2 == 1){
          digitalWrite(Fan_2, LOW);
        }
        else{
          if(ctmp2 > stmp2){
            digitalWrite(Fan_2, HIGH);
          }
          else{
            digitalWrite(Fan_2, LOW);
          }
        }
      }
      https.end();   //Close connection
    }
    
    delay(10000);// wait a 10 seconds between readings   
}
