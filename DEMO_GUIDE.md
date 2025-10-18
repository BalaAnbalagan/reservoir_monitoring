# Reservoir Monitoring System - Demonstration Guide

## How to Demonstrate This Project

This guide explains how the system works and how to demonstrate it for your assignment.

---

## System Overview

### What This System Does:

1. **Fetches Real-Time Data** from California CDEC API
2. **Publishes Data** via MQTT Protocol to topics
3. **Collects Data** using a single subscriber
4. **Generates Reports** in JSON and text format
5. **Creates Visualizations** - charts and interactive dashboard

### Technologies Used:

- **Python** - Programming language
- **MQTT (Mosquitto)** - Message broker protocol
- **CDEC API** - California water data source
- **Matplotlib** - Chart generation
- **HTML/CSS** - Interactive dashboard

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    CDEC API (California)                      │
│            https://cdec.water.ca.gov/dynamicapp/              │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ HTTP Request
                         ↓
┌──────────────────────────────────────────────────────────────┐
│                   API Publisher (Python)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Fetches data for 21 major reservoirs:               │   │
│  │  - Shasta, Oroville, Trinity, Folsom, etc.           │   │
│  │  - Converts AF → TAF                                 │   │
│  │  - Formats as JSON messages                          │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ MQTT Publish
                         ↓
┌──────────────────────────────────────────────────────────────┐
│              MQTT Broker (Mosquitto)                          │
│                                                                │
│  Topics:                                                       │
│  • SHASTA/WML        • OROVILLE/WML     • TRINITY/WML        │
│  • FOLSOM/WML        • DON_PEDRO/WML    • NEW_MELONES/WML    │
│  • + 15 more reservoirs...                                    │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ MQTT Subscribe (+/WML)
                         ↓
┌──────────────────────────────────────────────────────────────┐
│                 Subscriber (Python)                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  - Subscribes to ALL reservoir topics                │   │
│  │  - Collects all messages                             │   │
│  │  - Aggregates by date and reservoir                  │   │
│  │  - Calculates statistics (avg, min, max)             │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ Generate Reports
                         ↓
┌──────────────────────────────────────────────────────────────┐
│                    Report Files                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • comprehensive_report.json  (machine-readable)     │   │
│  │  • summary_report.txt         (human-readable)       │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ Visualization
                         ↓
┌──────────────────────────────────────────────────────────────┐
│            Visualizations & Dashboard                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Time series charts (PNG)                          │   │
│  │  • Comparison bar charts (PNG)                       │   │
│  │  • Total capacity charts (PNG)                       │   │
│  │  • Interactive HTML dashboard                        │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Demonstration

### Step 1: Show the Data Source (CDEC API)

**What to Say:**
> "California provides public APIs for reservoir data through the California Data Exchange Center (CDEC). We can query this API to get real-time water levels for any reservoir in the state."

**Demo Command:**
```bash
# Show API in action - fetch Shasta data
curl "https://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?Stations=SHA&SensorNums=15&dur_code=D&Start=2024-10-01&End=2024-10-10"
```

**Expected Output:**
```
STATION_ID,DURATION,SENSOR_NUMBER,SENSOR_TYPE,DATE TIME,OBS DATE,VALUE,DATA_FLAG,UNITS
SHA,D,15,STORAGE,20241001 0000,20241001 0000,2760766, ,AF
SHA,D,15,STORAGE,20241002 0000,20241002 0000,2758203, ,AF
...
```

**Explain:**
- `SHA` = Shasta reservoir station code
- `15` = Sensor number for storage/water level
- `D` = Daily data
- Value is in Acre-Feet (AF), we convert to TAF (Thousand Acre-Feet)

---

### Step 2: Start the MQTT Broker

**What to Say:**
> "MQTT is a lightweight messaging protocol perfect for IoT devices. Mosquitto is the broker that routes messages between publishers and subscribers."

**Demo Command:**
```bash
# Check if Mosquitto is running
sc query mosquitto
```

**Expected Output:**
```
SERVICE_NAME: mosquitto
STATE      : 4  RUNNING
```

**Explain:**
- Mosquitto acts as the "post office" for messages
- Publishers send messages to topics
- Subscribers receive messages from topics
- Runs on port 1883 (default MQTT port)

---

### Step 3: Start the Subscriber

**What to Say:**
> "The subscriber is our data collector. It listens to ALL reservoir topics using MQTT wildcards and aggregates the data."

**Demo Command:**
```bash
# Start subscriber in background (60 seconds)
python subscriber.py --duration 60
```

**Expected Output:**
```
Starting MQTT subscriber...
Connected to MQTT Broker at localhost:1883
Subscribing to all reservoir topics...
  -> Subscribed to: +/WML (all reservoirs)

Listening for messages...
```

**Explain:**
- `+/WML` is a wildcard pattern
- `+` matches any reservoir name
- Automatically subscribes to all current and future reservoirs
- Will collect data for 60 seconds

---

### Step 4: Publish Live Data from API

**What to Say:**
> "Now we'll fetch live data from the CDEC API and publish it to our MQTT broker. This simulates sensors at each reservoir sending data."

**Demo Command:**
```bash
# Fetch and publish data for specific reservoirs
python api_publisher.py --reservoir SHASTA,OROVILLE,FOLSOM --days 7

# OR fetch ALL 21 reservoirs
python api_publisher.py --reservoir ALL --days 7
```

**Expected Output:**
```
============================================================
FETCHING REAL-TIME DATA FROM CDEC API
============================================================
Date Range: 2024-10-11 to 2024-10-18
Reservoirs: SHASTA, OROVILLE, FOLSOM

Processing SHASTA (Station: SHA)
Fetching data from CDEC API...
  -> Fetched 7 records

Publishing data for SHASTA to topic: SHASTA/WML
Published: 10/11/2024 - 2636.8 TAF
Published: 10/12/2024 - 2629.67 TAF
...
```

**Explain:**
- Connects to CDEC API for each reservoir
- Converts data to JSON format
- Publishes to MQTT topics like `SHASTA/WML`
- Each message contains: date, water level (TAF), timestamp

---

### Step 5: View Collected Data and Reports

**What to Say:**
> "After the subscriber finishes collecting, it generates comprehensive reports with statistics for each day and reservoir."

**Show Reports:**
```bash
# View text summary
cat reports/summary_report_*.txt

# View JSON data
cat reports/comprehensive_report_*.json
```

**Point Out:**
- Daily summaries for each reservoir
- Average, min, max water levels
- Total readings count
- Total water across all reservoirs

---

### Step 6: Generate Visualizations

**What to Say:**
> "Raw data is hard to interpret. Let's create visual charts to see trends and comparisons."

**Demo Command:**
```bash
# Generate all charts
python visualize.py
```

**Expected Output:**
```
============================================================
GENERATING VISUALIZATIONS
============================================================

1. Water Levels Over Time...
Chart saved to: reports/visualizations/water_levels_timeseries_*.png

2. Current Levels Comparison...
Chart saved to: reports/visualizations/water_levels_comparison_*.png

3. Total Capacity Over Time...
Chart saved to: reports/visualizations/total_capacity_*.png
```

**Show Charts:**
- Open the PNG files
- Point out:
  - Time series shows trends over time
  - Bar chart compares current levels
  - Area chart shows total capacity

---

### Step 7: Generate Interactive Dashboard

**What to Say:**
> "Finally, let's create an interactive web dashboard that combines everything - stats, charts, and detailed data tables."

**Demo Command:**
```bash
# Generate HTML dashboard
python generate_dashboard.py
```

**Expected Output:**
```
Dashboard generated: reports/dashboard_20241018_011156.html
Open in browser: C:\myCodes\reservoir_monitoring\reports\dashboard_20241018_011156.html
```

**Open Dashboard:**
```bash
start reports/dashboard_*.html
```

**Show Features:**
1. **Header** - Professional title
2. **Stats Cards** - Total water, active reservoirs, days, readings
3. **Charts** - Embedded visualizations
4. **Data Table** - Sortable daily data
5. **Color Coding** - Each reservoir has unique color
6. **Responsive** - Works on all screen sizes

---

## Supported Reservoirs (21 Total)

| Reservoir | Station Code | Region |
|-----------|--------------|--------|
| Shasta | SHA | Northern CA |
| Oroville | ORO | Northern CA |
| Trinity | CLR | Northern CA |
| Folsom | FOL | Sacramento Valley |
| New Melones | NML | Central CA |
| Don Pedro | DNP | Central CA |
| New Bullards Bar | NBB | Northern CA |
| San Luis | SLS | Central CA |
| Cachuma | CCH | Southern CA |
| Castaic | CAS | Southern CA |
| Casitas | CST | Southern CA |
| Diamond Valley | DMV | Southern CA |
| Millerton | MIL | Central CA |
| Pine Flat | PNF | Central CA |
| Sonoma | SLT | Northern CA |
| McClure | MCL | Central CA |
| Berryessa | BER | Northern CA |
| Camanche | CMN | Central CA |
| Isabella | ISB | Central CA |
| Perris | PRR | Southern CA |
| Exchequer | EXC | Central CA |

---

## Key Features to Highlight

### 1. Real-Time Data
- Fetches live data from California state API
- Not simulated - actual reservoir levels
- Updates available daily

### 2. Scalable Architecture
- MQTT allows unlimited sensors/publishers
- Single subscriber handles all reservoirs
- Easy to add new reservoirs

### 3. MQTT Protocol Benefits
- **Lightweight** - Works on IoT devices
- **Reliable** - QoS guarantees delivery
- **Decoupled** - Publishers don't need to know about subscribers
- **Wildcard Topics** - Subscribe to multiple topics at once

### 4. Data Aggregation
- Collects from multiple sources
- Calculates statistics automatically
- Organizes by date and reservoir

### 5. Multiple Output Formats
- **JSON** - Machine-readable for further processing
- **TXT** - Human-readable summaries
- **PNG** - Charts for presentations
- **HTML** - Interactive dashboards

---

## Common Questions & Answers

**Q: Why use MQTT instead of a database?**
> A: MQTT is designed for real-time streaming data and IoT devices. It allows sensors to publish data even with unreliable connections, and multiple subscribers can receive the same data without coordinating.

**Q: How does the wildcard subscription work?**
> A: The `+/WML` pattern means "any reservoir name followed by /WML". So it automatically subscribes to SHASTA/WML, OROVILLE/WML, etc. without listing them individually.

**Q: What if a reservoir has no data?**
> A: The API publisher skips reservoirs with missing data (shown as `---` in the API) and only publishes valid readings.

**Q: Can we add more reservoirs?**
> A: Yes! Just add the station code to the `RESERVOIR_STATIONS` dictionary in api_publisher.py. The subscriber automatically handles it.

**Q: How is data stored?**
> A: The subscriber collects data in memory, then writes JSON and text reports when finished. For long-term storage, you could add a database.

---

## Tips for Demonstration

1. **Start Simple** - Show just SHASTA first, then add more
2. **Show Live Data** - Run API publisher to prove it's real
3. **Explain MQTT** - Use the "group chat" analogy
4. **Show Dashboard** - Visual impact is powerful
5. **Highlight TAF** - Explain the water measurement unit
6. **Compare to Image** - Show how your dashboard matches the official one

---

## Quick Demo Script (5 minutes)

```bash
# Terminal 1: Start subscriber (background)
python subscriber.py --duration 60 &

# Terminal 2: Fetch live data
python api_publisher.py --reservoir SHASTA,OROVILLE,FOLSOM --days 7

# Wait for subscriber to finish (60 seconds)

# Generate visualizations
python visualize.py

# Create dashboard
python generate_dashboard.py

# Open in browser
start reports/dashboard_*.html
```

---

## Complete Demo Script (15 minutes)

```bash
# 1. Show API (1 min)
curl "https://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?Stations=SHA&SensorNums=15&dur_code=D&Start=2024-10-01&End=2024-10-10"

# 2. Check Mosquitto (30 sec)
sc query mosquitto

# 3. Start subscriber (30 sec)
python subscriber.py --duration 90 &

# 4. Fetch ALL reservoirs (3 min)
python api_publisher.py --reservoir ALL --days 7

# 5. Wait and show reports (2 min)
# Wait 90 seconds for subscriber to finish
cat reports/summary_report_*.txt

# 6. Generate charts (2 min)
python visualize.py

# 7. Create dashboard (1 min)
python generate_dashboard.py

# 8. Show dashboard (5 min)
start reports/dashboard_*.html
# Walk through features
```

---

## Project Structure Summary

```
reservoir_monitoring/
├── data/                      # Sample CSV data
├── reports/                   # Generated reports
│   ├── visualizations/       # PNG charts
│   ├── *.json               # JSON reports
│   ├── *.txt                # Text summaries
│   └── *.html               # Dashboards
├── csv_to_json.py            # CSV converter
├── publisher.py              # CSV-based publisher
├── api_publisher.py          # Live API publisher (NEW!)
├── subscriber.py             # Data collector
├── visualize.py              # Chart generator (NEW!)
├── generate_dashboard.py     # Dashboard creator (NEW!)
├── requirements.txt          # Dependencies
├── README.md                 # Full documentation
└── DEMO_GUIDE.md            # This file
```

---

## Assignment Checklist

- [x] MQTT publisher sending to RESERVOIR_ID/WML topics
- [x] MQTT subscriber collecting from all topics
- [x] JSON data model
- [x] CSV to JSON conversion
- [x] Single subscriber generating daily reports
- [x] TAF (Thousand Acre-Feet) measurements
- [x] Aggregated data from multiple reservoirs
- [x] **BONUS:** Real-time API integration
- [x] **BONUS:** Data visualization
- [x] **BONUS:** Interactive dashboard
- [x] **BONUS:** 21+ reservoirs supported

---

**Good luck with your demonstration!**
