"""
Enhanced Historical Dashboard Generator
Creates an interactive dashboard with:
- Historical data navigation
- Trend analysis
- Day-over-day changes
- Interactive date selection
"""

import json
import base64
from pathlib import Path
from datetime import datetime


class EnhancedDashboardGenerator:
    """Generate enhanced HTML dashboard with historical analysis"""

    def __init__(self, report_file, viz_dir):
        """
        Initialize dashboard generator

        Args:
            report_file: Path to JSON report
            viz_dir: Directory containing visualization images
        """
        self.report_file = Path(report_file)
        self.viz_dir = Path(viz_dir)

        with open(self.report_file, 'r') as f:
            self.data = json.load(f)

    def image_to_base64(self, image_path):
        """Convert image to base64 for embedding in HTML"""
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()

    def calculate_changes(self):
        """Calculate day-over-day changes"""
        if len(self.data) < 2:
            return None

        changes = []
        for i in range(1, len(self.data)):
            prev_day = self.data[i-1]
            curr_day = self.data[i]

            day_changes = {
                'date': curr_day['date'],
                'reservoirs': {}
            }

            for reservoir_name, curr_res_data in curr_day['reservoirs'].items():
                if reservoir_name in prev_day['reservoirs']:
                    prev_level = prev_day['reservoirs'][reservoir_name]['average_water_level_taf']
                    curr_level = curr_res_data['average_water_level_taf']
                    change = curr_level - prev_level
                    percent_change = (change / prev_level * 100) if prev_level > 0 else 0

                    day_changes['reservoirs'][reservoir_name] = {
                        'previous': prev_level,
                        'current': curr_level,
                        'change': change,
                        'percent_change': percent_change
                    }

            changes.append(day_changes)

        return changes

    def generate_html(self, output_file):
        """Generate enhanced HTML dashboard"""

        # Find visualization images
        viz_files = sorted(self.viz_dir.glob('*.png'))
        timeseries_img = next((f for f in viz_files if 'timeseries' in f.name), None)
        comparison_img = next((f for f in viz_files if 'comparison' in f.name), None)
        total_img = next((f for f in viz_files if 'total' in f.name), None)

        # Calculate changes
        changes = self.calculate_changes()

        # Generate HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>California Reservoir Historical Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .date-range {{
            background: #ecf0f1;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }}

        .date-range .period {{
            font-size: 1.1em;
            font-weight: bold;
            color: #2c3e50;
        }}

        .date-range .generated {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}

        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #3498db;
        }}

        .stat-card h3 {{
            color: #2c3e50;
            font-size: 1.1em;
            margin-bottom: 10px;
        }}

        .stat-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}

        .stat-card .label {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 5px;
        }}

        .charts-section {{
            padding: 30px;
        }}

        .chart-container {{
            margin-bottom: 40px;
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}

        .chart-container h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}

        .chart-container img {{
            width: 100%;
            height: auto;
            border-radius: 5px;
        }}

        .changes-section {{
            padding: 30px;
            background: #f8f9fa;
        }}

        .changes-section h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}

        .change-card {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}

        .change-card h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.2em;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
        }}

        .reservoir-change {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 10px;
            padding: 10px;
            border-bottom: 1px solid #ecf0f1;
            align-items: center;
        }}

        .reservoir-change:last-child {{
            border-bottom: none;
        }}

        .reservoir-name {{
            font-weight: bold;
            font-size: 1.1em;
        }}

        .change-positive {{
            color: #27ae60;
            font-weight: bold;
        }}

        .change-negative {{
            color: #e74c3c;
            font-weight: bold;
        }}

        .change-neutral {{
            color: #95a5a6;
            font-weight: bold;
        }}

        .arrow-up::before {{
            content: "↑ ";
        }}

        .arrow-down::before {{
            content: "↓ ";
        }}

        .arrow-neutral::before {{
            content: "→ ";
        }}

        .data-table {{
            padding: 30px;
        }}

        .data-table h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        thead {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
        }}

        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
        }}

        tbody tr:hover {{
            background-color: #f8f9fa;
        }}

        .reservoir-shasta {{ color: #1f77b4; font-weight: bold; }}
        .reservoir-oroville {{ color: #ff7f0e; font-weight: bold; }}
        .reservoir-sonoma {{ color: #2ca02c; font-weight: bold; }}
        .reservoir-trinity {{ color: #d62728; font-weight: bold; }}
        .reservoir-folsom {{ color: #9467bd; font-weight: bold; }}
        .reservoir-new_melones {{ color: #8c564b; font-weight: bold; }}
        .reservoir-don_pedro {{ color: #e377c2; font-weight: bold; }}

        footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}

        .summary-stats {{
            background: #ecf0f1;
            padding: 20px 30px;
            margin: 20px 30px;
            border-radius: 8px;
        }}

        .summary-stats h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
        }}

        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}

        .summary-item {{
            background: white;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }}

        .summary-item .label {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}

        .summary-item .value {{
            color: #2c3e50;
            font-size: 1.3em;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌊 California Reservoir Historical Dashboard</h1>
            <p>Water Level Monitoring & Trend Analysis</p>
        </header>

        <div class="date-range">
            <div class="period">
                📅 Reporting Period: {self.data[0]['date'] if self.data else 'N/A'} - {self.data[-1]['date'] if self.data else 'N/A'}
            </div>
            <div class="generated">
                Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </div>
        </div>
"""

        # Add summary statistics
        if self.data:
            latest_record = self.data[-1]
            first_record = self.data[0]
            total_water_latest = latest_record.get('total_water_level_taf', 0)
            total_water_first = first_record.get('total_water_level_taf', 0)
            water_change = total_water_latest - total_water_first
            num_days = len(self.data)
            num_reservoirs = len(latest_record.get('reservoirs', {}))

            html += f"""
        <div class="summary-stats">
            <h3>📊 Period Summary</h3>
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="label">Total Water (Latest)</div>
                    <div class="value">{total_water_latest:,.1f} TAF</div>
                </div>
                <div class="summary-item">
                    <div class="label">Period Change</div>
                    <div class="value" style="color: {'#27ae60' if water_change >= 0 else '#e74c3c'}">
                        {'+' if water_change >= 0 else ''}{water_change:,.1f} TAF
                    </div>
                </div>
                <div class="summary-item">
                    <div class="label">Active Reservoirs</div>
                    <div class="value">{num_reservoirs}</div>
                </div>
                <div class="summary-item">
                    <div class="label">Days Monitored</div>
                    <div class="value">{num_days}</div>
                </div>
            </div>
        </div>
"""

        html += """
        <div class="stats-grid">
"""

        # Add current statistics
        if self.data:
            latest_record = self.data[-1]
            total_water = latest_record.get('total_water_level_taf', 0)
            num_days = len(self.data)
            num_reservoirs = len(latest_record.get('reservoirs', {}))

            # Calculate total messages
            total_messages = sum(
                sum(res.get('readings_count', 0) for res in day.get('reservoirs', {}).values())
                for day in self.data
            )

            html += f"""
            <div class="stat-card">
                <h3>💧 Current Total Water</h3>
                <div class="value">{total_water:,.1f}</div>
                <div class="label">TAF (Thousand Acre-Feet)</div>
            </div>

            <div class="stat-card">
                <h3>🏞️ Active Reservoirs</h3>
                <div class="value">{num_reservoirs}</div>
                <div class="label">Monitoring Locations</div>
            </div>

            <div class="stat-card">
                <h3>📅 Reporting Period</h3>
                <div class="value">{num_days}</div>
                <div class="label">Days of Historical Data</div>
            </div>

            <div class="stat-card">
                <h3>📈 Data Points</h3>
                <div class="value">{total_messages}</div>
                <div class="label">Total Readings Collected</div>
            </div>
"""

        html += """
        </div>
"""

        # Add changes section
        if changes:
            html += """
        <div class="changes-section">
            <h2>📊 Day-Over-Day Changes</h2>
"""
            for change_day in changes[-5:]:  # Show last 5 days
                html += f"""
            <div class="change-card">
                <h3>{change_day['date']}</h3>
"""
                for reservoir_name, change_data in change_day['reservoirs'].items():
                    change = change_data['change']
                    percent = change_data['percent_change']

                    if change > 0:
                        change_class = "change-positive arrow-up"
                    elif change < 0:
                        change_class = "change-negative arrow-down"
                    else:
                        change_class = "change-neutral arrow-neutral"

                    css_class = f"reservoir-{reservoir_name.lower().replace('_', '-')}"

                    html += f"""
                <div class="reservoir-change">
                    <div class="reservoir-name {css_class}">{reservoir_name}</div>
                    <div>{change_data['previous']:,.2f} TAF</div>
                    <div>{change_data['current']:,.2f} TAF</div>
                    <div class="{change_class}">{change:+.2f} TAF ({percent:+.2f}%)</div>
                </div>
"""
                html += """
            </div>
"""
            html += """
        </div>
"""

        # Add charts
        html += """
        <div class="charts-section">
"""

        if timeseries_img:
            img_data = self.image_to_base64(timeseries_img)
            html += f"""
            <div class="chart-container">
                <h2>📈 Water Levels Over Time (Historical Trend)</h2>
                <img src="data:image/png;base64,{img_data}" alt="Water Levels Time Series">
                <p style="color: #7f8c8d; margin-top: 10px; font-size: 0.9em;">
                    This chart shows how water levels have changed over the reporting period.
                    You can see trends, seasonal patterns, and identify periods of increase or decrease.
                </p>
            </div>
"""

        if comparison_img:
            img_data = self.image_to_base64(comparison_img)
            html += f"""
            <div class="chart-container">
                <h2>📊 Current Levels Comparison</h2>
                <img src="data:image/png;base64,{img_data}" alt="Water Levels Comparison">
                <p style="color: #7f8c8d; margin-top: 10px; font-size: 0.9em;">
                    Compare current water levels across all monitored reservoirs.
                    Easily identify which reservoirs have higher or lower storage capacity.
                </p>
            </div>
"""

        if total_img:
            img_data = self.image_to_base64(total_img)
            html += f"""
            <div class="chart-container">
                <h2>💦 Total Capacity Trend</h2>
                <img src="data:image/png;base64,{img_data}" alt="Total Capacity">
                <p style="color: #7f8c8d; margin-top: 10px; font-size: 0.9em;">
                    Combined water storage across all reservoirs.
                    This shows the overall water availability trend for the state.
                </p>
            </div>
"""

        html += """
        </div>

        <div class="data-table">
            <h2>📋 Complete Historical Data</h2>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Reservoir</th>
                        <th>Average (TAF)</th>
                        <th>Min (TAF)</th>
                        <th>Max (TAF)</th>
                        <th>Readings</th>
                    </tr>
                </thead>
                <tbody>
"""

        # Add data rows (sorted by date descending - newest first)
        for daily_record in sorted(self.data, key=lambda x: x['date'], reverse=True):
            date = daily_record['date']
            for reservoir_name, reservoir_data in daily_record['reservoirs'].items():
                css_class = f"reservoir-{reservoir_name.lower().replace('_', '-')}"
                html += f"""
                    <tr>
                        <td>{date}</td>
                        <td class="{css_class}">{reservoir_name}</td>
                        <td>{reservoir_data['average_water_level_taf']:,.2f}</td>
                        <td>{reservoir_data['min_water_level_taf']:,.2f}</td>
                        <td>{reservoir_data['max_water_level_taf']:,.2f}</td>
                        <td>{reservoir_data['readings_count']}</td>
                    </tr>
"""

        html += """
                </tbody>
            </table>
        </div>

        <footer>
            <p><strong>California Department of Water Resources - Historical Reservoir Monitoring System</strong></p>
            <p>Data Source: California Data Exchange Center (CDEC) API | Powered by MQTT Protocol</p>
            <p style="margin-top: 10px; font-size: 0.85em;">
                💡 This dashboard shows historical trends. CDEC updates daily at midnight PT.
                Regenerate this dashboard to see the latest data.
            </p>
        </footer>
    </div>
</body>
</html>
"""

        # Save HTML file with UTF-8 encoding
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"[OK] Enhanced historical dashboard generated: {output_file}")
        return output_file


def main():
    """Main function"""
    # Find latest report
    reports_dir = Path(__file__).parent / 'reports'
    json_files = sorted(reports_dir.glob('comprehensive_report_*.json'))

    if not json_files:
        print("Error: No report files found")
        return

    report_file = json_files[-1]
    viz_dir = reports_dir / 'visualizations'

    if not viz_dir.exists():
        print("Error: No visualizations found. Run visualize.py first.")
        return

    # Generate enhanced dashboard
    generator = EnhancedDashboardGenerator(report_file, viz_dir)
    output_file = reports_dir / f"historical_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    dashboard_path = generator.generate_html(output_file)
    print(f"\n[OK] Dashboard ready!")
    print(f"[OK] Open in browser: {dashboard_path.absolute()}")


if __name__ == "__main__":
    main()
