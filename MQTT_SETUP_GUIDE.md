# MQTT Setup Guide - Local & Cloud

This guide shows you how to use **both local MQTT (Mosquitto)** and **cloud MQTT (HiveMQ)** with your reservoir monitoring system.

---

## Quick Start

### Use Local MQTT (Default)
```bash
# No configuration needed!
# Just ensure Mosquitto is running
python publisher.py --reservoir ALL
python subscriber.py --duration 60
```

### Use Cloud MQTT (HiveMQ)
```bash
# Set environment variable
export MQTT_ENV=cloud  # Linux/Mac
set MQTT_ENV=cloud     # Windows

# Configure cloud settings (see below)
python publisher.py --reservoir ALL
python subscriber.py --duration 60
```

---

## Option 1: Local MQTT (Mosquitto)

### When to Use:
- ✅ Development and testing
- ✅ Running on your machine
- ✅ No internet required
- ✅ Free forever

### Setup:

1. **Install Mosquitto** (if not already installed)
   - Windows: https://mosquitto.org/download/
   - Linux: `sudo apt-get install mosquitto`
   - Mac: `brew install mosquitto`

2. **Start Mosquitto**
   ```bash
   # Windows
   net start mosquitto

   # Linux
   sudo systemctl start mosquitto

   # Mac
   brew services start mosquitto
   ```

3. **Run your system**
   ```bash
   python publisher.py --reservoir ALL
   python subscriber.py --duration 60
   ```

**That's it!** No configuration needed - it uses localhost by default.

---

## Option 2: Cloud MQTT (HiveMQ Cloud)

### When to Use:
- ✅ Deploy to cloud (Render, Heroku, etc.)
- ✅ Multiple machines need access
- ✅ Access from anywhere
- ✅ No local Mosquitto needed

### Setup:

#### Step 1: Create HiveMQ Cloud Account

1. Go to: **https://console.hivemq.cloud**
2. Sign up (free, no credit card)
3. Click **"Create Cluster"**
   - Name: `reservoir-monitoring`
   - Plan: **Free** (100 MB/month)
   - Region: Closest to you
   - Click **Create**

4. Wait 2-3 minutes for cluster to deploy

#### Step 2: Create Credentials

1. In your cluster, go to **"Access Management"**
2. Click **"Add Credentials"**
3. Create username and password:
   - Username: `reservoir_user` (or your choice)
   - Password: Create a strong password
4. Click **"Add"**

#### Step 3: Note Your Connection Details

You'll see:
- **Cluster URL**: `abcdef12.s1.eu.hivemq.cloud`
- **Port**: `8883` (TLS/SSL)
- **Username**: `reservoir_user`
- **Password**: `your_password`

#### Step 4: Configure Your System

**Option A: Environment Variables (Recommended)**

```bash
# Linux/Mac
export MQTT_ENV=cloud
export MQTT_CLOUD_BROKER=abcdef12.s1.eu.hivemq.cloud
export MQTT_CLOUD_PORT=8883
export MQTT_CLOUD_USER=reservoir_user
export MQTT_CLOUD_PASS=your_password

# Windows CMD
set MQTT_ENV=cloud
set MQTT_CLOUD_BROKER=abcdef12.s1.eu.hivemq.cloud
set MQTT_CLOUD_PORT=8883
set MQTT_CLOUD_USER=reservoir_user
set MQTT_CLOUD_PASS=your_password

# Windows PowerShell
$env:MQTT_ENV="cloud"
$env:MQTT_CLOUD_BROKER="abcdef12.s1.eu.hivemq.cloud"
$env:MQTT_CLOUD_PORT="8883"
$env:MQTT_CLOUD_USER="reservoir_user"
$env:MQTT_CLOUD_PASS="your_password"
```

**Option B: Edit mqtt_config.py directly**

```python
# In mqtt_config.py, update CLOUD_CONFIG:
CLOUD_CONFIG = {
    'broker': 'abcdef12.s1.eu.hivemq.cloud',
    'port': 8883,
    'username': 'reservoir_user',
    'password': 'your_password',
    'use_tls': True
}
```

#### Step 5: Test Cloud Connection

```bash
# Terminal 1: Start subscriber
python subscriber.py --duration 90

# Terminal 2: Start publisher
python publisher.py --reservoir ALL
```

You should see:
```
==================================================
MQTT Configuration (CLOUD)
==================================================
  broker       : abcdef12.s1.eu.hivemq.cloud
  port         : 8883
  username     : reservoir_user
  password     : ***
  use_tls      : True
==================================================

Connected to MQTT Broker at abcdef12.s1.eu.hivemq.cloud:8883
```

---

## Switching Between Local and Cloud

### Method 1: Environment Variable (Easiest)

```bash
# Use Local MQTT
export MQTT_ENV=local
python publisher.py --reservoir ALL

# Use Cloud MQTT
export MQTT_ENV=cloud
python publisher.py --reservoir ALL
```

### Method 2: Edit mqtt_config.py

```python
# At the top of mqtt_config.py
MQTT_ENV = 'local'  # or 'cloud'
```

---

## For Render.com Deployment

### Configure Environment Variables in Render:

1. Go to your Render.com dashboard
2. Select your web service
3. Go to **"Environment"** tab
4. Add these variables:

```
MQTT_ENV=cloud
MQTT_CLOUD_BROKER=abcdef12.s1.eu.hivemq.cloud
MQTT_CLOUD_PORT=8883
MQTT_CLOUD_USER=reservoir_user
MQTT_CLOUD_PASS=your_password
```

5. Click **"Save Changes"**
6. Render will auto-redeploy

Now your deployed app uses **cloud MQTT**!

---

## Architecture Comparison

### Local MQTT (Development)
```
┌──────────────┐
│ Your Machine │
├──────────────┤
│  Publisher   │ ──┐
│  Subscriber  │   │
│  Mosquitto   │ ←─┘
│  (localhost) │
└──────────────┘
```

### Cloud MQTT (Production)
```
┌──────────────┐         ┌─────────────┐
│ Your Machine │←────────→│  HiveMQ     │
│  Publisher   │         │   Cloud     │
│  Subscriber  │         │ (Internet)  │
└──────────────┘         └─────────────┘
                               ↕
                         ┌─────────────┐
                         │ Render.com  │
                         │   (Flask)   │
                         │  Publisher  │
                         │  Subscriber │
                         └─────────────┘
```

---

## Troubleshooting

### Local MQTT

**Connection Refused:**
```bash
# Check if Mosquitto is running
# Windows
sc query mosquitto

# Linux
sudo systemctl status mosquitto

# Mac
brew services list
```

**Start Mosquitto:**
```bash
# Windows
net start mosquitto

# Linux
sudo systemctl start mosquitto

# Mac
brew services start mosquitto
```

### Cloud MQTT

**Connection Timeout:**
- ✅ Check your cluster URL is correct
- ✅ Ensure port is `8883` (not 1883)
- ✅ Check username/password
- ✅ Verify cluster is **Active** in HiveMQ console

**TLS/SSL Errors:**
- Make sure `use_tls: True` in config
- Cloud MQTT requires TLS (port 8883)

**Authentication Failed:**
- Double-check username and password
- Passwords are case-sensitive
- Recreate credentials in HiveMQ console if needed

---

## Free Tier Limits

### HiveMQ Cloud Free Tier:
- ✅ **100 MB/month** data transfer
- ✅ **Unlimited connections**
- ✅ **1 cluster**
- ✅ **No credit card required**

**Estimated Usage:**
- Each message: ~200 bytes
- 21 reservoirs × 7 days = 147 messages
- Total: ~30 KB per week
- **You can run this system for MONTHS on free tier!**

---

## Testing Both Configurations

### Test Script:

```bash
# Test Local MQTT
export MQTT_ENV=local
python publisher.py --reservoir SHASTA
# Should connect to localhost:1883

# Test Cloud MQTT
export MQTT_ENV=cloud
python publisher.py --reservoir SHASTA
# Should connect to your HiveMQ cluster
```

---

## Recommendations

### For Development:
✅ Use **Local MQTT** (Mosquitto)
- Faster
- No internet required
- Free forever

### For Production (Render.com):
✅ Use **Cloud MQTT** (HiveMQ)
- Accessible from anywhere
- No local infrastructure needed
- Works with serverless deployments

### Hybrid Approach:
✅ Develop locally, deploy to cloud
- Use local MQTT while coding
- Switch to cloud MQTT for deployment
- Change with one environment variable!

---

## Next Steps

1. ✅ **Test Local MQTT** - Make sure Mosquitto works
2. ✅ **Create HiveMQ Account** - Set up cloud MQTT
3. ✅ **Test Cloud MQTT** - Verify cloud connection
4. ✅ **Deploy to Render** - Use cloud MQTT in production

---

## Summary

| Feature | Local MQTT | Cloud MQTT |
|---------|-----------|------------|
| **Setup** | Install Mosquitto | Create HiveMQ account |
| **Cost** | Free | Free (100MB/month) |
| **Access** | Your machine only | From anywhere |
| **Internet** | Not required | Required |
| **Best For** | Development | Production |
| **Switch** | `MQTT_ENV=local` | `MQTT_ENV=cloud` |

---

**Your system now supports BOTH local and cloud MQTT!** 🎉

Switch between them with a single environment variable!
