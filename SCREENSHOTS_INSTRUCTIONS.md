# How to Add Dashboard Screenshots to Repository

## Quick Instructions

Based on the screenshots you showed me, you need to save them to the `screenshots/` directory with these specific names:

### Step 1: Take/Prepare Screenshots

You already have these screenshots from your browser:

1. **Local Summary View** (localhost:5000)
   - The one showing "Last Updated: October 18, 2025 at 04:26 AM"
   - Save as: `local_summary_view.png`

2. **Local Detailed View** (localhost:5000/detailed)
   - The one showing bar charts and stacked charts from localhost
   - Save as: `local_detailed_view.png`

3. **Cloud Summary View** (https://reservoir-monitoring.onrender.com)
   - The one showing "Last Updated: October 18, 2025 at 11:29 AM"
   - Save as: `cloud_summary_view.png`

4. **Cloud Detailed View** (https://reservoir-monitoring.onrender.com/detailed)
   - The one showing bar charts and stacked charts from Render.com
   - Save as: `cloud_detailed_view.png`

### Step 2: Save Screenshots to Repository

**Option A: Using File Explorer (Windows)**
1. Open File Explorer
2. Navigate to: `C:\myCodes\reservoir_monitoring\screenshots\`
3. Copy/paste your 4 screenshot images into this folder
4. Rename them exactly as shown above

**Option B: Using Command Line**
```bash
# If your screenshots are on Desktop, move them to screenshots folder
cd C:\myCodes\reservoir_monitoring\screenshots
copy "%USERPROFILE%\Desktop\your-screenshot-1.png" local_summary_view.png
copy "%USERPROFILE%\Desktop\your-screenshot-2.png" local_detailed_view.png
copy "%USERPROFILE%\Desktop\your-screenshot-3.png" cloud_summary_view.png
copy "%USERPROFILE%\Desktop\your-screenshot-4.png" cloud_detailed_view.png
```

### Step 3: Commit and Push to GitHub

```bash
cd C:\myCodes\reservoir_monitoring
git add screenshots/*.png
git commit -m "Add dashboard screenshots for local and cloud deployments"
git push origin main
```

### Step 4: Verify on GitHub

1. Go to: https://github.com/BalaAnbalagan/reservoir_monitoring
2. Navigate to the `screenshots/` folder
3. You should see all 4 PNG files

## Screenshot Names (Important!)

Make sure the filenames are EXACTLY:
- ✅ `local_summary_view.png` (correct)
- ❌ `local_summary_view.PNG` (wrong - uppercase extension)
- ❌ `Local Summary View.png` (wrong - spaces and capitals)
- ❌ `screenshot1.png` (wrong - generic name)

## What These Screenshots Show

### Local Summary View
- Total Water Volume: 5,587.8 TAF
- Period Change: -19.8 TAF (red = loss)
- Active Reservoirs: 8
- Reporting Period: 7 days
- Quick view charts

### Local Detailed View
- Current Water Levels bar chart (8 reservoirs)
- Stacked Water Levels Over Time chart
- Color-coded by reservoir

### Cloud Summary View
- Same as local but running on Render.com
- Shows it's live and accessible via URL

### Cloud Detailed View
- Same features as local detailed view
- Proves cloud deployment is working

## Why This Matters

These screenshots serve as **artifacts** or **proof** that:
1. ✅ Your local development environment works
2. ✅ Your cloud production deployment works
3. ✅ Both display the same data correctly
4. ✅ The single subscriber architecture is functioning
5. ✅ MQTT pub/sub is working in both modes

Your professor can see visual evidence of a working system!

---

**After you add the screenshots and push to GitHub, the README will automatically display them as visual examples.**
