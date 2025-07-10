import pandas as pd
from sklearn.ensemble import IsolationForest
import json
import os
from datetime import datetime

# Path to the log file and model
LOG_FILE = "logs/traffic_log.json"
MODEL_FILE = "models/anomaly_model.pkl"

# Load logs from file
def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    
    logs = []
    with open(LOG_FILE, "r") as f:
        for line in f.readlines():
            logs.append(json.loads(line.strip()))
    return logs

# Train Isolation Forest model (for anomaly detection)
def train_model():
    logs = load_logs()
    
    # We only use features like packet_size and dst_port for training
    if len(logs) < 10:  # Reduced from 100 to 10 for testing
        print("Not enough data to train model.")
        return None

    # Convert logs to a DataFrame for easier manipulation
    df = pd.DataFrame(logs)
    
    # We use packet_size and dst_port as the feature set
    features = df[["packet_size", "dst_port"]]

    # Train Isolation Forest model
    model = IsolationForest(contamination=0.05)  # 5% contamination (outliers)
    model.fit(features)

    # Save the trained model to disk
    import pickle
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)
    
    print("Model trained and saved.")

# Detect anomalies in new traffic data
def detect_anomaly(log_entry):
    if not os.path.exists(MODEL_FILE):
        return None
    
    # Load the pre-trained model
    import pickle
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)
    
    # Create DataFrame for the new log entry
    log_df = pd.DataFrame([log_entry])
    
    # Get features: packet_size and dst_port
    features = log_df[["packet_size", "dst_port"]]
    
    # Predict using the Isolation Forest model
    prediction = model.predict(features)
    
    # If prediction is -1, it's an anomaly, otherwise it's normal (1)
    if prediction[0] == -1:
        return {"risk_score": 1.0, "tag": "Anomaly"}  # 1.0 for anomaly
    else:
        return {"risk_score": 0.0, "tag": "Normal"}  # 0.0 for normal

# Example usage: Detect anomaly in a single log entry
if __name__ == "__main__":
    logs = load_logs()
    if len(logs) > 0:
        # Train the model first
        train_model()
        
        for log_entry in logs:
            result = detect_anomaly(log_entry)
            if result is not None:
                log_entry.update(result)
                print(f"Updated Log: {log_entry}")
            else:
                print(f"Could not analyze log: {log_entry}")
    else:
        print("No logs found.")
