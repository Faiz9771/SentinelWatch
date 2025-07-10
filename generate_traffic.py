import json
import random
import time
from datetime import datetime
import os
from anomaly_detector import detect_anomaly

# Configuration
OUTPUT_FILE = "logs/traffic_log.json"
NORMAL_PORTS = [80, 443, 22, 3306]  # HTTP, HTTPS, SSH, MySQL
IP_RANGE = list(range(1, 255))  # Generate IPs in 192.168.0.x range

def generate_normal_traffic():
    """Generate normal traffic pattern"""
    return {
        "src_ip": f"192.168.0.{random.choice(IP_RANGE)}",
        "dst_port": random.choice(NORMAL_PORTS),
        "packet_size": random.randint(200, 1500),  # Normal packet size range
        "timestamp": datetime.now().isoformat()  # Already in ISO format
    }

def generate_anomalous_traffic():
    """Generate anomalous traffic pattern"""
    anomaly_type = random.choice([
        "small_packet",
        "large_packet",
        "unusual_port",
        "port_scan",
        "burst_traffic",
        "suspicious_port"
    ])
    
    if anomaly_type == "small_packet":
        return {
            "src_ip": f"192.168.0.{random.choice(IP_RANGE)}",
            "dst_port": random.choice(NORMAL_PORTS),
            "packet_size": random.randint(20, 100),  # Suspiciously small
            "timestamp": datetime.now().isoformat()
        }
    elif anomaly_type == "large_packet":
        return {
            "src_ip": f"192.168.0.{random.choice(IP_RANGE)}",
            "dst_port": random.choice(NORMAL_PORTS),
            "packet_size": random.randint(5000, 10000),  # Suspiciously large
            "timestamp": datetime.now().isoformat()
        }
    elif anomaly_type == "unusual_port":
        return {
            "src_ip": f"192.168.0.{random.choice(IP_RANGE)}",
            "dst_port": random.randint(10000, 65535),  # Unusual high port
            "packet_size": random.randint(200, 1500),
            "timestamp": datetime.now().isoformat()
        }
    elif anomaly_type == "port_scan":
        return {
            "src_ip": f"192.168.0.{random.choice(IP_RANGE)}",
            "dst_port": random.randint(1, 1024),  # Scanning common ports
            "packet_size": random.randint(40, 100),  # Small packets typical in scans
            "timestamp": datetime.now().isoformat()
        }
    elif anomaly_type == "burst_traffic":
        return {
            "src_ip": f"192.168.0.{random.choice(IP_RANGE)}",
            "dst_port": random.choice(NORMAL_PORTS),
            "packet_size": random.randint(2000, 5000),  # Burst of large packets
            "timestamp": datetime.now().isoformat()
        }
    else:  # suspicious_port
        return {
            "src_ip": f"192.168.0.{random.choice(IP_RANGE)}",
            "dst_port": random.choice([23, 445, 3389, 1433]),  # Telnet, SMB, RDP, MSSQL
            "packet_size": random.randint(200, 1500),
            "timestamp": datetime.now().isoformat()
        }

def write_log(log_entry):
    """Write log entry to file"""
    # Ensure directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # Detect anomaly
    result = detect_anomaly(log_entry)
    if result:
        log_entry.update(result)
    
    # Append to file with proper JSON formatting
    with open(OUTPUT_FILE, "a") as f:
        json.dump(log_entry, f)
        f.write("\n")  # Add newline after each entry

def generate_traffic():
    """Generate mixed traffic with occasional anomalies"""
    try:
        while True:
            # 70% normal traffic, 30% anomalous (increased from 10%)
            if random.random() < 0.7:
                log_entry = generate_normal_traffic()
            else:
                log_entry = generate_anomalous_traffic()
            
            write_log(log_entry)
            print(f"Generated log: {log_entry}")
            
            # Wait for a random interval (0.5 to 2 seconds)
            time.sleep(random.uniform(0.5, 2))
            
    except KeyboardInterrupt:
        print("\nStopping traffic generation...")

if __name__ == "__main__":
    generate_traffic() 