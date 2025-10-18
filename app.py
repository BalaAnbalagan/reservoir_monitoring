"""
Flask Web Application for Reservoir Monitoring Dashboard
A lightweight, dynamic dashboard that can be deployed to free hosting services
"""

from flask import Flask, render_template, jsonify, send_from_directory
from pathlib import Path
import json
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Configure paths
BASE_DIR = Path(__file__).parent
REPORTS_DIR = BASE_DIR / 'reports'
DATA_DIR = BASE_DIR / 'data'


def get_latest_report():
    """Get the latest comprehensive report"""
    try:
        json_files = sorted(REPORTS_DIR.glob('comprehensive_report_*.json'))
        if json_files:
            with open(json_files[-1], 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading report: {e}")
    return []


def get_summary_stats(data):
    """Calculate summary statistics from report data"""
    if not data:
        return {}

    latest = data[-1] if data else {}
    first = data[0] if data else {}

    total_water_latest = latest.get('total_water_level_taf', 0)

    # Calculate period change only for reservoirs that exist in both first and last day
    common_reservoirs = set(first.get('reservoirs', {}).keys()) & set(latest.get('reservoirs', {}).keys())

    first_total = sum(
        first['reservoirs'][r]['average_water_level_taf']
        for r in common_reservoirs
    ) if common_reservoirs else 0

    latest_total = sum(
        latest['reservoirs'][r]['average_water_level_taf']
        for r in common_reservoirs
    ) if common_reservoirs else 0

    period_change = latest_total - first_total

    return {
        'total_water': total_water_latest,
        'period_change': period_change,
        'num_reservoirs': len(latest.get('reservoirs', {})),
        'num_reservoirs_tracked': len(common_reservoirs),
        'num_days': len(data),
        'date_range': {
            'start': first.get('date', 'N/A'),
            'end': latest.get('date', 'N/A')
        }
    }


def calculate_changes(data):
    """Calculate day-over-day changes"""
    if len(data) < 2:
        return []

    changes = []
    for i in range(1, len(data)):
        prev_day = data[i-1]
        curr_day = data[i]

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


@app.route('/')
def index():
    """Main dashboard page"""
    data = get_latest_report()
    stats = get_summary_stats(data)

    return render_template('index.html',
                         stats=stats,
                         last_update=datetime.now().strftime('%B %d, %Y at %I:%M %p'))


@app.route('/api/summary')
def api_summary():
    """API endpoint for summary statistics"""
    data = get_latest_report()
    stats = get_summary_stats(data)
    return jsonify(stats)


@app.route('/api/latest')
def api_latest():
    """API endpoint for latest data"""
    data = get_latest_report()
    if data:
        return jsonify(data[-1])
    return jsonify({})


@app.route('/api/historical')
def api_historical():
    """API endpoint for all historical data"""
    data = get_latest_report()
    return jsonify(data)


@app.route('/api/changes')
def api_changes():
    """API endpoint for day-over-day changes"""
    data = get_latest_report()
    changes = calculate_changes(data)
    return jsonify(changes)


@app.route('/api/reservoir/<reservoir_name>')
def api_reservoir(reservoir_name):
    """API endpoint for specific reservoir data"""
    data = get_latest_report()
    reservoir_data = []

    for day in data:
        if reservoir_name.upper() in day.get('reservoirs', {}):
            res_data = day['reservoirs'][reservoir_name.upper()]
            reservoir_data.append({
                'date': day['date'],
                **res_data
            })

    return jsonify(reservoir_data)


@app.route('/detailed')
def detailed():
    """Detailed view with all data"""
    data = get_latest_report()
    changes = calculate_changes(data)
    stats = get_summary_stats(data)

    return render_template('detailed.html',
                         data=data,
                         changes=changes,
                         stats=stats,
                         last_update=datetime.now().strftime('%B %d, %Y at %I:%M %p'))


@app.route('/detailed/charts')
def detailed_charts():
    """Detailed view with interactive charts"""
    data = get_latest_report()
    changes = calculate_changes(data)
    stats = get_summary_stats(data)

    # Prepare chart data
    chart_data = prepare_chart_data(data)

    return render_template('detailed_charts.html',
                         chart_data=chart_data,
                         stats=stats,
                         last_update=datetime.now().strftime('%B %d, %Y at %I:%M %p'))


def prepare_chart_data(data):
    """Prepare data for Chart.js visualizations"""
    if not data:
        return {}

    # Get latest day data for current levels
    latest = data[-1]
    reservoirs = latest.get('reservoirs', {})

    # Current levels (sorted by value)
    current_sorted = sorted(reservoirs.items(), key=lambda x: x[1]['average_water_level_taf'], reverse=True)
    current_labels = [name for name, _ in current_sorted]
    current_values = [res_data['average_water_level_taf'] for _, res_data in current_sorted]

    # Top 10 reservoirs
    top10_labels = current_labels[:10]
    top10_values = current_values[:10]

    # Stacked bar data (all reservoirs over time)
    all_reservoir_names = set()
    for day in data:
        all_reservoir_names.update(day.get('reservoirs', {}).keys())

    stacked_reservoirs = []
    for res_name in sorted(all_reservoir_names):
        values = []
        for day in data:
            if res_name in day.get('reservoirs', {}):
                values.append(day['reservoirs'][res_name]['average_water_level_taf'])
            else:
                values.append(0)
        stacked_reservoirs.append({
            'name': res_name,
            'values': values
        })

    # Changes data (first to last day)
    if len(data) >= 2:
        first = data[0]
        last = data[-1]
        changes_data = {}

        for res_name in all_reservoir_names:
            if res_name in first.get('reservoirs', {}) and res_name in last.get('reservoirs', {}):
                first_val = first['reservoirs'][res_name]['average_water_level_taf']
                last_val = last['reservoirs'][res_name]['average_water_level_taf']
                changes_data[res_name] = last_val - first_val

        changes_sorted = sorted(changes_data.items(), key=lambda x: abs(x[1]), reverse=True)
        changes_labels = [name for name, _ in changes_sorted]
        changes_values = [change for _, change in changes_sorted]
    else:
        changes_labels = []
        changes_values = []

    # Comparison data (all days, common reservoirs)
    common_reservoirs = set(data[0].get('reservoirs', {}).keys())
    for day in data[1:]:
        common_reservoirs &= set(day.get('reservoirs', {}).keys())

    comparison_data = []
    for day in data:
        day_values = []
        for res_name in sorted(common_reservoirs):
            if res_name in day.get('reservoirs', {}):
                day_values.append(day['reservoirs'][res_name]['average_water_level_taf'])
            else:
                day_values.append(0)
        comparison_data.append(day_values)

    return {
        'current': {
            'labels': current_labels,
            'values': current_values
        },
        'top10': {
            'labels': top10_labels,
            'values': top10_values
        },
        'stacked': {
            'dates': [day['date'] for day in data],
            'reservoirs': stacked_reservoirs
        },
        'changes': {
            'labels': changes_labels,
            'values': changes_values
        },
        'comparison': {
            'dates': [day['date'] for day in data],
            'reservoirs': sorted(common_reservoirs),
            'data': comparison_data
        }
    }


@app.route('/visualizations/<path:filename>')
def visualizations(filename):
    """Serve visualization images"""
    viz_dir = REPORTS_DIR / 'visualizations'
    return send_from_directory(viz_dir, filename)


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = BASE_DIR / 'templates'
    templates_dir.mkdir(exist_ok=True)

    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
