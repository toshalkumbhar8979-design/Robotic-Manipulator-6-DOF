#include <Servo.h>

// 6 servo objects for each joint
Servo s[6];

// PWM pins for each servo
int pins[6] = {3, 5, 6, 9, 10, 11};

// Safe angle boundaries
const int ANGLE_MIN = 10;
const int ANGLE_MAX = 170;

// -----------------------------------------------
// Clamp angle to safe servo range
// -----------------------------------------------
int clampAngle(int val) {
  return constrain(val, ANGLE_MIN, ANGLE_MAX);
}

// -----------------------------------------------
// Setup
// -----------------------------------------------
void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 6; i++) {
    s[i].attach(pins[i]);
    s[i].write(90);   // Start at neutral position
  }

  delay(1000);
  Serial.println("ARM_READY");
}

// -----------------------------------------------
// Main Loop — wait for angle commands from Python
// -----------------------------------------------
void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    data.trim();

    if (data.length() == 0) return;

    int angles[6];
    int count = 0;

    // Parse comma-separated values: "90,90,45,90,90,30"
    while (data.length() > 0 && count < 6) {
      int comma = data.indexOf(',');

      if (comma == -1) {
        // Last value
        angles[count++] = data.toInt();
        break;
      }

      angles[count++] = data.substring(0, comma).toInt();
      data = data.substring(comma + 1);
    }

    // Apply clamped angles to servos
    if (count == 6) {
      for (int i = 0; i < 6; i++) {
        s[i].write(clampAngle(angles[i]));
      }
      Serial.println("OK");
    } else {
      Serial.println("ERR:PARSE");
    }
  }
}
