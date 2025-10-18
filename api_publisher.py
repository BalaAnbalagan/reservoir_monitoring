"""
MQTT Publisher for Real-Time CDEC Reservoir Data
Fetches live data from California Data Exchange Center (CDEC) API
and publishes to MQTT topics
"""

import json
import time
import argparse
import requests
from datetime import datetime, timedelta
from pathlib import Path
import paho.mqtt.client as mqtt
from io import StringIO
import csv


class CDECAPIPublisher:
    """MQTT Publisher that fetches real-time data from CDEC API"""

    # CDEC Station IDs for major California reservoirs
    # Based on CDEC Major Reservoirs list
    RESERVOIR_STATIONS = {
        'SHASTA': 'SHA',
        'OROVILLE': 'ORO',
        'TRINITY': 'CLR',  # Clair Engle Lake (Trinity)
        'NEW_MELONES': 'NML',
        'DON_PEDRO': 'DNP',
        'EXCHEQUER': 'EXC',
        'FOLSOM': 'FOL',
        'NEW_BULLARDS_BAR': 'NBB',
        'SAN_LUIS': 'SLS',
        'CACHUMA': 'CCH',
        'CASTAIC': 'CAS',
        'CASITAS': 'CST',
        'DIAMOND_VALLEY': 'DMV',
        'MILLERTON': 'MIL',
        'PINE_FLAT': 'PNF',
        'SONOMA': 'SLT',  # Lake Sonoma
        'MCCLURE': 'MCL',
        'BERRYESSA': 'BER',
        'CAMANCHE': 'CMN',
        'ISABELLA': 'ISB',
        'PERRIS': 'PRR'
    }

    def __init__(self, broker_address="localhost", broker_port=1883):
        """
        Initialize MQTT publisher with CDEC API integration

        Args:
            broker_address: MQTT broker address
            broker_port: MQTT broker port
        """
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client(client_id="cdec_api_publisher", clean_session=True)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish

    def on_connect(self, client, userdata, flags, rc):
        """Callback for when client connects to broker"""
        if rc == 0:
            print(f"Connected to MQTT Broker at {self.broker_address}:{self.broker_port}")
        else:
            print(f"Failed to connect, return code {rc}")

    def on_publish(self, client, userdata, mid):
        """Callback for when message is published"""
        print(f"  -> Message published (ID: {mid})")

    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.broker_address, self.broker_port, keepalive=60)
            self.client.loop_start()
            time.sleep(1)  # Wait for connection
        except Exception as e:
            print(f"Error connecting to broker: {e}")
            raise

    def fetch_cdec_data(self, station_id, start_date, end_date):
        """
        Fetch reservoir data from CDEC API

        Args:
            station_id: CDEC station ID (e.g., 'SHA' for Shasta)
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            List of data records
        """
        # CDEC CSV Data Servlet URL
        # Sensor 15 = Reservoir Storage
        # dur_code D = Daily
        url = (
            f"https://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?"
            f"Stations={station_id}&SensorNums=15&dur_code=D&"
            f"Start={start_date}&End={end_date}"
        )

        print(f"\nFetching data from CDEC API...")
        print(f"  Station: {station_id}")
        print(f"  Date Range: {start_date} to {end_date}")
        print(f"  URL: {url}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Parse CSV data
            csv_data = StringIO(response.text)
            reader = csv.DictReader(csv_data)

            records = []
            for row in reader:
                # Skip rows with missing data
                value_str = row['VALUE'].strip()
                if not value_str or value_str == '---':
                    continue

                try:
                    # Convert acre-feet (AF) to thousand acre-feet (TAF)
                    value_af = float(value_str)
                    value_taf = round(value_af / 1000, 2)

                    # Parse date
                    date_str = row['DATE TIME'].strip()
                    date_obj = datetime.strptime(date_str, '%Y%m%d %H%M')

                    record = {
                        'date': date_obj.strftime('%m/%d/%Y'),
                        'water_level_taf': value_taf,
                        'timestamp': date_obj.isoformat()
                    }
                    records.append(record)
                except (ValueError, KeyError) as e:
                    # Skip invalid records
                    continue

            print(f"  -> Fetched {len(records)} records")
            return records

        except requests.RequestException as e:
            print(f"  -> Error fetching data: {e}")
            return []
        except Exception as e:
            print(f"  -> Error parsing data: {e}")
            return []

    def publish_data(self, reservoir_id, data):
        """
        Publish reservoir data to MQTT topic

        Args:
            reservoir_id: Reservoir identifier (e.g., 'SHASTA')
            data: List of data records to publish
        """
        if not data:
            print(f"No data to publish for {reservoir_id}")
            return

        topic = f"{reservoir_id}/WML"
        print(f"\nPublishing data for {reservoir_id} to topic: {topic}")

        for record in data:
            # Add reservoir_id and publishing timestamp
            message = {
                "reservoir_id": reservoir_id,
                **record,
                "published_at": datetime.now().isoformat(),
                "source": "CDEC_API"
            }

            # Publish message
            payload = json.dumps(message)
            result = self.client.publish(topic, payload, qos=1)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Published: {record['date']} - {record['water_level_taf']} TAF")
            else:
                print(f"Failed to publish message")

            time.sleep(0.5)  # Small delay between messages

    def publish_realtime_data(self, reservoirs=None, days_back=7):
        """
        Fetch and publish real-time data from CDEC

        Args:
            reservoirs: List of reservoir names (default: all)
            days_back: Number of days of historical data to fetch
        """
        if reservoirs is None:
            reservoirs = list(self.RESERVOIR_STATIONS.keys())

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        print("\n" + "="*60)
        print("FETCHING REAL-TIME DATA FROM CDEC API")
        print("="*60)
        print(f"Date Range: {start_date_str} to {end_date_str}")
        print(f"Reservoirs: {', '.join(reservoirs)}")
        print("="*60)

        for reservoir_name in reservoirs:
            if reservoir_name not in self.RESERVOIR_STATIONS:
                print(f"Warning: Unknown reservoir {reservoir_name}")
                continue

            station_id = self.RESERVOIR_STATIONS[reservoir_name]

            print(f"\n{'='*60}")
            print(f"Processing {reservoir_name} (Station: {station_id})")
            print('='*60)

            # Fetch data from API
            data = self.fetch_cdec_data(station_id, start_date_str, end_date_str)

            # Publish to MQTT
            if data:
                self.publish_data(reservoir_name, data)
            else:
                print(f"  -> No data available for {reservoir_name}")

        print("\n" + "="*60)
        print("DATA PUBLISHING COMPLETE")
        print("="*60)

    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
        print("\nDisconnected from MQTT broker")


def main():
    """Main function to run API publisher"""
    parser = argparse.ArgumentParser(
        description='Fetch real-time reservoir data from CDEC API and publish to MQTT'
    )
    parser.add_argument(
        '--reservoir',
        type=str,
        default='ALL',
        help='Reservoir to publish data for (use reservoir name or ALL for all reservoirs)'
    )
    parser.add_argument(
        '--broker',
        type=str,
        default='localhost',
        help='MQTT broker address (default: localhost)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=1883,
        help='MQTT broker port (default: 1883)'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days of historical data to fetch (default: 7)'
    )

    args = parser.parse_args()

    # Initialize publisher
    publisher = CDECAPIPublisher(broker_address=args.broker, broker_port=args.port)

    try:
        publisher.connect()

        # Determine which reservoirs to publish
        if args.reservoir == 'ALL':
            reservoirs = list(publisher.RESERVOIR_STATIONS.keys())
        else:
            # Support comma-separated list
            reservoirs = [r.strip().upper() for r in args.reservoir.split(',')]

        # Fetch and publish real-time data
        publisher.publish_realtime_data(reservoirs=reservoirs, days_back=args.days)

        time.sleep(2)  # Wait for all messages to be sent

    except KeyboardInterrupt:
        print("\n\nPublisher stopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        publisher.disconnect()


if __name__ == "__main__":
    main()
