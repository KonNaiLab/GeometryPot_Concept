#include <DHT.h>
/*#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_Sensor.h>*/
#include <WiFi.h>
#include <HTTPClient.h>
  

#define DHT_SENSOR_PIN_1 18 // ESP32 pin GIOP22 connected to DHT11 sensor
#define DHT_SENSOR_PIN_2 19 // ESP32 pin GIOP23 connected to DHT11 sensor
#define DHT_SENSOR_TYPE DHT11
/*#define OLED_WIDTH 128
#define OLED_HEIGHT 64
Adafruit_SSD1306 display(OLED_WIDTH, OLED_HEIGHT, &Wire, -1);*/

DHT dht_sensor1(DHT_SENSOR_PIN_1, DHT_SENSOR_TYPE);
DHT dht_sensor2(DHT_SENSOR_PIN_2, DHT_SENSOR_TYPE);

const char* ssid = "pluem";
const char* password = "55483667";

void setup() {
  Serial.begin(115200);
  dht_sensor1.begin(); // initialize the DHT sensor
  dht_sensor2.begin(); // initialize the DHT sensor
  delay(4000);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  
  Serial.println("Connected to the WiFi network");
/*
  // initialize with the I2C addr 0x3C
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  
 
  delay(2000);
  display.clearDisplay();
  display.setTextColor(WHITE);*/
}

void loop() {
  // read humidity
  delay(5000);// wait a 2 seconds between readings

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
  
  float humi1  = dht_sensor1.readHumidity(); // read temperature in Celsius
  float tempC1 = dht_sensor1.readTemperature(); // read temperature in Fahrenheit
  float tempF1 = dht_sensor1.readTemperature(true);

  float humi2  = dht_sensor2.readHumidity(); // read temperature in Celsius
  float tempC2 = dht_sensor2.readTemperature(); // read temperature in Fahrenheit
  float tempF2 = dht_sensor2.readTemperature(true);
  //display.clearDisplay();
  // check whether the reading is successful or not
  if ( isnan(tempC1) || isnan(tempF1) || isnan(humi1)) {
    Serial.println("Failed to read from DHT sensor1!");
    /*display.setTextSize(2);
    display.setTextColor(WHITE);
    display.setCursor(0,15);
    display.println("Error");
    display.display();*/
  } else {
    char buf1[20];
    sprintf(buf1,"%d.%02d", (int)(tempC1*100)/100,(int)(tempC1*100)%100);
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
   /* display.setTextSize(1);
    display.setCursor(0,0);
    display.print("Temperature: ");
    display.setTextSize(2);
    display.setCursor(0,10);
    display.print(tempC1);
    display.print(" ");
    display.setTextSize(1);
    display.cp437(true);
    display.write(167);
    display.setTextSize(2);
    display.print("C");
    display.display(); */
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
}
