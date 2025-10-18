# Dashboard Screenshots

This directory contains screenshots of the California Reservoir Monitoring System dashboard.

## Required Screenshots

Please save your dashboard screenshots with the following names:

### Local Dashboard (localhost:5000)

1. **`local_summary_view.png`**
   - URL: http://localhost:5000/
   - Shows: Summary dashboard with total water volume, period change, active reservoirs, and quick view charts

2. **`local_detailed_view.png`**
   - URL: http://localhost:5000/detailed
   - Shows: Detailed analysis with bar charts, stacked charts, and water level changes

3. **`local_detailed_stacked_chart.png`** (optional - closeup of stacked chart)
   - URL: http://localhost:5000/detailed
   - Shows: Closeup of the stacked water levels over time chart

### Cloud Dashboard (https://reservoir-monitoring.onrender.com)

4. **`cloud_summary_view.png`**
   - URL: https://reservoir-monitoring.onrender.com/
   - Shows: Live cloud dashboard summary view

5. **`cloud_detailed_view.png`**
   - URL: https://reservoir-monitoring.onrender.com/detailed
   - Shows: Live cloud dashboard detailed analysis view

6. **`cloud_detailed_stacked_chart.png`** (optional - closeup of stacked chart)
   - URL: https://reservoir-monitoring.onrender.com/detailed
   - Shows: Closeup of the stacked water levels chart

## How to Add Screenshots

1. Take screenshots of your dashboard (use Snipping Tool, PrtScn, or browser screenshot feature)
2. Save them to this `screenshots/` directory with the exact names above
3. Commit and push to GitHub:
   ```bash
   git add screenshots/
   git commit -m "Add dashboard screenshots"
   git push origin main
   ```

## Screenshot Guidelines

- **Format:** PNG or JPG (PNG preferred for better quality)
- **Resolution:** Full browser window (1920x1080 or similar)
- **Content:** Make sure all charts and data are visible
- **Clean:** Close unnecessary browser tabs/toolbars for clean screenshots

## Usage in Documentation

These screenshots will be referenced in the main README.md to provide visual examples of the dashboard features.
