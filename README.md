# 🔔 Arduino Distance Alert to Discord

This project detects when an object is closer than a configurable threshold (default: **5 cm**) to an ultrasonic sensor connected to an Arduino, and sends a real-time **Discord notification** using a webhook.

## 🚀 Features

- 🟢 Real-time distance monitoring using an HC-SR04 ultrasonic sensor.
- 🔁 Configurable distance threshold and alert cooldown interval.
- 🧠 Auto-detects Arduino COM port (supports CH340-based clones too).
- 📲 Sends a custom Discord webhook message (with optional user mention).
- 🖥️ Runs continuously and handles reconnections if Arduino is unplugged.

---

## 🛠️ Requirements

### Hardware
- Arduino (Uno, Nano, etc.)
- HC-SR04 Ultrasonic Sensor
- Jumper wires
- USB cable to connect Arduino to PC

### Software
- [Arduino IDE](https://www.arduino.cc/en/software) (for uploading the sensor code)
- Python 3.x
- Python packages:
  - `pyserial`
  - `requests`

Install dependencies:

```bash
pip install pyserial requests
