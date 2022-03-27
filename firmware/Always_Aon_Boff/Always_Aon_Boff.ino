#define LEDA D1
#define LEDB D2

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Setup...");
  pinMode(LEDA, OUTPUT);
  pinMode(LEDB, OUTPUT);
  Serial.println("A on");
  digitalWrite(LEDA, LOW);
  Serial.println("B off");
  digitalWrite(LEDB, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Running...");
  Serial.println("A on");
  digitalWrite(LEDA, HIGH);
  Serial.println("B off");
  digitalWrite(LEDB, HIGH);
  delay(10000);
}
