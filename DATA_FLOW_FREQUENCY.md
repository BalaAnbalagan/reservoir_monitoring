# Data Flow Frequency Guide

## Overview

This document explains how frequently data flows through the reservoir monitoring system.

---

## 1. CDEC API Update Frequency (Source Data)

### California Data Exchange Center Updates:

| Data Type | Code | Update Frequency | When Updated |
|-----------|------|------------------|--------------|
| **Daily** | `D` | Once per day | Midnight Pacific Time |
| **Hourly** | `H` | Every 1-6 hours | Varies by sensor |
| **Event** | `E` | On events | When triggered |
| **Monthly** | `M` | Once per month | End of month |

**Your system currently uses:** `dur_code=D` (Daily)
- **Real update frequency:** Once per day at midnight PT
- **New data available:** After 12:00 AM Pacific Time

---

## 2. Your System's Data Flow

### A. Manual Mode (Current Setup)

```
You → Run Command → Fetch API → Publish MQTT → Collect → Report
     (manual)      (instant)   (~73 sec)     (60-90s)  (instant)
```

**Timeline:**
1. **T+0s**: You run `api_publisher.py`
2. **T+5s**: API returns data (7 days × 21 reservoirs)
3. **T+5s to T+78s**: Publishing messages (0.5s delay each)
4. **T+90s**: Subscriber finishes, generates report
5. **T+92s**: Visualizations generated
6. **T+93s**: Dashboard created

**Total Time:** ~93 seconds from start to dashboard

---

### B. Message Publishing Rate

```python
# Current setting in api_publisher.py:
time.sleep(0.5)  # 0.5 seconds between messages
```

**Message Flow Rate:**

| Scenario | Messages | Time to Publish |
|----------|----------|-----------------|
| 3 reservoirs × 7 days | 21 | ~10.5 seconds |
| 3 reservoirs × 30 days | 90 | ~45 seconds |
| 21 reservoirs × 7 days | 147 | ~73.5 seconds |
| 21 reservoirs × 30 days | 630 | ~315 seconds (5.25 min) |

**You can adjust the delay:**
```python
time.sleep(0.1)  # Faster: 0.1 seconds
time.sleep(1.0)  # Slower: 1 second (better for demos)
time.sleep(2.0)  # Very slow: 2 seconds (dramatic for presentations)
```

---

## 3. Live Demo Streaming

### For Impressive Demonstrations:

Use the new **[demo_live_stream.py](demo_live_stream.py:1)** script:

```bash
# Slow streaming (2 seconds per message) - Great for demos!
python subscriber.py --duration 30 &
python demo_live_stream.py --reservoir SHASTA --delay 2
```

**Effect:**
- Messages appear every 2 seconds
- Looks like live sensor readings
- Easy to follow during presentation
- Subscriber shows each message arriving

**Timeline Example:**
```
00:00 - Start subscriber
00:03 - Start demo stream
00:03 - Message 1: 10/11/2024 - 2636.8 TAF
00:05 - Message 2: 10/12/2024 - 2629.67 TAF
00:07 - Message 3: 10/13/2024 - 2626.4 TAF
...
00:21 - Message 9: 10/19/2024 - 2608.6 TAF
00:23 - Stream complete
```

---

## 4. Production Scenarios

### Scenario A: Daily Monitoring

**Schedule:** Once per day at 1:00 AM

```bash
# Windows Task Scheduler
# Action: Run program
# Program: python
# Arguments: C:\myCodes\reservoir_monitoring\api_publisher.py --reservoir ALL --days 1
# Schedule: Daily at 1:00 AM
```

**Data Flow:**
- CDEC updates at midnight
- Script runs at 1:00 AM
- Fetches latest 1 day × 21 reservoirs = 21 messages
- Publishes in ~10 seconds
- Dashboard updates automatically

**Frequency:** Daily

---

### Scenario B: Hourly Monitoring

**Schedule:** Every hour

```bash
# Fetch and publish every hour
# Uses hourly data (dur_code=H)
```

Modify `api_publisher.py` line 82:
```python
# Change from:
dur_code=D

# To:
dur_code=H
```

**Data Flow:**
- Runs every hour
- Fetches last 24 hours of data
- More frequent updates

**Frequency:** Hourly

---

### Scenario C: On-Demand

**Schedule:** Manual/As needed

```bash
# Run whenever you want updated data
python subscriber.py --duration 90 &
python api_publisher.py --reservoir ALL --days 7
python visualize.py
python generate_dashboard.py
```

**Frequency:** Whenever you run it

---

## 5. Real-Time vs Near Real-Time

### Current System: **Near Real-Time**

```
Source Data → Your System
(Daily)       (On-demand)

CDEC API      →  You manually run script
Updates daily →  Fetches + Publishes (~1 min)
                 Generates report (instant)
```

**Latency:**
- CDEC updates: Midnight PT
- Your system: When you run it
- Total delay: Up to 24 hours (if CDEC is daily)

---

### True Real-Time Would Require:

```
Source Data → Your System
(Continuous)  (Continuous)

Sensors  →  MQTT  →  Subscriber  →  Live Dashboard
(real-time)  (instant)  (instant)     (auto-refresh)
```

**Latency:** < 1 second

**Requirements:**
- Sensors publishing continuously
- Subscriber always running
- WebSocket dashboard
- Database storage

---

## 6. Comparison Table

| Metric | Current System | True Real-Time |
|--------|---------------|----------------|
| **Source Updates** | Daily (CDEC) | Continuous (sensors) |
| **Your Polling** | Manual | Automated |
| **Message Delay** | 0.5s | Instant |
| **Dashboard** | Static (regenerate) | Live (auto-update) |
| **Latency** | Up to 24h | < 1 second |
| **Good For** | Reports, analysis | Monitoring, alerts |

---

## 7. How to Change Message Flow Rate

### Option 1: Edit api_publisher.py

Find line 80:
```python
time.sleep(0.5)  # Small delay between messages
```

Change to:
```python
time.sleep(2.0)  # Slower for demos
# OR
time.sleep(0.1)  # Faster for production
# OR
time.sleep(0)    # No delay (fastest)
```

---

### Option 2: Use Demo Mode

```bash
# Slow dramatic streaming (2 sec per message)
python demo_live_stream.py --reservoir SHASTA --delay 2

# Medium speed (1 sec per message)
python demo_live_stream.py --reservoir SHASTA --delay 1

# Fast streaming (0.5 sec per message)
python demo_live_stream.py --reservoir SHASTA --delay 0.5
```

---

## 8. For Your Presentation

### Recommended Settings:

**For Impressive Demo:**
```bash
# Use slow streaming so audience can see messages
python subscriber.py --duration 30 &
python demo_live_stream.py --reservoir SHASTA --delay 2
```

**Each message will be visible for 2 seconds - easy to follow!**

---

**For Fast Demo:**
```bash
# Use normal speed
python subscriber.py --duration 90 &
python api_publisher.py --reservoir SHASTA,OROVILLE,FOLSOM --days 7
```

**Messages flow quickly - shows system efficiency!**

---

## 9. Summary

### Current Data Flow:

1. **CDEC API**: Updates **once per day** (midnight PT)
2. **Your Publisher**: Runs **on-demand** (when you trigger it)
3. **Message Rate**: **0.5 seconds** between messages (configurable)
4. **Total Time**: **~73 seconds** for 21 reservoirs × 7 days
5. **Dashboard**: **Static snapshot** (regenerate for updates)

### To Make It Look "Live" for Demo:

Use **demo_live_stream.py** with 2-second delay:
- Looks like real-time sensor readings
- Easy for audience to follow
- Professional presentation effect

---

**The system is designed for daily monitoring, but can be configured for any frequency!**
