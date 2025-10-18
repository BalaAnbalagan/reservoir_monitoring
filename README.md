# Reservoir Monitoring System

A real-time water level monitoring system for California reservoirs using MQTT protocol. This system fetches live data from the California Data Exchange Center (CDEC) API, publishes it via MQTT to topics, collects and aggregates the data, and generates comprehensive reports with interactive visualizations.

## Features

- **Live Data Integration** - Fetches real-time data from CDEC API for 21+ major California reservoirs
- **MQTT Protocol** - Lightweight, reliable message broker for IoT-style communication
- **Single Subscriber** - Collects data from all reservoirs using wildcard subscriptions
- **Multiple Publishers** - CSV-based (for testing) and API-based (for live data)
- **Comprehensive Reports** - JSON (machine-readable) and TXT (human-readable) formats
- **Interactive Web Dashboard** - Flask-powered web interface with real-time visualizations
- **Advanced Chart Visualizations** - Bar charts, stacked bar charts, and time-series analysis using Chart.js
- **Cloud Deployment Ready** - Configured for Render.com with auto-deploy from GitHub
- **Scalable Architecture** - Easy to add new reservoirs or data sources

## Table of Contents
- [Overview](#overview)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Web Dashboard](#web-dashboard)
- [Deployment to Render.com](#deployment-to-rendercom)
- [Project Structure](#project-structure)
- [Key Concepts](#key-concepts)
- [Real-World Applications](#real-world-applications)

---

## Overview

This project simulates the **California Department of Water Resources** monitoring system that:
- Collects water level data from multiple reservoir sensors
- Uses MQTT protocol for real-time data transmission
- Aggregates data from all reservoirs using a single subscriber
- Generates comprehensive daily reports

### What's MQTT?

Think of MQTT as a **group chat for devices**:
- **Traditional Way**: Each device calls you individually (inefficient)
- **MQTT Way**: Devices post updates to topics, and you read them all at once

MQTT is like WhatsApp for IoT devices - lightweight, reliable, and scalable!

---

## How It Works

### The Big Picture

```
┌─────────────┐
│   Sensors   │ (Publishers)
│  (Shasta)   │ ──┐
└─────────────┘   │
                  │
┌─────────────┐   │     ┌──────────────┐
│   Sensors   │───┼────→│ MQTT Broker  │
│ (Oroville)  │   │     │ (Mosquitto)  │
└─────────────┘   │     └──────────────┘
                  │            │
┌─────────────┐   │            ↓
│   Sensors   │ ──┘     ┌──────────────┐
│  (Sonoma)   │         │  Subscriber  │
└─────────────┘         │   (Report    │
                        │  Generator)  │
                        └──────────────┘
                               ↓
                        ┌──────────────┐
                        │   Reports    │
                        │   (JSON/TXT) │
                        └──────────────┘
```

### Step-by-Step Process

1. **Data Conversion**: CSV files are converted to JSON format
2. **Publishers Start**: Reservoir sensors publish water level data to specific topics:
   - Shasta → `SHASTA/WML`
   - Oroville → `OROVILLE/WML`
   - Sonoma → `SONOMA/WML`
3. **Subscriber Collects**: Single subscriber listens to all topics
4. **Reports Generated**: Daily summaries with averages, min/max, and totals

---

## Architecture

### Components

#### 1. MQTT Broker (Mosquitto) - "The Post Office"
- Acts as a central message hub
- Receives messages from publishers
- Delivers messages to subscribers
- Runs on `localhost:1883`

#### 2. Publishers (Sensors) - "The Senders"
- Simulate reservoir sensors
- Publish water level data to specific topics
- Send messages in JSON format

**Example Message:**
```json
{
  "reservoir_id": "SHASTA",
  "date": "10/1/2024",
  "water_level_taf": 2721.0,
  "timestamp": "2024-10-01T00:00:00",
  "published_at": "2025-10-18T00:50:00"
}
```

#### 3. Subscriber - "The Listener"
- Subscribes to all reservoir topics
- Collects data from all reservoirs
- Generates daily aggregated reports

---

## Prerequisites

### Software Requirements

1. **Python 3.7+**
   - Check: `python --version`

2. **MQTT Broker (Mosquitto)**
   - Download: https://mosquitto.org/download/
   - Windows: Install the `.exe` installer
   - Linux: `sudo apt-get install mosquitto mosquitto-clients`
   - macOS: `brew install mosquitto`

3. **Python Packages**
   - `paho-mqtt==1.6.1`

---

## Installation

### Step 1: Clone or Download Project
```bash
cd c:\myCodes\reservoir_monitoring
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install and Start Mosquitto

**Windows:**
1. Download from https://mosquitto.org/download/
2. Run the installer
3. Start the service:
   ```bash
   net start mosquitto
   ```

**Linux/macOS:**
```bash
# Install
sudo apt-get install mosquitto mosquitto-clients  # Linux
brew install mosquitto                             # macOS

# Start
sudo systemctl start mosquitto                     # Linux
brew services start mosquitto                      # macOS
```

### Step 4: Verify Installation
```bash
# Check Mosquitto is running
sc query mosquitto              # Windows
sudo systemctl status mosquitto # Linux
brew services list              # macOS
```

---

## Usage

### Quick Start

Run the complete system in 3 steps:

#### Step 1: Convert CSV to JSON
```bash
python csv_to_json.py
```

**Output:**
```
Converting Shasta_WML.csv to JSON...
  -> 9 records converted for SHASTA
Converting Oroville_WML.csv to JSON...
  -> 9 records converted for OROVILLE
Converting Sonoma_WML.csv to JSON...
  -> 9 records converted for SONOMA
```

#### Step 2: Start Subscriber (Terminal 1)
```bash
python subscriber.py --duration 60
```

**Options:**
- `--broker`: MQTT broker address (default: `localhost`)
- `--port`: MQTT broker port (default: `1883`)
- `--duration`: How long to listen in seconds (default: `30`)

#### Step 3: Start Publisher (Terminal 2)
```bash
python publisher.py --reservoir ALL
```

**Options:**
- `--reservoir`: Which reservoir to publish (`SHASTA`, `OROVILLE`, `SONOMA`, or `ALL`)
- `--broker`: MQTT broker address (default: `localhost`)
- `--port`: MQTT broker port (default: `1883`)

**Examples:**
```bash
# Publish only Shasta data
python publisher.py --reservoir SHASTA

# Publish to remote broker
python publisher.py --reservoir ALL --broker 192.168.1.100

# Publish all reservoirs to custom port
python publisher.py --reservoir ALL --port 1884
```

---

## Web Dashboard

The project includes a Flask-powered web dashboard for visualizing reservoir data in real-time.

### Starting the Web Dashboard

```bash
python app.py
```

The dashboard will be available at: `http://localhost:5000`

### Dashboard Features

#### 1. Summary View (`/`)
- Overview of total water storage
- Period changes and statistics
- Number of active reservoirs
- Quick summary cards

#### 2. Detailed View (`/detailed`)
- **Interactive Bar Charts** - Current water levels by reservoir
- **Stacked Bar Charts** - Water distribution over time across all reservoirs
- **Change Analysis** - Visual representation of water level changes (green=gain, red=loss)
- **Toggleable Tables** - Detailed historical data tables (hidden by default)
- Complete day-over-day change analysis

#### 3. Advanced Charts View (`/detailed/charts`)
- Top 10 largest reservoirs (horizontal bar chart)
- Multi-day comparison with interactive controls
- Weekly comparison view
- First vs Last day analysis

#### 4. API Endpoints
- `/api/summary` - Summary statistics (JSON)
- `/api/latest` - Latest day data (JSON)
- `/api/historical` - Complete historical data (JSON)
- `/api/changes` - Day-over-day changes (JSON)
- `/api/reservoir/<name>` - Specific reservoir data (JSON)

### Technologies Used
- **Flask** - Web framework
- **Chart.js** - Interactive charts and visualizations
- **Gunicorn** - Production WSGI server
- **Bootstrap styling** - Responsive design

---

## Deployment to Render.com

This project is configured for easy deployment to Render.com's free tier.

### Prerequisites
- GitHub account
- Render.com account (sign up at https://render.com)
- Code pushed to GitHub repository

### Deployment Steps

#### 1. Connect to Render.com
1. Go to https://render.com and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select the `reservoir_monitoring` repository

#### 2. Configure Service
Render will auto-detect settings from `render.yaml`:
- **Name**: `reservoir-monitoring`
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Instance Type**: Free

#### 3. Deploy
Click **"Create Web Service"** and wait for deployment (5-10 minutes)

#### 4. Access Your Live App
Your app will be available at: `https://your-app-name.onrender.com`

### Auto-Deploy from GitHub
- Every push to the `main` branch triggers automatic deployment
- No manual intervention needed
- View build logs in Render dashboard

### Free Tier Limitations
- App spins down after 15 minutes of inactivity
- ~30 seconds to wake up on first request
- 750 hours/month free

### Environment Variables (Optional)
Add in Render dashboard if needed:
- `FLASK_ENV`: `production`
- `PYTHON_VERSION`: `3.11.0`

---

## Project Structure

```
reservoir_monitoring/
│
├── data/                           # Data files
│   ├── Shasta_WML.csv             # Shasta reservoir CSV data
│   ├── Oroville_WML.csv           # Oroville reservoir CSV data
│   ├── Sonoma_WML.csv             # Sonoma reservoir CSV data
│   ├── SHASTA_WML.json            # Generated JSON files
│   ├── OROVILLE_WML.json
│   └── SONOMA_WML.json
│
├── templates/                      # Flask HTML templates
│   ├── index.html                 # Summary dashboard
│   ├── detailed.html              # Detailed view with charts
│   └── detailed_charts.html       # Advanced interactive charts
│
├── reports/                        # Generated reports
│   ├── comprehensive_report_*.json # Detailed JSON reports
│   ├── summary_report_*.txt        # Human-readable summaries
│   └── visualizations/             # Generated chart images
│
├── app.py                          # Flask web application
├── api_publisher.py                # Live API data publisher
├── publisher.py                    # MQTT publisher (CSV-based)
├── subscriber.py                   # MQTT subscriber (data collector)
├── csv_to_json.py                  # CSV to JSON converter
├── visualize.py                    # Chart generation utilities
├── generate_dashboard.py           # Dashboard generation
│
├── requirements.txt                # Python dependencies
├── runtime.txt                     # Python version for deployment
├── Procfile                        # Process file for Heroku/Render
├── render.yaml                     # Render.com configuration
├── .gitignore                      # Git ignore rules
│
└── README.md                       # This file
```

---

## Key Concepts

### MQTT Topics

Topics are like **channels** or **hashtags**:
- `SHASTA/WML` - Shasta water mark level
- `OROVILLE/WML` - Oroville water mark level
- `SONOMA/WML` - Sonoma water mark level

Publishers send to topics, subscribers listen to topics.

### Quality of Service (QoS)

This project uses **QoS 1** (At least once delivery):
- Message delivery is guaranteed
- Messages are acknowledged
- Perfect for critical data like water levels

### TAF (Thousand Acre-Feet)

Unit for measuring water volume:
- 1 TAF = 1,233,482 cubic meters
- 1 TAF = 325,851 gallons
- Common in US reservoir measurements

### Data Model

```json
{
  "reservoir_id": "SHASTA",           // Reservoir identifier
  "date": "10/1/2024",                // Reading date
  "water_level_taf": 2721.0,          // Water level in TAF
  "timestamp": "2024-10-01T00:00:00", // ISO 8601 timestamp
  "published_at": "2025-10-18T..."    // When message was sent
}
```

---

## Generated Reports

### JSON Report (Machine-Readable)

Located in `reports/comprehensive_report_*.json`:

```json
[
  {
    "date": "10/1/2024",
    "reservoirs": {
      "SHASTA": {
        "average_water_level_taf": 2721.0,
        "min_water_level_taf": 2721.0,
        "max_water_level_taf": 2721.0,
        "readings_count": 1
      },
      "OROVILLE": {
        "average_water_level_taf": 1999.0,
        "min_water_level_taf": 1999.0,
        "max_water_level_taf": 1999.0,
        "readings_count": 1
      }
    },
    "total_water_level_taf": 4720.0
  }
]
```

### Text Report (Human-Readable)

Located in `reports/summary_report_*.txt`:

```
================================================================================
CALIFORNIA DEPARTMENT OF WATER RESOURCES
RESERVOIR WATER MARK LEVEL DAILY SUMMARY REPORT
================================================================================

Report Generated: 2025-10-18 00:50:42
Total Messages Collected: 27
Reporting Period: 8 days

================================================================================

DATE: 10/1/2024
--------------------------------------------------------------------------------

  SHASTA RESERVOIR:
    Average Water Level:    2721.00 TAF
    Minimum Water Level:    2721.00 TAF
    Maximum Water Level:    2721.00 TAF
    Number of Readings:           1

  OROVILLE RESERVOIR:
    Average Water Level:    1999.00 TAF
    Minimum Water Level:    1999.00 TAF
    Maximum Water Level:    1999.00 TAF
    Number of Readings:           1

  TOTAL WATER LEVEL (All Reservoirs):    4720.00 TAF

================================================================================
```

---

## Real-World Applications

This architecture is used in:

### IoT Systems
- **Smart Homes**: Thermostats, lights, security cameras
- **Industrial IoT**: Factory sensors, equipment monitoring
- **Agriculture**: Soil moisture, weather stations

### Real Companies Using MQTT
- **Tesla**: Vehicle telemetry data
- **Amazon AWS IoT**: Cloud IoT services
- **Facebook Messenger**: Message delivery
- **NASA**: Satellite communication

### Why MQTT?

1. **Lightweight**: Works on tiny devices with limited resources
2. **Reliable**: Guarantees message delivery
3. **Scalable**: Handles thousands of devices
4. **Real-time**: Instant data transmission
5. **Bi-directional**: Devices can send and receive

---

## Troubleshooting

### Common Issues

**1. "Connection refused" error**
```
Problem: Mosquitto broker not running
Solution: Start Mosquitto service
  Windows: net start mosquitto
  Linux: sudo systemctl start mosquitto
```

**2. "No module named 'paho'"**
```
Problem: paho-mqtt not installed
Solution: pip install paho-mqtt
```

**3. Subscriber receives no messages**
```
Problem: Publisher ran before subscriber started
Solution: Start subscriber first, then publisher within the duration window
```

**4. Port 1883 already in use**
```
Problem: Another broker is running
Solution:
  - Check running processes
  - Use different port: --port 1884
```

---

## Assignment Requirements

This project fulfills the following requirements:

- [x] MQTT publishers sending to `RESERVOIR_ID/WML` topics
- [x] MQTT subscriber collecting from all topics
- [x] JSON data model
- [x] CSV to JSON conversion
- [x] Single subscriber generating daily reports
- [x] TAF (Thousand Acre-Feet) measurements
- [x] Aggregated data from multiple reservoirs
- [x] Web dashboard with interactive visualizations
- [x] Cloud deployment configuration (Render.com)

---

## Future Enhancements

Possible improvements:
- Add database storage (MongoDB, PostgreSQL) for historical data
- Add email/SMS alerts for critical water levels
- Implement user authentication and authorization
- Add real-time WebSocket updates for live dashboard
- Implement data persistence for offline scenarios
- Add authentication and encryption (MQTT with TLS)
- Add predictive analytics and forecasting
- Integrate with weather API for correlation analysis
- Deploy to additional cloud platforms (AWS IoT, Azure IoT Hub)
- Mobile app development (React Native/Flutter)

---

## License

This project is for educational purposes as part of the California Department of Water Resources assignment.

---

## References

- [MQTT Official Website](https://mqtt.org/)
- [Mosquitto Documentation](https://mosquitto.org/documentation/)
- [Paho MQTT Python Client](https://pypi.org/project/paho-mqtt/)
- [California Data Exchange Center](https://cdec.water.ca.gov/resapp/RescondMain)

---

## Contact

For questions or issues, please refer to the assignment guidelines or contact your instructor.

---

**Built with Python, MQTT, and Mosquitto**
