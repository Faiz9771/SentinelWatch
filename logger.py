import random
import json
import time
from datetime import datetime

# Path to the log file
LOG_FILE = "logs/traffic_log.json"

# Function to generate a random network traffic log entry
def generate_log():
    # Random IP simulation
    src_ip = f"192.168.0.{random.randint(1, 255)}"
    dst_port = random.choice([22, 80, 443, 3306])  # Common ports (SSH, HTTP, HTTPS, MySQL)
    packet_size = random.randint(50, 1500)  # Random packet size between 50 and 1500 bytes
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    return {
        "src_ip": src_ip,
        "dst_port": dst_port,
        "packet_size": packet_size,
        "timestamp": timestamp
    }

# Function to write logs to a file
def write_log(log_data):
    with open(LOG_FILE, "a") as log_file:
        json.dump(log_data, log_file)
        log_file.write("\n")  # Each log entry in a new line

# Simulate logging network traffic every 2 seconds
if __name__ == "__main__":
    while True:
        log_entry = generate_log()
        write_log(log_entry)
        print(f"Log Entry: {log_entry}")  # For monitoring
        time.sleep(2)  # Log every 2 seconds
