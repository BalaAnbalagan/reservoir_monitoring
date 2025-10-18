# California Reservoir Monitoring System
## Project Submission Document

**Student:** Bala Anbalagan
**Email:** Bala.Anbalagan@sjsu.edu
**Date:** October 18, 2025
**Course:** IoT/MQTT Assignment

---

## Executive Summary

This project implements a real-time water level monitoring system for California reservoirs using MQTT protocol. The system demonstrates a complete IoT architecture with multiple publishers, a single subscriber collecting data from all reservoirs, and an interactive web dashboard for data visualization.

**Key Achievement:** Single subscriber architecture collecting data from 8+ California reservoirs using MQTT wildcard subscriptions.

---

## Live Deployment

### Cloud Production Dashboard (Recommended)
**URL:** https://reservoir-monitoring.onrender.com

**Features:**
- ✅ Live data from California Data Exchange Center (CDEC) API
- ✅ Automated daily updates via GitHub Actions
- ✅ MongoDB Atlas cloud database
- ✅ HiveMQ Cloud MQTT broker with TLS/SSL
- ✅ Publicly accessible (no login required)
- ✅ Interactive Chart.js visualizations

**Dashboard Views:**
- Summary: https://reservoir-monitoring.onrender.com/
- Detailed Analysis: https://reservoir-monitoring.onrender.com/detailed
- API Endpoints: https://reservoir-monitoring.onrender.com/api/summary

**Note:** First request may take 30 seconds to wake up (free tier limitation). Subsequent requests are fast.

---

## GitHub Repository

**URL:** https://github.com/BalaAnbalagan/reservoir_monitoring

**Repository Contents:**
- Complete source code
- Documentation (README.md with 1000+ lines)
- Dashboard screenshots (6 high-quality PNG files)
- MQTT configuration for local and cloud
- GitHub Actions workflow for automation
- Deployment configurations (Render.com)

---

## Architecture Overview

### Core Design Pattern: Single Subscriber

```
Multiple Publishers          MQTT Broker          Single Subscriber
┌─────────────┐             ┌──────────┐         ┌──────────────┐
│  SHASTA     │──SHASTA/WML→│          │         │              │
└─────────────┘             │          │         │    Single    │
                            │ Broker   │────────→│  Subscriber  │
┌─────────────┐             │          │         │              │
│  OROVILLE   │──OROVILLE/..│          │         │  Listens to  │
└─────────────┘             │          │         │   +/WML      │
                            │          │         │  (wildcard)  │
┌─────────────┐             │          │         │              │
│  8+ More    │──.../WML───→│          │         │  Generates   │
└─────────────┘             └──────────┘         │   Report     │
                                                 └──────────────┘
```

**Key Points:**
- ✅ **ONE subscriber** collects data from ALL reservoirs
- ✅ Uses wildcard subscription: `+/WML` (matches all topics ending in /WML)
- ✅ Generates ONE comprehensive report for all reservoirs
- ✅ Efficient MQTT pattern demonstrating pub/sub architecture

---

## System Components

### 1. MQTT Protocol Implementation

**Local Mode (Development):**
- Mosquitto broker on localhost:1883
- No authentication
- JSON file storage
- For testing and development

**Cloud Mode (Production):**
- HiveMQ Cloud broker (port 8883)
- TLS/SSL encryption
- Username/password authentication
- MongoDB Atlas storage
- Automated via GitHub Actions

### 2. Publishers (Multiple)
- CSV-based publisher (for testing)
- API-based publisher (live CDEC data)
- Publishes to topics: `RESERVOIR_ID/WML`
- Supports 21+ California reservoirs

### 3. Subscriber (Single - Key Requirement)
- **Wildcard subscription:** `+/WML`
- Collects messages from all reservoirs
- Aggregates data into single report
- Saves to JSON (local) or MongoDB (cloud)

### 4. Web Dashboard
- Flask-based Python web application
- Interactive Chart.js visualizations
- Three views: Summary, Detailed, Advanced
- RESTful API endpoints

### 5. Database
- **Local:** JSON files in `reports/` directory
- **Cloud:** MongoDB Atlas (512 MB free tier)

### 6. Automation
- GitHub Actions workflow
- Runs daily at 8 AM UTC
- Fetches data, publishes via MQTT, saves to MongoDB
- Zero manual intervention

---

## Technical Specifications

### Technologies Used
- **Language:** Python 3.11
- **MQTT Library:** paho-mqtt
- **Web Framework:** Flask
- **Database:** MongoDB Atlas (cloud), JSON (local)
- **Visualization:** Chart.js
- **MQTT Brokers:** Mosquitto (local), HiveMQ Cloud (production)
- **CI/CD:** GitHub Actions
- **Hosting:** Render.com (free tier)

### Data Sources
- **Primary:** California Data Exchange Center (CDEC) API
- **Reservoirs Monitored:** 21+ major California reservoirs
- **Data Points:** Water levels in TAF (Thousand Acre-Feet)
- **Update Frequency:** Daily (automated)
- **Historical Data:** 7 days rolling window

### Message Format (JSON)
```json
{
  "reservoir_id": "SHASTA",
  "date": "10/18/2025",
  "water_level_taf": 2587.8,
  "timestamp": "2025-10-18T00:00:00",
  "published_at": "2025-10-18T11:29:00"
}
```

---

## Project Artifacts

### 1. Documentation
- **README.md** - Comprehensive 1000+ line documentation
- **MQTT_SETUP_GUIDE.md** - MQTT broker setup instructions
- **GITHUB_SECRETS_SETUP.md** - Automation configuration guide
- **WEB_DASHBOARD_GUIDE.md** - Dashboard feature documentation

### 2. Screenshots (in `screenshots/` directory)

**Local Dashboard:**
- `local_summary_view.png` - Summary dashboard (localhost:5000)
- `local_detailed_view.png` - Detailed analysis with charts
- `local_detailed_stacked_chart.png` - Closeup of stacked chart

**Cloud Dashboard:**
- `cloud_summary_view.png` - Live production summary
- `cloud_detailed_view.png` - Live production detailed view
- `cloud_detailed_stacked_chart.png` - Closeup of cloud chart

### 3. Source Code
- `app.py` - Flask web application (248 lines)
- `subscriber.py` - MQTT subscriber with wildcard (350+ lines)
- `publisher.py` - CSV-based MQTT publisher
- `api_publisher.py` - Live API data publisher
- `mqtt_config.py` - Dual MQTT configuration (local/cloud)
- `db_config.py` - Database manager (JSON/MongoDB)
- `test_mqtt.py` - Connection testing tool

### 4. Configuration Files
- `requirements.txt` - Python dependencies
- `render.yaml` - Render.com deployment config
- `.github/workflows/update-data.yml` - GitHub Actions workflow
- `.env.example` - Environment variables template

---

## Key Features Demonstrated

### MQTT Concepts
✅ **Publish/Subscribe Pattern** - Multiple publishers, single subscriber
✅ **Topics and Wildcards** - `RESERVOIR_ID/WML` topics, `+/WML` wildcard
✅ **Quality of Service (QoS)** - QoS 1 for guaranteed delivery
✅ **Message Broker** - Central hub for all communications
✅ **Persistent Connections** - Long-lived subscriber connection

### IoT Architecture
✅ **Sensor Simulation** - Multiple reservoir sensors publishing data
✅ **Data Aggregation** - Single subscriber collecting all data
✅ **Cloud Integration** - HiveMQ Cloud, MongoDB Atlas, Render.com
✅ **Security** - TLS/SSL encryption, authentication
✅ **Scalability** - Easy to add new reservoirs (wildcard subscription)

### Software Engineering
✅ **Version Control** - Git with comprehensive commit history
✅ **CI/CD** - GitHub Actions for automated deployment
✅ **Documentation** - Extensive README and guides
✅ **Testing** - MQTT connection testing utilities
✅ **Configuration Management** - Environment-based configs

### Data Visualization
✅ **Interactive Charts** - Bar charts, stacked charts, line graphs
✅ **Responsive Design** - Mobile-friendly dashboard
✅ **Multiple Views** - Summary, detailed, and advanced charts
✅ **RESTful API** - JSON endpoints for data access
✅ **Real-time Updates** - Fresh data from MongoDB

---

## Deployment Architecture

### Cloud Production (Current State)

```
┌─────────────────────────────────────────────────────┐
│  GitHub Actions (Daily 8 AM UTC)                    │
│                                                      │
│  1. Fetch data from CDEC API                        │
│  2. Publish to HiveMQ Cloud (TLS)                   │
│  3. Subscriber collects messages                    │
│  4. Save to MongoDB Atlas                           │
│                                                      │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  Render.com                                         │
│                                                      │
│  Flask App reads from MongoDB                       │
│  Serves dashboard at:                               │
│  https://reservoir-monitoring.onrender.com          │
│                                                      │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  Users / Professor Access                           │
│                                                      │
│  View live dashboard                                │
│  No login required                                  │
│  Public access                                      │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**All services use FREE tiers - Zero cost operation!**

---

## Assignment Requirements Fulfillment

| Requirement | Status | Evidence |
|-------------|--------|----------|
| MQTT Publishers | ✅ Complete | Multiple publishers (CSV + API based) |
| MQTT Subscriber | ✅ Complete | **Single subscriber** with wildcard `+/WML` |
| Topics | ✅ Complete | `RESERVOIR_ID/WML` format for all reservoirs |
| JSON Format | ✅ Complete | All messages in standardized JSON |
| Data Collection | ✅ Complete | Collects from 8+ active reservoirs |
| Report Generation | ✅ Complete | Comprehensive JSON and TXT reports |
| TAF Measurements | ✅ Complete | Water levels in Thousand Acre-Feet |
| Single Subscriber | ✅ **CRITICAL** | ONE subscriber collects ALL reservoir data |

**Most Important:** The system uses **ONE subscriber** that collects data from **ALL reservoirs** using a wildcard subscription (`+/WML`), demonstrating the efficiency and scalability of MQTT pub/sub architecture.

---

## Testing & Verification

### Local Testing
1. Start Mosquitto broker: `net start mosquitto`
2. Run subscriber: `python subscriber.py --duration 60`
3. Run publisher: `python api_publisher.py --reservoir ALL --days 7`
4. View dashboard: http://localhost:5000
5. Check reports in `reports/` directory

### Cloud Testing
1. Visit: https://reservoir-monitoring.onrender.com
2. View summary dashboard with live data
3. Navigate to detailed analysis
4. Check GitHub Actions runs in repository
5. Verify MongoDB Atlas has data

### API Testing
```bash
# Get summary statistics
curl https://reservoir-monitoring.onrender.com/api/summary

# Get specific reservoir
curl https://reservoir-monitoring.onrender.com/api/reservoir/SHASTA

# Get all historical data
curl https://reservoir-monitoring.onrender.com/api/historical
```

---

## Performance Metrics

### Current System Stats
- **Active Reservoirs:** 8 locations
- **Total Water Volume:** 5,587.8 TAF
- **Data Points:** 56 readings (8 reservoirs × 7 days)
- **Update Frequency:** Daily at 8 AM UTC
- **Response Time:** < 2 seconds (after wake-up)
- **Uptime:** 99%+ (Render.com free tier)

### Resource Usage
- **GitHub Actions:** ~3 minutes per run
- **MongoDB Storage:** < 1 MB of 512 MB free tier
- **Render.com:** < 1% of 750 hours/month free tier
- **HiveMQ Cloud:** < 1% of 100 MB/month free tier

**Total Monthly Cost:** $0.00 (all free tiers)

---

## Future Enhancements

Potential improvements for the system:
- Add email/SMS alerts for critical water levels
- Implement predictive analytics using machine learning
- Add authentication for admin features
- Create mobile app (React Native/Flutter)
- Integrate weather API for correlation analysis
- Add real-time WebSocket updates
- Implement data export to Excel/CSV
- Add user-configurable alert thresholds

---

## Conclusion

This project successfully demonstrates a complete MQTT-based IoT system with:
- **Single subscriber architecture** (key requirement)
- Multiple publishers sending data to specific topics
- Wildcard subscriptions for scalable data collection
- Both local development and cloud production deployments
- Professional web dashboard with interactive visualizations
- Automated data updates with zero manual intervention
- Comprehensive documentation and artifacts

The system is fully functional, deployed to the cloud, and accessible for review at:

**https://reservoir-monitoring.onrender.com**

---

## Contact Information

**Student:** Bala Anbalagan
**Email:** Bala.Anbalagan@sjsu.edu
**GitHub:** https://github.com/BalaAnbalagan
**Repository:** https://github.com/BalaAnbalagan/reservoir_monitoring

**Submission Date:** October 18, 2025

---

## Quick Links Summary

| Resource | URL |
|----------|-----|
| Live Dashboard | https://reservoir-monitoring.onrender.com |
| Detailed View | https://reservoir-monitoring.onrender.com/detailed |
| API Summary | https://reservoir-monitoring.onrender.com/api/summary |
| GitHub Repository | https://github.com/BalaAnbalagan/reservoir_monitoring |
| Documentation | https://github.com/BalaAnbalagan/reservoir_monitoring/blob/main/README.md |
| Screenshots | https://github.com/BalaAnbalagan/reservoir_monitoring/tree/main/screenshots |

---

**Thank you for reviewing this project!**

This document can be converted to PDF for formal submission or printed for reference.
