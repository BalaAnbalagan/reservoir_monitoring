# Quick Reference Card - Reservoir Monitoring System

## Essential Commands

### 1. Test with Live API Data (Recommended)
```bash
# Terminal 1: Start subscriber
python subscriber.py --duration 90

# Terminal 2: Fetch live data (within 90 seconds)
python api_publisher.py --reservoir SHASTA,OROVILLE,FOLSOM --days 7

# Generate visualizations
python visualize.py

# Create dashboard
python generate_dashboard.py

# Open dashboard
start reports/dashboard_*.html
```

### 2. Test with CSV Data (Offline Demo)
```bash
# Convert CSV to JSON
python csv_to_json.py

# Start subscriber
python subscriber.py --duration 60

# Publish CSV data (within 60 seconds)
python publisher.py --reservoir ALL

# Generate visualizations
python visualize.py

# Create dashboard
python generate_dashboard.py
```

### 3. Fetch ALL 21 Reservoirs
```bash
python api_publisher.py --reservoir ALL --days 7
```

---

## File Locations

| File Type | Location | Purpose |
|-----------|----------|---------|
| JSON Reports | `reports/comprehensive_report_*.json` | Machine-readable data |
| Text Reports | `reports/summary_report_*.txt` | Human-readable summary |
| Charts | `reports/visualizations/*.png` | PNG images |
| Dashboard | `reports/dashboard_*.html` | Interactive web page |

---

## API Publisher Options

```bash
# Specific reservoirs (comma-separated)
python api_publisher.py --reservoir SHASTA,OROVILLE

# All reservoirs
python api_publisher.py --reservoir ALL

# Custom date range (14 days)
python api_publisher.py --reservoir ALL --days 14

# Remote MQTT broker
python api_publisher.py --reservoir ALL --broker 192.168.1.100
```

---

## Supported Reservoirs (21 Total)

```python
SHASTA, OROVILLE, TRINITY, FOLSOM, NEW_MELONES, DON_PEDRO,
NEW_BULLARDS_BAR, SAN_LUIS, CACHUMA, CASTAIC, CASITAS,
DIAMOND_VALLEY, MILLERTON, PINE_FLAT, SONOMA, MCCLURE,
BERRYESSA, CAMANCHE, ISABELLA, PERRIS, EXCHEQUER
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Start Mosquitto: `net start mosquitto` |
| "No module 'paho'" | Install: `pip install -r requirements.txt` |
| No messages received | Start subscriber BEFORE publisher |
| Port 1883 in use | Check: `sc query mosquitto` |

---

## MQTT Topics Pattern

```
RESERVOIR_NAME/WML

Examples:
- SHASTA/WML
- OROVILLE/WML
- FOLSOM/WML

Subscriber uses wildcard: +/WML (matches all)
```

---

## Key Metrics to Show

1. **Total Water Volume** - Sum across all reservoirs (TAF)
2. **Active Reservoirs** - Number of reservoirs reporting
3. **Data Points** - Total readings collected
4. **Reporting Period** - Number of days

---

## Demonstration Flow

1. ✅ Show CDEC API (curl command)
2. ✅ Check Mosquitto running
3. ✅ Start subscriber
4. ✅ Fetch and publish live data
5. ✅ Show text report
6. ✅ Generate charts
7. ✅ Open dashboard
8. ✅ Explain architecture

---

## One-Liner Demo

```bash
python subscriber.py --duration 90 & sleep 5 && python api_publisher.py --reservoir SHASTA,OROVILLE,FOLSOM --days 7 && sleep 90 && python visualize.py && python generate_dashboard.py && start reports/dashboard_*.html
```

---

## Assignment Requirements ✓

- ✅ MQTT publishers → Topics (RESERVOIR_ID/WML)
- ✅ MQTT subscribers → Collect all topics
- ✅ JSON data model
- ✅ CSV to JSON conversion
- ✅ Single subscriber
- ✅ Daily reports
- ✅ TAF measurements
- ✅ Multiple reservoirs

## Bonus Features ⭐

- ⭐ Real-time CDEC API integration
- ⭐ 21+ reservoirs supported
- ⭐ Data visualization (charts)
- ⭐ Interactive HTML dashboard
- ⭐ Wildcard MQTT subscriptions
