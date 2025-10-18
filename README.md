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
- [3. Local Development Mode](#3-local-development-mode)
  - [3.1 Local Architecture](#31-local-architecture)
  - [3.2 Local Installation](#32-local-installation)
  - [3.3 Local Setup](#33-local-setup)
  - [3.4 Local Usage](#34-local-usage)
  - [3.5 Local Dashboard](#35-local-dashboard)
- [4. Cloud Production Mode](#4-cloud-production-mode)
  - [4.1 Cloud Architecture](#41-cloud-architecture)
  - [4.2 Cloud Setup & Configuration](#42-cloud-setup--configuration)
  - [4.3 Cloud Usage](#43-cloud-usage)
  - [4.4 Cloud Dashboard](#44-cloud-dashboard)
- [5. Project Structure](#5-project-structure)
- [6. Key Concepts](#6-key-concepts)
- [7. Contact](#7-contact)

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

**Key Concepts:**
- **Broker**: Central message hub (like WhatsApp server)
- **Publishers**: Devices that send messages (like senders)
- **Subscribers**: Devices that receive messages (like readers)
- **Topics**: Message channels (like group chats)
- **QoS**: Quality of Service - delivery guarantee levels

---

## 3. Local Development Mode

**When to use:** Development, testing, learning MQTT concepts, running without internet

**Benefits:**
- No cloud accounts needed
- Fast iteration and testing
- Complete control over infrastructure
- Learn MQTT concepts hands-on
- Works offline

---

### 3.1 Local Architecture

**System Diagram:**
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
│  │ API Pub.    │ ──┘     │ localhost:   │              │
│  │ (CDEC API)  │         │     1883     │              │
│  └─────────────┘         └──────────────┘              │
│                                 │                       │
│                                 ↓                       │
│                          ┌──────────────┐               │
│                          │  Subscriber  │               │
│                          │  (Collect &  │               │
│                          │   Generate)  │               │
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

**Components:**

1. **Mosquitto Broker** (localhost:1883)
   - Central message hub running on your machine
   - No authentication required
   - Lightweight and fast

2. **Publishers** (CSV-based or API-based)
   - Fetch data from CSV files or live CDEC API
   - Publish to topics: `SHASTA/WML`, `OROVILLE/WML`, etc.
   - Send JSON messages with water level data

3. **Subscriber**
   - Subscribes to all topics using wildcard: `+/WML`
   - Collects messages for specified duration
   - Generates comprehensive reports (JSON & TXT)
   - Saves to `reports/` directory

4. **Flask Web Dashboard**
   - Reads reports from `reports/` directory
   - Displays interactive charts and tables
   - Runs on localhost:5000

**Data Flow:**
```
CSV/API → Publisher → Mosquitto → Subscriber → JSON Files → Flask App → Browser
```

---

### 3.2 Local Installation

**Prerequisites:**
- Python 3.7+
- Mosquitto MQTT Broker
- Basic command line knowledge

**Step 1: Install Mosquitto Broker**

**Windows:**
```bash
# Download installer from https://mosquitto.org/download/
# Run the .exe installer
# Start the service
net start mosquitto
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

**macOS:**
```bash
brew install mosquitto
brew services start mosquitto
```

**Step 2: Verify Mosquitto Installation**
```bash
# Windows
sc query mosquitto

# Linux
sudo systemctl status mosquitto

# macOS
brew services list
```

**Step 3: Install Python Dependencies**
```bash
cd C:\myCodes\reservoir_monitoring
pip install -r requirements.txt
```

**Key packages installed:**
- `paho-mqtt` - MQTT client library
- `flask` - Web framework
- `requests` - HTTP library for API calls
- `gunicorn` - Production WSGI server

---

### 3.3 Local Setup

**Step 1: Prepare Data Files**

Your project already includes sample CSV files in the `data/` directory:
- `Shasta_WML.csv`
- `Oroville_WML.csv`
- `Sonoma_WML.csv`

**Step 2: Convert CSV to JSON (Optional)**
```bash
python csv_to_json.py
```

This creates JSON files for CSV-based testing.

**Step 3: Test MQTT Connection**
```bash
python test_mqtt.py local
```

**Expected output:**
```
[LOCAL] Using LOCAL MQTT: localhost
[SUCCESS] CONNECTION SUCCESSFUL!
   Connected to localhost:1883
```

---

### 3.4 Local Usage

**Complete Workflow:**

**Terminal 1: Start Subscriber**
```bash
# Listen for 60 seconds, then generate reports
python subscriber.py --duration 60
```

**Terminal 2: Start Publisher (within 60 seconds)**

**Option A: CSV-based (for testing)**
```bash
python publisher.py --reservoir ALL
```

**Option B: API-based (live CDEC data)**
```bash
# Fetch 7 days of data from CDEC API
python api_publisher.py --reservoir ALL --days 7
```

**Terminal 3: Start Web Dashboard**
```bash
python app.py
```

Visit: `http://localhost:5000`

**What Happens:**

1. **Subscriber** connects to Mosquitto and listens to `+/WML` topics
2. **Publisher** fetches data and publishes messages to specific topics
3. **Subscriber** collects all messages for 60 seconds
4. **Subscriber** generates reports:
   - `reports/comprehensive_report_*.json` (detailed data)
   - `reports/summary_report_*.txt` (human-readable)
5. **Flask app** reads JSON reports and displays dashboard

**Publisher Options:**

```bash
# Publish specific reservoir only
python publisher.py --reservoir SHASTA

# Publish to custom broker/port
python publisher.py --reservoir ALL --broker 192.168.1.100 --port 1884

# API publisher with specific days
python api_publisher.py --reservoir OROVILLE --days 14

# API publisher for all 21+ reservoirs
python api_publisher.py --reservoir ALL --days 7
```

**Subscriber Options:**

```bash
# Listen for 30 seconds (default)
python subscriber.py

# Listen for 2 minutes
python subscriber.py --duration 120

# Connect to custom broker
python subscriber.py --broker 192.168.1.100 --port 1884
```

---

### 3.5 Local Dashboard

**Starting the Dashboard:**
```bash
python app.py
```

The dashboard runs on **`http://localhost:5000`**

---

**Dashboard Features:**

#### 1. Summary View (`/`)

**URL:** `http://localhost:5000/`

**Features:**
- Total water storage across all reservoirs (TAF)
- Period changes (first vs last day) - Shows increase/decrease
- Number of active reservoirs
- Summary statistics cards with visual indicators
- Quick view charts:
  - Water Levels Over Time (line chart)
  - Current Levels Comparison (bar chart)
  - Total Capacity Trend (area chart)
- "View Detailed Analysis" button
- "Download JSON Data" button
- Last updated timestamp

**Data Shown:**
- Total Water Volume in TAF
- Period Change (positive/negative)
- Active Reservoirs count
- Reporting Period (days of data)

---

#### 2. Detailed View (`/detailed`)

**URL:** `http://localhost:5000/detailed`

**Features:**
- **Current Water Levels (Bar Chart)**
  - Sorted by capacity (largest first)
  - Color-coded bars for easy identification
  - Shows all 8 active reservoirs

- **Stacked Water Levels Over Time**
  - Complete time series visualization
  - All reservoirs stacked to show total capacity
  - Color-coded by reservoir
  - Shows 7 days of data trends

- **Water Level Changes Chart**
  - Green bars = water gains
  - Red bars = water losses
  - Day-over-day comparison

- **Toggleable Data Tables**
  - Detailed historical data tables
  - Hidden by default for clean view
  - Click "Show Tables" to expand
  - Complete day-by-day breakdown

**Navigation:**
- ← Back to Summary
- Interactive Charts (advanced view)
- Download JSON

---

#### 3. Advanced Charts (`/detailed/charts`)

**URL:** `http://localhost:5000/detailed/charts`

**Features:**
- Top 10 largest reservoirs (horizontal bar chart)
- Multi-day comparison with interactive controls
- Weekly comparison view
- First vs Last day analysis

---

#### 4. API Endpoints (for developers/integrations)

```
GET http://localhost:5000/api/summary          # Summary statistics (JSON)
GET http://localhost:5000/api/latest           # Latest day data (JSON)
GET http://localhost:5000/api/historical       # Complete historical data (JSON)
GET http://localhost:5000/api/changes          # Day-over-day changes (JSON)
GET http://localhost:5000/api/reservoir/<name> # Specific reservoir (JSON)
```

**Example API Usage:**
```bash
# Get summary statistics
curl http://localhost:5000/api/summary

# Get specific reservoir data
curl http://localhost:5000/api/reservoir/SHASTA

# Download historical data
curl http://localhost:5000/api/historical > data.json
```

---

**Technologies:**
- **Flask** - Python web framework
- **Chart.js** - Interactive JavaScript charts
- **Bootstrap** - Responsive CSS framework
- **Jinja2** - HTML templating engine
- **JSON** - Data storage and API responses

---

## 4. Cloud Production Mode

**When to use:** Production deployment, automated daily updates, no local infrastructure

**Benefits:**
- Completely free (using free tiers)
- Fully automated (no manual intervention)
- Professional cloud infrastructure
- Scalable and reliable
- Accessible from anywhere
- Automatic daily data updates

---

### 4.1 Cloud Architecture

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

**Components:**

1. **GitHub Actions** (Free CI/CD)
   - Runs daily at 8 AM UTC (midnight PST)
   - Executes publisher and subscriber scripts
   - No server costs

2. **CDEC API** (California Data Exchange Center)
   - Provides live reservoir data
   - Free public API
   - 21+ major reservoirs

3. **HiveMQ Cloud** (MQTT Broker)
   - Cloud-hosted MQTT broker
   - Secure TLS/SSL (port 8883)
   - Free tier: 100 connections, 10 GB/month
   - Global accessibility

4. **API Publisher** (GitHub Actions)
   - Fetches data from CDEC API
   - Publishes to HiveMQ Cloud
   - Runs automatically daily

5. **Subscriber** (GitHub Actions)
   - Collects messages from HiveMQ Cloud
   - Processes and aggregates data
   - Saves to MongoDB Atlas

6. **MongoDB Atlas** (Database)
   - Cloud NoSQL database
   - Free tier: 512 MB storage
   - Stores daily reports
   - No file commits needed

7. **Render.com** (Web Hosting)
   - Hosts Flask web app
   - Free tier: 750 hours/month
   - Auto-deploys from GitHub
   - Reads from MongoDB

8. **Flask Dashboard** (Web App)
   - Reads reports from MongoDB
   - Interactive visualizations
   - Publicly accessible

**Data Flow:**
```
Daily Schedule (8 AM UTC):
GitHub Actions triggers
    ↓
API Publisher fetches CDEC data
    ↓
Publishes to HiveMQ Cloud (TLS)
    ↓
Subscriber collects messages
    ↓
Saves to MongoDB Atlas
    ↓
Render.com Flask app reads MongoDB
    ↓
Users access live dashboard
```

**Why This Architecture?**
- **Zero Cost:** All services use free tiers
- **Zero Manual Work:** Fully automated daily updates
- **Professional:** Industry-standard cloud services
- **Scalable:** Can handle millions of data points
- **Reliable:** Cloud redundancy and uptime
- **Secure:** TLS/SSL encryption for MQTT

---

### 4.2 Cloud Setup & Configuration

**Prerequisites:**
- GitHub account
- Basic understanding of GitHub Actions
- 30 minutes for initial setup

**Cloud Services Required (All Free):**

| Service | Purpose | Free Tier | Sign Up Link |
|---------|---------|-----------|--------------|
| GitHub | Code hosting & CI/CD | Unlimited public repos | https://github.com |
| HiveMQ Cloud | MQTT Broker | 100 MB/month | https://console.hivemq.cloud |
| MongoDB Atlas | Database | 512 MB storage | https://www.mongodb.com/atlas |
| Render.com | Web hosting | 750 hours/month | https://render.com |

---

**Step 1: Setup HiveMQ Cloud**

1. Go to https://console.hivemq.cloud and sign up
2. Create a new cluster (select Free tier)
3. Wait 2-3 minutes for cluster provisioning
4. Note your cluster URL (e.g., `7f5a2a82095f4558a5ce236d5cbb146d.s1.eu.hivemq.cloud`)
5. Create credentials:
   - Click "Access Management"
   - Add new user (e.g., username: `wateradm`, password: `CAwater2025!`)
6. Save your credentials securely

---

**Step 2: Setup MongoDB Atlas**

1. Go to https://www.mongodb.com/atlas and sign up
2. Create a new cluster (select M0 Free tier)
3. Choose cloud provider and region (any will work)
4. Wait 5-10 minutes for cluster creation
5. Configure network access:
   - Click "Network Access"
   - Add IP: `0.0.0.0/0` (allow from anywhere)
6. Create database user:
   - Click "Database Access"
   - Add user (e.g., `reservoir_admin` with password)
7. Get connection string:
   - Click "Connect" → "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your actual password
   - Example: `mongodb+srv://reservoir_admin:zfUFiqhZgD48NO8W@reservoir-monitoring.lmdpkq6.mongodb.net/?retryWrites=true&w=majority`

---

**Step 3: Configure GitHub Secrets**

GitHub Secrets store sensitive credentials securely for GitHub Actions.

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Add these 5 secrets:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `MQTT_CLOUD_BROKER` | Your HiveMQ cluster URL | `7f5a2a82095f4558a5ce236d5cbb146d.s1.eu.hivemq.cloud` |
| `MQTT_CLOUD_PORT` | HiveMQ port | `8883` |
| `MQTT_CLOUD_USER` | HiveMQ username | `wateradm` |
| `MQTT_CLOUD_PASS` | HiveMQ password | `CAwater2025!` |
| `MONGODB_URI` | MongoDB connection string | `mongodb+srv://reservoir_admin:password@...` |

See [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md) for detailed instructions with screenshots.

---

**Step 4: Setup Render.com**

1. Go to https://render.com and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your `reservoir_monitoring` repository
5. Render auto-detects settings from `render.yaml`:
   - Name: `reservoir-monitoring`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
6. Add environment variables:
   - `DB_MODE`: `mongodb`
   - `MONGODB_URI`: Your MongoDB connection string
   - `FLASK_ENV`: `production`
7. Click **"Create Web Service"**
8. Wait 5-10 minutes for deployment
9. Your app will be live at: `https://your-app-name.onrender.com`

---

**Step 5: Verify GitHub Actions Workflow**

The project includes `.github/workflows/update-data.yml` which runs automatically.

**Check the workflow file:**
```yaml
name: Update Reservoir Data with Cloud MQTT
on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 8 AM UTC
  workflow_dispatch:      # Manual trigger
```

**Manual Test:**
1. Go to GitHub repository → **Actions** tab
2. Click "Update Reservoir Data with Cloud MQTT"
3. Click **"Run workflow"** dropdown → **"Run workflow"**
4. Watch the workflow execute (takes ~2-3 minutes)

**Expected output:**
```
✅ Set up environment
✅ Install dependencies
✅ Run subscriber (background)
✅ Run API publisher
✅ Wait for subscriber to finish
✅ Check MongoDB for saved reports
✅ Workflow completed
```

---

### 4.3 Cloud Usage

**Automated Daily Updates:**

Once configured, the system runs completely automatically:

1. **Every day at 8 AM UTC (midnight PST):**
   - GitHub Actions workflow triggers
   - Fetches live data from CDEC API for 21+ reservoirs
   - Publishes to HiveMQ Cloud via secure TLS
   - Subscriber collects messages for 90 seconds
   - Saves comprehensive reports to MongoDB Atlas
   - Render.com dashboard updates automatically

2. **No manual intervention required!**

**Monitoring:**

**GitHub Actions:**
- View workflow runs: Repository → Actions tab
- Check run history and logs
- See success/failure status
- View execution time (~2-3 minutes per run)

**MongoDB Atlas:**
- Login to MongoDB Atlas dashboard
- Navigate to Collections → `reservoir_monitoring` → `daily_reports`
- View stored reports (JSON documents)
- Check database size and metrics

**Render.com:**
- View deployment logs
- Monitor app status (running/sleeping)
- Check build history
- View app metrics

**HiveMQ Cloud:**
- View connection statistics
- Monitor message throughput
- Check client connections

---

**Manual Cloud Testing (Optional):**

You can also run the cloud workflow manually from your local machine:

**Set environment variables:**
```bash
# Windows
set MQTT_ENV=cloud
set MQTT_CLOUD_BROKER=your_hivemq_cluster.hivemq.cloud
set MQTT_CLOUD_USER=your_username
set MQTT_CLOUD_PASS=your_password
set DB_MODE=mongodb
set MONGODB_URI=your_mongodb_connection_string

# Linux/macOS
export MQTT_ENV=cloud
export MQTT_CLOUD_BROKER=your_hivemq_cluster.hivemq.cloud
export MQTT_CLOUD_USER=your_username
export MQTT_CLOUD_PASS=your_password
export DB_MODE=mongodb
export MONGODB_URI=your_mongodb_connection_string
```

**Test connection:**
```bash
python test_mqtt.py cloud
```

**Run publisher and subscriber:**
```bash
# Terminal 1: Start subscriber (90 seconds)
python subscriber.py --duration 90

# Terminal 2: Start API publisher
python api_publisher.py --reservoir ALL --days 7
```

**Check MongoDB:**
- Data should appear in MongoDB Atlas immediately
- Render.com dashboard will show updated data

---

### 4.4 Cloud Dashboard

**Live Production URL:** **`https://reservoir-monitoring.onrender.com`**

Share this URL with your professor or anyone to view the live dashboard!

---

**Important Notes:**
- **First Request:** If the app is sleeping (free tier), it takes ~30 seconds to wake up
- **Subsequent Requests:** Fast response times after initial wake-up
- **Data Source:** Real-time data from MongoDB Atlas
- **Updates:** Automatically updated daily at 8 AM UTC via GitHub Actions

---

**Dashboard Features:**

#### 1. Summary View (`/`)

**URL:** `https://reservoir-monitoring.onrender.com/`

**Features:**
- **Total Water Volume** - Aggregated across all active reservoirs (in TAF)
- **Period Change** - Shows net increase/decrease (red = loss, green = gain)
- **Active Reservoirs** - Count of reservoirs with current data (8 locations)
- **Reporting Period** - Number of days of data available (7 days)
- **Quick View Charts:**
  - Water Levels Over Time (line chart showing trends)
  - Current Levels Comparison (bar chart by reservoir)
  - Total Capacity Trend (area chart showing aggregate)
- **Action Buttons:**
  - "View Detailed Analysis" - Navigate to detailed charts
  - "Download JSON Data" - Export raw data
  - "Refresh Data" - Reload latest from MongoDB
- **Last Updated Timestamp** - Shows when data was last refreshed

**Live Data from MongoDB:**
- Reads directly from MongoDB Atlas cloud database
- No file commits needed for updates
- Instant data refresh on page load

---

#### 2. Detailed View (`/detailed`)

**URL:** `https://reservoir-monitoring.onrender.com/detailed`

**Features:**
- **Current Water Levels (Bar Chart)**
  - All 8 active reservoirs displayed
  - Sorted by capacity (SHASTA, NEW_MELONES, FOLSOM, etc.)
  - Color-coded bars for visual distinction
  - Shows current TAF values

- **Stacked Water Levels Over Time**
  - Complete 7-day time series
  - All reservoirs stacked to show total capacity
  - Color-coded layers by reservoir
  - Interactive tooltips on hover
  - Shows water distribution trends

- **Water Level Changes Chart**
  - Day-over-day comparison
  - Green bars = water gains
  - Red bars = water losses
  - Numerical values displayed

- **Toggleable Data Tables**
  - Click "Show Tables" to expand
  - Detailed historical data
  - Day-by-day breakdown for each reservoir
  - Complete TAF values

**Navigation:**
- ← Back to Summary
- 📊 Interactive Charts (advanced visualizations)
- Download JSON (export data)

---

#### 3. Advanced Charts (`/detailed/charts`)

**URL:** `https://reservoir-monitoring.onrender.com/detailed/charts`

**Features:**
- Top 10 largest reservoirs (horizontal bar chart)
- Multi-day comparison with interactive date controls
- Weekly comparison view
- First vs Last day analysis
- Custom date range selection

---

#### 4. API Endpoints (for developers/integrations)

**Base URL:** `https://reservoir-monitoring.onrender.com`

```
GET /api/summary          # Summary statistics (JSON)
GET /api/latest           # Latest day data (JSON)
GET /api/historical       # Complete historical data (JSON)
GET /api/changes          # Day-over-day changes (JSON)
GET /api/reservoir/<name> # Specific reservoir data (JSON)
```

**Example API Usage:**
```bash
# Get summary statistics
curl https://reservoir-monitoring.onrender.com/api/summary

# Get specific reservoir data
curl https://reservoir-monitoring.onrender.com/api/reservoir/SHASTA

# Get historical data for all reservoirs
curl https://reservoir-monitoring.onrender.com/api/historical

# Get day-over-day changes
curl https://reservoir-monitoring.onrender.com/api/changes
```

**Example JSON Response:**
```json
{
  "total_water_taf": 5587.8,
  "period_change_taf": -19.8,
  "active_reservoirs": 8,
  "reporting_days": 7,
  "last_updated": "2025-10-18T11:29:00"
}
```

---

**Data Updates:**
- ✅ Automatic daily updates at 8 AM UTC (midnight PST)
- ✅ GitHub Actions fetches fresh data from CDEC API
- ✅ Data saved directly to MongoDB Atlas
- ✅ Dashboard reads from MongoDB (no rebuild needed)
- ✅ Always shows latest available data

**Performance:**
- Fast MongoDB queries (optimized indexes)
- Responsive design (mobile-friendly)
- Interactive Chart.js visualizations
- Free tier limitations:
  - App sleeps after 15 minutes of inactivity
  - ~30 seconds wake-up time on first request
  - 750 hours/month free

**Sharing with Professor:**
Simply share this URL: **`https://reservoir-monitoring.onrender.com`**

✅ No login required
✅ Publicly accessible
✅ Professional presentation
✅ Live data from MongoDB
✅ Automated daily updates

---


## 5. Project Structure

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
│   ├── detailed.html              # Detailed view with charts/tables
│   └── detailed_charts.html       # Advanced interactive charts
│
├── reports/                        # Generated reports (local mode)
│   ├── comprehensive_report_*.json # Detailed JSON reports
│   └── summary_report_*.txt        # Human-readable summaries
│
├── screenshots/                    # Dashboard screenshots (artifacts)
│   ├── README.md                  # Screenshot guidelines
│   ├── local_summary_view.png     # Local dashboard summary
│   ├── local_detailed_view.png    # Local dashboard detailed view
│   ├── cloud_summary_view.png     # Cloud dashboard summary
│   ├── cloud_detailed_view.png    # Cloud dashboard detailed view
│   └── *.png                      # Additional screenshots
│
├── .github/workflows/              # GitHub Actions
│   └── update-data.yml            # Daily automated updates
│
├── mqtt_config.py                  # MQTT configuration (local/cloud)
├── db_config.py                    # Database manager (JSON/MongoDB)
├── app.py                          # Flask web application
├── api_publisher.py                # Live API data publisher
├── publisher.py                    # MQTT publisher (CSV-based)
├── subscriber.py                   # MQTT subscriber (data collector)
├── csv_to_json.py                  # CSV to JSON converter
├── test_mqtt.py                    # MQTT connection testing tool
│
├── requirements.txt                # Python dependencies
├── runtime.txt                     # Python version for deployment
├── render.yaml                     # Render.com configuration
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
│
├── MQTT_SETUP_GUIDE.md            # MQTT setup documentation
├── GITHUB_SECRETS_SETUP.md        # GitHub secrets documentation
├── WEB_DASHBOARD_GUIDE.md         # Dashboard documentation
└── README.md                       # This file
```

---

## 5.1. Dashboard Screenshots (Artifacts)

Visual examples of the dashboard in action are available in the [`screenshots/`](screenshots/) directory.

### Local Dashboard Screenshots:
- **Summary View:** See [`screenshots/local_summary_view.png`](screenshots/local_summary_view.png)
- **Detailed View:** See [`screenshots/local_detailed_view.png`](screenshots/local_detailed_view.png)

### Cloud Dashboard Screenshots:
- **Summary View:** See [`screenshots/cloud_summary_view.png`](screenshots/cloud_summary_view.png)
- **Detailed View:** See [`screenshots/cloud_detailed_view.png`](screenshots/cloud_detailed_view.png)

**Note:** To add your own screenshots, follow the instructions in [`screenshots/README.md`](screenshots/README.md)

---

## 6. Key Concepts

### MQTT Topics

Topics are like **channels** or **hashtags**:
- `SHASTA/WML` - Shasta water mark level
- `OROVILLE/WML` - Oroville water mark level
- `+/WML` - Wildcard subscription (all reservoirs)

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

### Environment Variables

**Local Mode:**
- `MQTT_ENV=local` (default)
- `DB_MODE=json` (default)

**Cloud Mode:**
- `MQTT_ENV=cloud`
- `MQTT_CLOUD_BROKER` - HiveMQ cluster URL
- `MQTT_CLOUD_USER` - HiveMQ username
- `MQTT_CLOUD_PASS` - HiveMQ password
- `DB_MODE=mongodb`
- `MONGODB_URI` - MongoDB connection string

---

## 7. Contact

**Project Author:** Bala Anbalagan
**Email:** Bala.Anbalagan@sjsu.edu
**GitHub Repository:** https://github.com/BalaAnbalagan/reservoir_monitoring

For questions, issues, or feedback about this project, please contact via email or open an issue on GitHub.

---

**Built with Python, MQTT, Flask, and Cloud Services**
**Powered by:** HiveMQ Cloud, MongoDB Atlas, Render.com, and GitHub Actions
