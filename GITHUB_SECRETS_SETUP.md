# GitHub Secrets Setup Guide

## Overview

To run the automated daily data updates using GitHub Actions with cloud MQTT, you need to add your HiveMQ credentials as **GitHub Secrets**.

GitHub Secrets are encrypted and secure - perfect for storing passwords and API keys!

---

## Step-by-Step Setup

### 1. Go to Your Repository Settings

1. Open your repository: https://github.com/BalaAnbalagan/reservoir_monitoring
2. Click **"Settings"** tab (top right)
3. In left sidebar, click **"Secrets and variables"** → **"Actions"**

### 2. Add These Secrets

Click **"New repository secret"** for each of these:

#### Secret 1: MQTT_CLOUD_BROKER
- **Name**: `MQTT_CLOUD_BROKER`
- **Value**: `your-cluster-id.s1.eu.hivemq.cloud` (replace with YOUR HiveMQ cluster URL)
- Click **"Add secret"**

#### Secret 2: MQTT_CLOUD_PORT
- **Name**: `MQTT_CLOUD_PORT`
- **Value**: `8883`
- Click **"Add secret"**

#### Secret 3: MQTT_CLOUD_USER
- **Name**: `MQTT_CLOUD_USER`
- **Value**: `your_hivemq_username` (replace with YOUR HiveMQ username)
- Click **"Add secret"**

#### Secret 4: MQTT_CLOUD_PASS
- **Name**: `MQTT_CLOUD_PASS`
- **Value**: `your_hivemq_password` (replace with YOUR HiveMQ password)
- Click **"Add secret"**

### 3. Verify Secrets Added

You should now see 4 secrets listed:
- ✅ MQTT_CLOUD_BROKER
- ✅ MQTT_CLOUD_PORT
- ✅ MQTT_CLOUD_USER
- ✅ MQTT_CLOUD_PASS

**Note**: You won't be able to view the values after adding them (they're encrypted), but you can update them anytime.

---

## How It Works

### The Workflow:

```
Every Day at 8 AM UTC:
├── GitHub Actions starts
├── Sets MQTT_ENV=cloud
├── Uses your HiveMQ credentials from secrets
├── Runs subscriber.py (90 seconds)
├── Runs api_publisher.py (fetches CDEC data)
├── Publisher sends data to HiveMQ Cloud
├── Subscriber collects data from HiveMQ Cloud
├── Generates reports
├── Commits to GitHub
└── Triggers Render.com deployment
```

### When Render Deploys:
```
Render.com:
├── Pulls latest code from GitHub
├── Sees new reports in reports/ directory
├── Builds and deploys Flask app
├── Dashboard shows updated data
└── Users see fresh reservoir data!
```

---

## Testing the Workflow

### Manual Test (Recommended First Time)

1. Go to your repository on GitHub
2. Click **"Actions"** tab
3. Select **"Update Reservoir Data with Cloud MQTT"** workflow
4. Click **"Run workflow"** dropdown
5. Click **"Run workflow"** button
6. Watch it run in real-time!

**Expected Output:**
- ✅ Subscriber connects to HiveMQ Cloud
- ✅ Publisher fetches data from CDEC API
- ✅ Data published to cloud MQTT
- ✅ Subscriber collects messages
- ✅ Reports generated
- ✅ Changes committed to GitHub

### Check the Logs

Click on the running workflow to see detailed logs:
- Connection to HiveMQ
- Data fetching progress
- MQTT messages sent/received
- Reports generated
- Git commit status

---

## Automatic Daily Runs

After the secrets are set up, the workflow will run automatically:

**Schedule**: Daily at **8:00 AM UTC**
- California PST: **Midnight (12:00 AM)**
- California PDT: **1:00 AM**

Perfect timing to have fresh data every morning!

---

## Benefits

### 🎯 Completely Free
- GitHub Actions: 2,000 minutes/month (free)
- This workflow uses ~2 minutes per run
- Can run 1,000 times per month!
- **You use ~30 runs per month = FREE**

### 🔒 Secure
- Credentials encrypted in GitHub Secrets
- Never exposed in code or logs
- Only accessible by GitHub Actions

### 🚀 Automated
- No manual intervention needed
- Runs every day automatically
- Updates Render deployment automatically

### 🌐 Cloud-Based
- Uses HiveMQ Cloud MQTT
- No local Mosquitto needed
- Works from anywhere

---

## Troubleshooting

### Workflow Fails with "Connection Refused"

**Check**:
1. GitHub Secrets are correctly named (case-sensitive!)
2. HiveMQ cluster is active (check console.hivemq.cloud)
3. Username and password are correct

### No Reports Generated

**Check**:
1. Subscriber ran for full 90 seconds
2. Publisher successfully connected to CDEC API
3. MQTT messages were sent (check logs)

### Render Not Updating

**Check**:
1. Commits are being pushed to GitHub (check commit history)
2. Render auto-deploy is enabled (Render settings)
3. Render build succeeded (check Render dashboard)

---

## Cost Breakdown

### GitHub Actions (Free Tier)
- ✅ 2,000 minutes/month free
- This workflow: ~2 minutes per run
- Daily runs: 30 runs/month = **60 minutes used**
- **Cost: $0.00**

### HiveMQ Cloud (Free Tier)
- ✅ 100 MB/month free
- Each run: ~30 KB
- Daily runs: 30 runs = **900 KB/month**
- **Cost: $0.00**

### Render.com (Free Tier)
- ✅ 750 hours/month free
- Your app: Running 24/7 = **720 hours/month**
- **Cost: $0.00**

**Total Monthly Cost: $0.00** 🎉

---

## What Happens When You Push Code

```
Local Machine:
git add .
git commit -m "Update code"
git push origin main
        ↓
GitHub:
- Code updated
- GitHub Actions workflow runs
- New data fetched
- Reports generated
- Changes committed
        ↓
Render.com:
- Detects new commit
- Pulls latest code
- Builds application
- Deploys updated app
        ↓
Live Website:
- Shows fresh data
- Users see updates
```

**Everything happens automatically!** 🚀

---

## Summary

1. ✅ Add 4 secrets to GitHub
2. ✅ Test workflow manually once
3. ✅ Enjoy automatic daily updates!

Your reservoir monitoring system will now:
- Fetch fresh data every day
- Publish to cloud MQTT
- Generate updated reports
- Deploy to Render automatically
- **All without any manual work!**

---

## Next Steps

After setting up secrets:

1. **Test the workflow**:
   - Go to Actions tab
   - Run workflow manually
   - Verify it completes successfully

2. **Check Render deployment**:
   - Go to Render.com dashboard
   - Verify auto-deploy is enabled
   - Wait for automatic deployment

3. **View live data**:
   - Visit your Render URL
   - See the latest reservoir data
   - Check the charts and visualizations

---

**Your cloud-based, fully automated reservoir monitoring system is ready!** 🎉
