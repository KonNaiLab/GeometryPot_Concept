#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

TaskHandle_t Task1;
TaskHandle_t Task2;

const TickType_t xDelay10000ms = pdMS_TO_TICKS(10000);   
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

  //create a task that will be executed in the Task1code() function, with priority 1 and executed on core 0
  xTaskCreatePinnedToCore(
                    Task1code,   /* Task function. */
                    "Task1",     /* name of task. */
                    10000,       /* Stack size of task */
                    NULL,        /* parameter of the task */
                    1,           /* priority of the task */
                    &Task1,      /* Task handle to keep track of created task */
                    0);          /* pin task to core 0 */                   

  //create a task that will be executed in the Task2code() function, with priority 1 and executed on core 1
  xTaskCreatePinnedToCore(
                    Task2code,   /* Task function. */
                    "Task2",     /* name of task. */
                    10000,       /* Stack size of task */
                    NULL,        /* parameter of the task */
                    1,           /* priority of the task */
                    &Task2,      /* Task handle to keep track of created task */
                    1);          /* pin task to core 1 */
}

void Task1code(void * pvParameters){ //humidity
  // read humidity
  while(1){
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
    vTaskDelay(xDelay10000ms);// wait a 2 seconds between readings    
  }

}

void Task2code( void * pvParameters ){ //fan
  while(1){
    Serial.print("Task2 running on core ");  
    /*if ((WiFi.status() == WL_CONNECTED)) { //Check the current connection status
    
      HTTPClient http;
    
      http.begin("http://jsonplaceholder.typicode.com/comments?id=10"); //Specify the URL
      int httpCode = http.GET();                                        //Make the request
    
      if (httpCode > 0) { //Check for the returning code
    
          String payload = http.getString();
          Serial.println(httpCode);
          Serial.println(payload);
        }
    
      else {
        Serial.println("Error on HTTP request");
      }
    
      http.end(); //Free the resources
    }*/
    
    vTaskDelay(xDelay10000ms);    
  }

}

void loop() {

}
