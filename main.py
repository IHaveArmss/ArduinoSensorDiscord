import serial
import serial.tools.list_ports
import time
import re
import requests

# config
baud_rate = 9600
webhook_url = "https://discord.com/api/webhooks/1388028588716068884/bA25_SwKiubqtfZEOxHCrvQeL12jOQwOgch01oV7waPGu44AZxDrJzrv_7kXAzd0RGKV" 
arduino = None
last_sent_time = 0
alert_interval = 10  # seconds between Discord alerts change if you want more often

def find_arduino():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "CH340" in port.description:
            return port.device
    return None

print("Looking for Arduino...")

while True:
    try:
        if arduino is None or not arduino.is_open:
            port = find_arduino()
            if port:
                print(f"Connecting to {port}...")
                arduino = serial.Serial(port, baud_rate, timeout=1)
                print("Connected.")
            else:
                print("Arduino not found. Retrying...")
                time.sleep(2)
                continue

        if arduino.in_waiting:
            line = arduino.readline().decode('utf-8', errors='ignore').strip()

            if line.startswith("Distance:"):
                match = re.search(r"Distance:\s*(\d+)", line)
                if match:
                    distance = int(match.group(1))
                    print(f"Distance measured: {distance} cm")

                    # discord alert
                    if distance < 5:
                        current_time = time.time()
                        if current_time - last_sent_time > alert_interval:
                            msg = {
                                        "content": f"<@706955959066689627> ⚠️ Warning! Object is very close: **{distance} cm**",
                                        "allowed_mentions": {
                                            "users": ["706955959066689627"]
                                        }
                                    }
                            try:
                                response = requests.post(webhook_url, json=msg)
                                if response.status_code == 204:
                                    print("Alert sent to Discord!")
                                    last_sent_time = current_time
                                else:
                                    print(f"Discord error: {response.status_code} - {response.text}")
                            except Exception as e:
                                print(f"Failed to send Discord message: {e}")
            elif "Out of range" in line:
                print("Object is out of range.")



    except serial.SerialException as e:
        print(f"Serial error: {e}. Reconnecting...")
        if arduino:
            try:
                arduino.close()
            except:
                pass
            arduino = None
        time.sleep(2)

    except KeyboardInterrupt:
        print("Exiting...")
        if arduino and arduino.is_open:
            arduino.close()
        break
