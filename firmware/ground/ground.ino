#define PIN 39

void setup() {
  Serial.begin(115200); // set up serial port for 9600 baud (speed)
  delay(500); // wait for display to boot up
}

void loop() {
  
  int sensorValue;
  sensorValue = analogRead(PIN);
  sensorValue = map(sensorValue, 0, 1023, 0, 100);
  sensorValue=100-(sensorValue/10);
  Serial.println("Analog Value : ");
  
  Serial.println(sensorValue);
  
  delay(500); //wait for half a second, so it is easier to read
}
