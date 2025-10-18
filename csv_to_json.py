"""
CSV to JSON Converter for Reservoir Water Mark Level Data
Converts CSV files containing reservoir data to JSON format
"""

import csv
import json
from datetime import datetime
from pathlib import Path


def csv_to_json(csv_file_path, reservoir_id):
    """
    Convert CSV file to JSON format for reservoir data

    Args:
        csv_file_path: Path to the CSV file
        reservoir_id: Reservoir identifier (e.g., 'SHASTA', 'OROVILLE', 'SONOMA')

    Returns:
        List of dictionaries containing reservoir data
    """
    json_data = []

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            # Parse date and TAF value
            date_str = row['Date'].strip()
            taf_value = float(row['TAF'].strip())

            # Create JSON record
            record = {
                "reservoir_id": reservoir_id,
                "date": date_str,
                "water_level_taf": taf_value,
                "timestamp": datetime.strptime(date_str, "%m/%d/%Y").isoformat()
            }

            json_data.append(record)

    return json_data


def save_json(data, output_path):
    """Save data to JSON file"""
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)
    print(f"Saved JSON data to {output_path}")


def main():
    """Convert all reservoir CSV files to JSON"""
    data_dir = Path(__file__).parent / 'data'

    reservoirs = {
        'SHASTA': 'Shasta_WML.csv',
        'OROVILLE': 'Oroville_WML.csv',
        'SONOMA': 'Sonoma_WML.csv'
    }

    for reservoir_id, csv_filename in reservoirs.items():
        csv_path = data_dir / csv_filename
        json_path = data_dir / f'{reservoir_id}_WML.json'

        if csv_path.exists():
            print(f"Converting {csv_filename} to JSON...")
            json_data = csv_to_json(csv_path, reservoir_id)
            save_json(json_data, json_path)
            print(f"  -> {len(json_data)} records converted for {reservoir_id}\n")
        else:
            print(f"Warning: {csv_path} not found\n")


if __name__ == "__main__":
    main()
