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
- [1. Overview](#1-overview)
- [2. What's MQTT?](#2-whats-mqtt)
- [3. How It Works](#3-how-it-works)
  - [3.1 Local Development Setup](#31-local-development-setup)
  - [3.2 Cloud Production Setup](#32-cloud-production-setup)
- [4. Architecture](#4-architecture)
- [5. Prerequisites](#5-prerequisites)
- [6. Installation & Setup](#6-installation--setup)
- [7. Usage](#7-usage)
  - [7.1 Local Development](#71-local-development)
  - [7.2 Cloud Production](#72-cloud-production)
- [8. Web Dashboard](#8-web-dashboard)
- [9. Deployment to Render.com](#9-deployment-to-rendercom)
- [10. Project Structure](#10-project-structure)
- [11. Key Concepts](#11-key-concepts)
- [12. Contact](#12-contact)

---

## 1. Overview

This project simulates the **California Department of Water Resources** monitoring system that:
- Collects water level data from multiple reservoir sensors
- Uses MQTT protocol for real-time data transmission
- Aggregates data from all reservoirs using a single subscriber
- Generates comprehensive daily reports

The system supports **two deployment modes**:
- **Local Development**: Runs on your machine with Mosquitto broker for testing and development
- **Cloud Production**: Fully automated cloud-based system using HiveMQ Cloud, MongoDB Atlas, and GitHub Actions

---

## 2. What's MQTT?

Think of MQTT as a **group chat for devices**:
- **Traditional Way**: Each device calls you individually (inefficient)
- **MQTT Way**: Devices post updates to topics, and you read them all at once

MQTT is like WhatsApp for IoT devices - lightweight, reliable, and scalable!

---

## 3. How It Works

This system can operate in two modes: **Local Development** and **Cloud Production**. Both use the same MQTT pub/sub architecture but differ in infrastructure.

### 3.1 Local Development Setup

**Architecture:**
```
Your Machine:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌─────────────┐                                        │
│  │  Publishers │ ──┐                                    │
│  │ (CSV/API)   │   │                                    │
│  └─────────────┘   │     ┌──────────────┐              │
│                    ├────→│  Mosquitto   │              │
│  ┌─────────────┐   │     │    Broker    │              │
│  │  Publisher  │ ──┘     │ localhost:   │              │
│  │   (API)     │         │     1883     │              │
│  └─────────────┘         └──────────────┘              │
│                                 │                       │
│                                 ↓                       │
│                          ┌──────────────┐               │
│                          │  Subscriber  │               │
│                          │   (Collect)  │               │
│                          └──────────────┘               │
│                                 │                       │
│                                 ↓                       │
│                          ┌──────────────┐               │
│                          │ JSON Reports │               │
│                          │  (reports/)  │               │
│                          └──────────────┘               │
│                                 │                       │
│                                 ↓                       │
│                          ┌──────────────┐               │
│                          │  Flask App   │               │
│                          │  localhost:  │               │
│                          │     5000     │               │
│                          └──────────────┘               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**How it works:**
1. Install Mosquitto broker on your machine
2. Run subscriber to listen for messages
3. Run publisher to send reservoir data
4. Subscriber saves reports to local JSON files
5. Flask app reads JSON files and displays dashboard

**Use Case:** Development, testing, and learning MQTT concepts

---

### 3.2 Cloud Production Setup

**Architecture:**
```
GitHub Actions (Scheduled Daily):
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌─────────────┐        ┌──────────────┐               │
│  │ API Publisher│───────→│   HiveMQ     │               │
│  │ (CDEC API)  │        │    Cloud     │               │
│  └─────────────┘        │   Broker     │               │
│                         │  (TLS 8883)  │               │
│                         └──────────────┘               │
│                                │                        │
│                                ↓                        │
│                         ┌──────────────┐                │
│                         │  Subscriber  │                │
│                         │   (Collect)  │                │
│                         └──────────────┘                │
│                                │                        │
│                                ↓                        │
│                         ┌──────────────┐                │
│                         │  MongoDB     │                │
│                         │   Atlas      │                │
│                         │  (Cloud DB)  │                │
│                         └──────────────┘                │
│                                                         │
└─────────────────────────────────────────────────────────┘
                                │
                                ↓
                         ┌──────────────┐
                         │  Render.com  │
                         │  Flask App   │
                         │  (reads DB)  │
                         └──────────────┘
                                │
                                ↓
                         ┌──────────────┐
                         │  Live Web    │
                         │  Dashboard   │
                         └──────────────┘
```

**How it works:**
1. **GitHub Actions** runs daily at 8 AM UTC (midnight PST)
2. **API Publisher** fetches live data from CDEC API
3. **HiveMQ Cloud** receives data via secure TLS connection
4. **Subscriber** collects data and saves to MongoDB Atlas
5. **Render.com** hosts Flask app (reads from MongoDB)
6. **Users** see live dashboard with fresh daily data

**Use Case:** Production deployment with zero manual intervention

**Benefits:**
- Completely free (uses free tiers of all services)
- Fully automated daily updates
- No local infrastructure needed
- Secure cloud MQTT with TLS/SSL
- Scalable database storage
- Professional cloud deployment

---

## 4. Architecture

### Components

#### 1. MQTT Broker - "The Post Office"

**Local Mode (Mosquitto):**
- Acts as a central message hub on your machine
- Receives messages from publishers
- Delivers messages to subscribers
- Runs on `localhost:1883`
- No authentication required

**Cloud Mode (HiveMQ Cloud):**
- Cloud-hosted MQTT broker
- Secure TLS/SSL connections (port 8883)
- Username/password authentication
- Free tier: 100 MB/month
- Globally accessible

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
- Subscribes to all reservoir topics using wildcard (`+/WML`)
- Collects data from all reservoirs
- Generates daily aggregated reports

**Local Mode:**
- Saves reports to JSON files in `reports/` directory
- Flask app reads from JSON files

**Cloud Mode:**
- Saves reports directly to MongoDB Atlas
- Flask app reads from MongoDB (no file commits)

#### 4. Database Storage

**Local Mode (JSON Files):**
- Reports stored in `reports/` directory
- File-based storage
- No external dependencies

**Cloud Mode (MongoDB Atlas):**
- Cloud-hosted NoSQL database
- Free tier: 512 MB storage
- Automatic scaling
- Supports queries and aggregations

---

## 5. Prerequisites

### Software Requirements

**For Local Development:**

1. **Python 3.7+**
   - Check: `python --version`

2. **MQTT Broker (Mosquitto)** - Required for local mode only
   - Download: https://mosquitto.org/download/
   - Windows: Install the `.exe` installer
   - Linux: `sudo apt-get install mosquitto mosquitto-clients`
   - macOS: `brew install mosquitto`

3. **Python Packages**
   - See `requirements.txt` for full list
   - Main packages: `paho-mqtt`, `flask`, `requests`

**For Cloud Production:**

1. **GitHub Account** - For hosting code and automated workflows
2. **HiveMQ Cloud Account** - Free tier MQTT broker (https://console.hivemq.cloud)
3. **MongoDB Atlas Account** - Free tier database (https://www.mongodb.com/atlas)
4. **Render.com Account** - Free tier web hosting (https://render.com)

---

## 6. Installation & Setup

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

## 7. Usage

The system supports two operational modes: **Local Development** and **Cloud Production**. Choose the mode that fits your needs.

---

### 7.1 Local Development

**When to use:** Development, testing, learning MQTT concepts, running without internet

**Requirements:**
- Mosquitto broker running on your machine
- Python environment set up
- No cloud accounts needed

#### Step 1: Start Mosquitto Broker

```bash
# Windows
net start mosquitto

# Linux
sudo systemctl start mosquitto

# macOS
brew services start mosquitto
```

#### Step 2: Test MQTT Connection (Optional)

```bash
# Test local MQTT connection
python test_mqtt.py local
```

**Expected output:**
```
[LOCAL] Using LOCAL MQTT: localhost
[SUCCESS] CONNECTION SUCCESSFUL!
   Connected to localhost:1883
```

#### Step 3: Start Subscriber (Terminal 1)

```bash
# Use local MQTT (default)
python subscriber.py --duration 60
```

**What happens:**
- Connects to `localhost:1883`
- Listens for messages on all reservoir topics (`+/WML`)
- Saves reports to `reports/` directory as JSON files
- Runs for 60 seconds then generates reports

#### Step 4: Start Publisher (Terminal 2)

**Option A: CSV-based publisher (for testing)**
```bash
# Publish data from CSV files
python publisher.py --reservoir ALL
```

**Option B: API-based publisher (live CDEC data)**
```bash
# Fetch live data from CDEC API and publish
python api_publisher.py --reservoir ALL --days 7
```

**What happens:**
- Fetches reservoir data (from CSV or API)
- Publishes to local Mosquitto broker
- Messages sent to topics like `SHASTA/WML`, `OROVILLE/WML`
- Subscriber receives and processes messages

#### Step 5: View Dashboard

```bash
# Start Flask app
python app.py
```

Visit: `http://localhost:5000`

**What happens:**
- Flask app reads reports from `reports/` directory
- Displays interactive dashboard with charts
- Shows latest water level data

**Complete Local Workflow:**
```bash
# Terminal 1: Start subscriber
python subscriber.py --duration 60

# Terminal 2: Publish data (within 60 seconds)
python api_publisher.py --reservoir ALL --days 7

# Terminal 3: Start web dashboard
python app.py
```

---

### 7.2 Cloud Production

**When to use:** Production deployment, automated daily updates, no local infrastructure

**Requirements:**
- GitHub repository set up
- HiveMQ Cloud account (free tier)
- MongoDB Atlas account (free tier)
- Render.com account (free tier)
- GitHub Secrets configured

#### How Cloud Production Works

**Automated Daily Workflow:**

```
Every day at 8:00 AM UTC (midnight PST):

1. GitHub Actions workflow triggers automatically
2. Fetches live data from CDEC API (21 reservoirs, 7 days)
3. Publishes data to HiveMQ Cloud (secure TLS)
4. Subscriber collects messages from HiveMQ Cloud
5. Saves reports to MongoDB Atlas
6. Render.com serves Flask app (reads from MongoDB)
7. Users see updated dashboard with fresh data
```

**No manual intervention required!**

#### Setup Steps

**1. Configure GitHub Secrets**

Add these secrets to your GitHub repository (Settings → Secrets → Actions):

- `MQTT_CLOUD_BROKER`: Your HiveMQ cluster URL
- `MQTT_CLOUD_PORT`: `8883`
- `MQTT_CLOUD_USER`: Your HiveMQ username
- `MQTT_CLOUD_PASS`: Your HiveMQ password
- `MONGODB_URI`: Your MongoDB Atlas connection string

See [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md) for detailed instructions.

**2. Configure Render.com Environment Variables**

Add these environment variables in Render dashboard:

- `DB_MODE`: `mongodb`
- `MONGODB_URI`: Your MongoDB Atlas connection string
- `FLASK_ENV`: `production`

**3. Test the Workflow**

```bash
# Go to GitHub repository → Actions tab
# Select "Update Reservoir Data with Cloud MQTT"
# Click "Run workflow" → "Run workflow"
# Watch the workflow execute in real-time
```

**Expected workflow output:**
```
✅ Subscriber connects to HiveMQ Cloud
✅ Publisher fetches data from CDEC API
✅ Data published to cloud MQTT
✅ Subscriber collects messages
✅ Reports saved to MongoDB
✅ Workflow completes successfully
```

**4. Access Live Dashboard**

Visit: `https://your-app-name.onrender.com`

**What you'll see:**
- Real-time reservoir water levels
- Interactive charts and visualizations
- Historical data trends
- Automatic daily updates

#### Manual Cloud Testing (Optional)

You can also test cloud MQTT manually from your local machine:

```bash
# Set environment to cloud mode
set MQTT_ENV=cloud          # Windows
export MQTT_ENV=cloud       # Linux/macOS

# Test cloud MQTT connection
python test_mqtt.py cloud

# Run subscriber with cloud MQTT
python subscriber.py --duration 90

# Run publisher with cloud MQTT
python api_publisher.py --reservoir ALL --days 7
```

#### Monitoring and Logs

**GitHub Actions:**
- View workflow runs: Repository → Actions tab
- Check logs for each step
- See data collection progress

**Render.com:**
- View deployment logs
- Monitor application health
- Check build status

**MongoDB Atlas:**
- View stored reports: Collections → daily_reports
- Monitor database size
- Check connection status

---

### Switching Between Local and Cloud

The system automatically detects the environment using the `MQTT_ENV` variable:

**Local Mode (default):**
```bash
# No environment variable needed
python subscriber.py
python publisher.py --reservoir ALL
```

**Cloud Mode:**
```bash
# Set environment variable
set MQTT_ENV=cloud          # Windows
export MQTT_ENV=cloud       # Linux/macOS

python subscriber.py --duration 90
python api_publisher.py --reservoir ALL
```

**Database Mode:**

Set `DB_MODE` to choose storage:
```bash
# Use JSON files (local)
set DB_MODE=json

# Use MongoDB (cloud)
set DB_MODE=mongodb
```

---

## 8. Web Dashboard

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

## 9. Deployment to Render.com

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

## 10. Project Structure

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

## 11. Key Concepts

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

## 12. Contact

**Project Author:** Bala Anbalagan
**Email:** Bala.Anbalagan@sjsu.edu
**GitHub Repository:** https://github.com/BalaAnbalagan/reservoir_monitoring

For questions, issues, or feedback about this project, please contact via email or open an issue on GitHub.

---

**Built with Python, MQTT, Flask, and Cloud Services**
**Powered by:** HiveMQ Cloud, MongoDB Atlas, Render.com, and GitHub Actions
