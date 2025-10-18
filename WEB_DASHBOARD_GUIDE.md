# Web Dashboard Deployment Guide

## Overview

This guide shows you how to deploy a **dynamic web dashboard** for your reservoir monitoring system on **free hosting platforms**.

---

## What You Get

### Features:

✅ **Dynamic Dashboard** - Auto-refreshes every 5 minutes
✅ **Summary View** - Quick stats and charts
✅ **Detailed View** - Full historical data with day-over-day changes
✅ **RESTful API** - JSON endpoints for data access
✅ **Responsive Design** - Works on mobile, tablet, desktop
✅ **Free Hosting** - Deploy on Render, Railway, Fly.io, or PythonAnywhere

---

## Local Testing

### 1. Install Flask

```bash
pip install flask gunicorn
```

### 2. Run Locally

```bash
# Start the web server
python app.py
```

**Open browser:**
```
http://localhost:5000
```

You'll see:
- Summary dashboard at `/`
- Detailed view at `/detailed`
- API endpoints at `/api/*`

---

## Free Hosting Options

### Option 1: Render.com (Recommended) ⭐

**Why Render:**
- 750 hours/month free
- Auto-deploys from GitHub
- Custom domains
- HTTPS included

**Steps:**

1. **Create account:** https://render.com
2. **Push code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Add web dashboard"
   git push origin main
   ```

3. **Create Web Service on Render:**
   - Click "New +"
   - Select "Web Service"
   - Connect GitHub repo
   - Settings:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
     - **Plan:** Free

4. **Deploy!**
   - Render auto-deploys
   - Your URL: `https://your-app.onrender.com`

---

### Option 2: Railway.app

**Why Railway:**
- $5 free credit/month
- Simple deployment
- Great for Python apps

**Steps:**

1. **Create account:** https://railway.app
2. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

3. **Deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

4. **Access:** Railway gives you a URL

---

### Option 3: Fly.io

**Why Fly.io:**
- 3 VMs free
- Global deployment
- Good performance

**Steps:**

1. **Install flyctl:** https://fly.io/docs/hands-on/install-flyctl/
2. **Deploy:**
   ```bash
   fly launch
   fly deploy
   ```

---

### Option 4: PythonAnywhere.com

**Why PythonAnywhere:**
- 100% Python focus
- Beginner-friendly
- Free tier available

**Steps:**

1. **Create account:** https://www.pythonanywhere.com
2. **Upload files** via web interface
3. **Configure web app:**
   - Framework: Flask
   - Python version: 3.11
   - Working directory: `/home/username/reservoir_monitoring`

4. **Reload web app**

---

## API Endpoints

Your deployed dashboard will have these endpoints:

| Endpoint | Description | Example |
|----------|-------------|---------|
| `/` | Main dashboard | Summary view |
| `/detailed` | Detailed analysis | Full data table |
| `/api/summary` | Summary stats (JSON) | `{"total_water": 2636.8, ...}` |
| `/api/latest` | Latest day data (JSON) | Today's readings |
| `/api/historical` | All historical data (JSON) | Complete dataset |
| `/api/changes` | Day-over-day changes (JSON) | Change analysis |
| `/api/reservoir/SHASTA` | Specific reservoir (JSON) | Shasta only |

---

## Updating Data

### Method 1: Manual Update

```bash
# On your local machine:
python subscriber.py --duration 90 &
python api_publisher.py --reservoir ALL --days 7
python visualize.py

# Push to GitHub
git add reports/
git commit -m "Update data"
git push

# Render auto-redeploys
```

### Method 2: Scheduled Updates (Advanced)

**Using GitHub Actions:**

Create `.github/workflows/update-data.yml`:

```yaml
name: Update Reservoir Data

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:  # Manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Fetch new data
        run: python api_publisher.py --reservoir ALL --days 7

      - name: Generate visualizations
        run: python visualize.py

      - name: Commit and push
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add reports/
          git commit -m "Auto-update data"
          git push
```

This auto-updates daily!

---

## Environment Variables (if needed)

For sensitive data, use environment variables:

**On Render:**
1. Go to Dashboard → Environment
2. Add:
   - `SECRET_KEY=your-secret-key`
   - `MQTT_BROKER=localhost` (if using external broker)

**In code:**
```python
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key')
```

---

## File Structure for Deployment

```
reservoir_monitoring/
├── app.py                    # Flask application
├── requirements.txt          # Python dependencies
├── Procfile                  # Render/Heroku config
├── runtime.txt              # Python version
├── templates/
│   └── index.html           # Dashboard template
├── reports/
│   ├── comprehensive_report_*.json
│   └── visualizations/
│       └── *.png
└── data/
    └── *.json
```

---

## Pros & Cons

### Web Dashboard

**Pros:**
- ✅ Access from anywhere
- ✅ No installation needed
- ✅ Share with others (URL)
- ✅ Auto-refresh capability
- ✅ RESTful API for integration

**Cons:**
- ❌ Need to host somewhere
- ❌ Free tiers have limitations
- ❌ Requires internet connection

### Static HTML Dashboard

**Pros:**
- ✅ Works offline
- ✅ No hosting needed
- ✅ Fast and simple
- ✅ Easy to share (single file)

**Cons:**
- ❌ No auto-refresh
- ❌ Manual regeneration
- ❌ No API access

---

## Recommendation for Your Assignment

### For Demonstration:

**Use local Flask app:**
```bash
python app.py
# Show at http://localhost:5000
```

**Benefits:**
- Show dynamic features
- Demonstrate API endpoints
- Refresh button works
- Professional web interface

### For Submission:

**Include both:**
1. **Static HTML** - Works offline, self-contained
2. **Flask App** - Shows you know web development

---

## Cost Comparison

| Platform | Free Tier | Best For |
|----------|-----------|----------|
| **Render** | 750 hrs/mo | Public demos |
| **Railway** | $5 credit/mo | Quick deploys |
| **Fly.io** | 3 VMs | Global access |
| **PythonAnywhere** | Limited | Python learners |
| **Local** | Free forever | Demos, testing |

---

## Quick Start Commands

```bash
# 1. Install Flask
pip install flask gunicorn

# 2. Run locally
python app.py

# 3. Open browser
# http://localhost:5000

# 4. Test API
curl http://localhost:5000/api/summary

# 5. Deploy to Render (after GitHub push)
# Just connect repo on Render.com
```

---

## Sample API Response

**GET `/api/summary`:**
```json
{
  "total_water": 2636.8,
  "period_change": -28.2,
  "num_reservoirs": 3,
  "num_days": 7,
  "date_range": {
    "start": "10/11/2025",
    "end": "10/17/2025"
  }
}
```

**GET `/api/reservoir/SHASTA`:**
```json
[
  {
    "date": "10/11/2025",
    "reservoir_id": "SHASTA",
    "average_water_level_taf": 2636.8,
    "min_water_level_taf": 2636.8,
    "max_water_level_taf": 2636.8,
    "readings_count": 1
  },
  ...
]
```

---

## Troubleshooting

### Port already in use:
```bash
# Change port in app.py:
app.run(debug=True, host='0.0.0.0', port=8000)
```

### Templates not found:
```bash
# Make sure templates/ directory exists
mkdir templates
```

### No data showing:
```bash
# Generate reports first
python subscriber.py --duration 90 &
python api_publisher.py --reservoir ALL --days 7
python visualize.py
```

---

## For Your Assignment

**Demonstrate both capabilities:**

1. **Static Dashboard** - "This is the generated report"
2. **Web Dashboard** - "This is the live monitoring interface"

**Say:**
> "The static HTML is perfect for offline reports and sharing via email.
> The web dashboard provides real-time access and can be deployed to the cloud for 24/7 monitoring."

---

**Your system now has BOTH static and dynamic visualization options!** 🎉
