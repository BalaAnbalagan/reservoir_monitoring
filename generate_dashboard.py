"""
Generate Interactive HTML Dashboard for Reservoir Data
Creates a web-based dashboard to view reports and charts
"""

import json
import base64
from pathlib import Path
from datetime import datetime


class DashboardGenerator:
    """Generate HTML dashboard from reports and visualizations"""

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

    def generate_html(self, output_file):
        """Generate complete HTML dashboard"""

        # Find visualization images
        viz_files = sorted(self.viz_dir.glob('*.png'))
        timeseries_img = next((f for f in viz_files if 'timeseries' in f.name), None)
        comparison_img = next((f for f in viz_files if 'comparison' in f.name), None)
        total_img = next((f for f in viz_files if 'total' in f.name), None)

        # Generate HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>California Reservoir Monitoring Dashboard</title>
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

        .data-table {{
            padding: 30px;
            background: #f8f9fa;
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

        footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}

        .timestamp {{
            background: #ecf0f1;
            padding: 15px;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>California Reservoir Monitoring Dashboard</h1>
            <p>Real-time Water Level Monitoring via MQTT & CDEC API</p>
        </header>

        <div class="timestamp">
            Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        </div>

        <div class="stats-grid">
"""

        # Add summary statistics
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
                <h3>Total Water Volume</h3>
                <div class="value">{total_water:,.1f}</div>
                <div class="label">TAF (Thousand Acre-Feet)</div>
            </div>

            <div class="stat-card">
                <h3>Active Reservoirs</h3>
                <div class="value">{num_reservoirs}</div>
                <div class="label">Monitoring Locations</div>
            </div>

            <div class="stat-card">
                <h3>Reporting Period</h3>
                <div class="value">{num_days}</div>
                <div class="label">Days of Data</div>
            </div>

            <div class="stat-card">
                <h3>Data Points</h3>
                <div class="value">{total_messages}</div>
                <div class="label">Total Readings</div>
            </div>
"""

        html += """
        </div>

        <div class="charts-section">
"""

        # Add charts
        if timeseries_img:
            img_data = self.image_to_base64(timeseries_img)
            html += f"""
            <div class="chart-container">
                <h2>Water Levels Over Time</h2>
                <img src="data:image/png;base64,{img_data}" alt="Water Levels Time Series">
            </div>
"""

        if comparison_img:
            img_data = self.image_to_base64(comparison_img)
            html += f"""
            <div class="chart-container">
                <h2>Current Levels Comparison</h2>
                <img src="data:image/png;base64,{img_data}" alt="Water Levels Comparison">
            </div>
"""

        if total_img:
            img_data = self.image_to_base64(total_img)
            html += f"""
            <div class="chart-container">
                <h2>Total Capacity Trend</h2>
                <img src="data:image/png;base64,{img_data}" alt="Total Capacity">
            </div>
"""

        html += """
        </div>

        <div class="data-table">
            <h2>Daily Water Level Summary</h2>
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

        # Add data rows
        for daily_record in sorted(self.data, key=lambda x: x['date']):
            date = daily_record['date']
            for reservoir_name, reservoir_data in daily_record['reservoirs'].items():
                css_class = f"reservoir-{reservoir_name.lower()}"
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
            <p>California Department of Water Resources - Reservoir Monitoring System</p>
            <p>Powered by MQTT Protocol & CDEC API</p>
        </footer>
    </div>
</body>
</html>
"""

        # Save HTML file
        with open(output_file, 'w') as f:
            f.write(html)

        print(f"Dashboard generated: {output_file}")
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

    # Generate dashboard
    generator = DashboardGenerator(report_file, viz_dir)
    output_file = reports_dir / f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    dashboard_path = generator.generate_html(output_file)
    print(f"\nOpen in browser: {dashboard_path.absolute()}")


if __name__ == "__main__":
    main()
