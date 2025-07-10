# SentinelWatch

A real-time network traffic monitoring and anomaly detection system built with Python and Flask.

## Features

- Real-time network traffic monitoring
- Anomaly detection using machine learning
- Web-based dashboard for visualization
- Traffic generation for testing
- Comprehensive logging system

## Project Structure

```
sentinelwatch/
├── app.py                 # Main Flask application
├── anomaly_detector.py    # Anomaly detection logic
├── generate_traffic.py    # Traffic generation utility
├── logger.py             # Logging configuration
├── static/               # Static files for web interface
├── models/               # Trained ML models
└── logs/                 # Application logs
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Faiz9771/SentinelWatch.git
cd SentinelWatch
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:

```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. To generate test traffic:

```bash
python generate_traffic.py
```

## Configuration

The application can be configured through environment variables or by modifying the configuration files in the project.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
