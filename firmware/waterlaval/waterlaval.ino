#define PIN 23

void setup() {
  Serial.begin(115200);
}
 
void loop() {
  if (digitalRead(PIN) == 1) {
    Serial.println("Water detected");
  } else {
    Serial.println("No Water");
  }
  delay(1000);
}                                         
