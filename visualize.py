"""
Reservoir Data Visualization Tool
Generates charts and graphs from JSON reports
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class ReservoirVisualizer:
    """Visualize reservoir data from JSON reports"""

    def __init__(self, report_file):
        """
        Initialize visualizer with report file

        Args:
            report_file: Path to JSON report file
        """
        self.report_file = Path(report_file)
        self.data = self.load_data()

    def load_data(self):
        """Load data from JSON report"""
        with open(self.report_file, 'r') as f:
            return json.load(f)

    def extract_time_series(self):
        """
        Extract time series data for each reservoir

        Returns:
            Dictionary with reservoir names as keys and (dates, levels) as values
        """
        reservoirs_data = {}

        for daily_record in self.data:
            date_str = daily_record['date']
            date_obj = datetime.strptime(date_str, '%m/%d/%Y')

            for reservoir_name, reservoir_data in daily_record['reservoirs'].items():
                if reservoir_name not in reservoirs_data:
                    reservoirs_data[reservoir_name] = {
                        'dates': [],
                        'levels': [],
                        'min_levels': [],
                        'max_levels': []
                    }

                reservoirs_data[reservoir_name]['dates'].append(date_obj)
                reservoirs_data[reservoir_name]['levels'].append(
                    reservoir_data['average_water_level_taf']
                )
                reservoirs_data[reservoir_name]['min_levels'].append(
                    reservoir_data['min_water_level_taf']
                )
                reservoirs_data[reservoir_name]['max_levels'].append(
                    reservoir_data['max_water_level_taf']
                )

        return reservoirs_data

    def plot_water_levels(self, output_file=None):
        """
        Plot water levels over time for all reservoirs

        Args:
            output_file: Path to save the plot (if None, displays plot)
        """
        data = self.extract_time_series()

        plt.figure(figsize=(14, 8))

        # Color scheme for different reservoirs
        colors = {
            'SHASTA': '#1f77b4',
            'OROVILLE': '#ff7f0e',
            'SONOMA': '#2ca02c'
        }

        for reservoir_name, reservoir_data in data.items():
            color = colors.get(reservoir_name, '#000000')
            plt.plot(
                reservoir_data['dates'],
                reservoir_data['levels'],
                marker='o',
                label=reservoir_name,
                color=color,
                linewidth=2,
                markersize=6
            )

        plt.xlabel('Date', fontsize=12, fontweight='bold')
        plt.ylabel('Water Level (TAF)', fontsize=12, fontweight='bold')
        plt.title('California Reservoir Water Levels Over Time', fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)

        # Format x-axis dates
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        plt.gcf().autofmt_xdate()

        plt.tight_layout()

        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Chart saved to: {output_file}")
        else:
            plt.show()

    def plot_comparison_bar(self, output_file=None):
        """
        Create bar chart comparing latest water levels

        Args:
            output_file: Path to save the plot (if None, displays plot)
        """
        # Get latest data for each reservoir
        latest_data = {}
        if self.data:
            latest_record = self.data[-1]
            for reservoir_name, reservoir_data in latest_record['reservoirs'].items():
                latest_data[reservoir_name] = reservoir_data['average_water_level_taf']

        reservoirs = list(latest_data.keys())
        levels = list(latest_data.values())

        plt.figure(figsize=(10, 6))

        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
        bars = plt.bar(reservoirs, levels, color=colors[:len(reservoirs)], alpha=0.8, edgecolor='black')

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f} TAF',
                    ha='center', va='bottom', fontweight='bold')

        plt.xlabel('Reservoir', fontsize=12, fontweight='bold')
        plt.ylabel('Water Level (TAF)', fontsize=12, fontweight='bold')
        plt.title('Current Reservoir Water Levels Comparison', fontsize=14, fontweight='bold')
        plt.grid(True, axis='y', alpha=0.3)

        plt.tight_layout()

        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Chart saved to: {output_file}")
        else:
            plt.show()

    def plot_total_capacity(self, output_file=None):
        """
        Plot total water capacity over time

        Args:
            output_file: Path to save the plot (if None, displays plot)
        """
        dates = []
        totals = []

        for daily_record in self.data:
            date_str = daily_record['date']
            date_obj = datetime.strptime(date_str, '%m/%d/%Y')
            dates.append(date_obj)
            totals.append(daily_record['total_water_level_taf'])

        plt.figure(figsize=(12, 6))

        plt.fill_between(dates, totals, alpha=0.3, color='#3498db')
        plt.plot(dates, totals, marker='o', color='#2c3e50', linewidth=2, markersize=6)

        plt.xlabel('Date', fontsize=12, fontweight='bold')
        plt.ylabel('Total Water Level (TAF)', fontsize=12, fontweight='bold')
        plt.title('Total Water Capacity Across All Reservoirs', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)

        # Format x-axis dates
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        plt.gcf().autofmt_xdate()

        plt.tight_layout()

        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Chart saved to: {output_file}")
        else:
            plt.show()

    def generate_all_charts(self, output_dir=None):
        """
        Generate all visualization charts

        Args:
            output_dir: Directory to save charts
        """
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True)
        else:
            output_dir = self.report_file.parent / 'visualizations'
            output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        print("\n" + "="*60)
        print("GENERATING VISUALIZATIONS")
        print("="*60)

        # Generate time series chart
        print("\n1. Water Levels Over Time...")
        time_series_file = output_dir / f'water_levels_timeseries_{timestamp}.png'
        self.plot_water_levels(output_file=time_series_file)

        # Generate comparison bar chart
        print("\n2. Current Levels Comparison...")
        comparison_file = output_dir / f'water_levels_comparison_{timestamp}.png'
        self.plot_comparison_bar(output_file=comparison_file)

        # Generate total capacity chart
        print("\n3. Total Capacity Over Time...")
        total_file = output_dir / f'total_capacity_{timestamp}.png'
        self.plot_total_capacity(output_file=total_file)

        print("\n" + "="*60)
        print(f"All charts saved to: {output_dir}")
        print("="*60)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Visualize reservoir data from JSON reports')
    parser.add_argument(
        '--report',
        type=str,
        help='Path to JSON report file (default: latest report in reports/)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output directory for charts (default: reports/visualizations/)'
    )
    parser.add_argument(
        '--type',
        type=str,
        choices=['timeseries', 'comparison', 'total', 'all'],
        default='all',
        help='Type of chart to generate (default: all)'
    )
    parser.add_argument(
        '--show',
        action='store_true',
        help='Display charts instead of saving'
    )

    args = parser.parse_args()

    # Find latest report if not specified
    if args.report:
        report_file = args.report
    else:
        reports_dir = Path(__file__).parent / 'reports'
        json_files = sorted(reports_dir.glob('comprehensive_report_*.json'))
        if not json_files:
            print("Error: No report files found in reports/")
            return
        report_file = json_files[-1]
        print(f"Using latest report: {report_file}")

    # Initialize visualizer
    visualizer = ReservoirVisualizer(report_file)

    # Generate charts
    output_file = None if args.show else args.output

    if args.type == 'all':
        visualizer.generate_all_charts(output_dir=output_file)
    elif args.type == 'timeseries':
        visualizer.plot_water_levels(output_file=output_file)
    elif args.type == 'comparison':
        visualizer.plot_comparison_bar(output_file=output_file)
    elif args.type == 'total':
        visualizer.plot_total_capacity(output_file=output_file)


if __name__ == "__main__":
    main()
