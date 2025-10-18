"""
MQTT Subscriber for Reservoir Data Collection
Single subscriber that collects Water Mark Level (WML) data from all reservoir topics
Aggregates data and generates daily reports

Supports both local and cloud MQTT brokers
"""

import json
import time
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import paho.mqtt.client as mqtt
import ssl
from mqtt_config import get_mqtt_config, print_config


class ReservoirSubscriber:
    """MQTT Subscriber that collects data from all reservoir topics"""

    def __init__(self, broker_address=None, broker_port=None, username=None, password=None, use_tls=False):
        """
        Initialize MQTT subscriber

        Args:
            broker_address: MQTT broker address (if None, uses config)
            broker_port: MQTT broker port (if None, uses config)
            username: MQTT username (optional)
            password: MQTT password (optional)
            use_tls: Enable TLS/SSL (for cloud brokers)
        """
        # Get config from mqtt_config if not provided
        if broker_address is None:
            config = get_mqtt_config()
            self.broker_address = config['broker']
            self.broker_port = config['port']
            self.username = config.get('username')
            self.password = config.get('password')
            self.use_tls = config.get('use_tls', False)
        else:
            self.broker_address = broker_address
            self.broker_port = broker_port
            self.username = username
            self.password = password
            self.use_tls = use_tls

        self.client = mqtt.Client(client_id="reservoir_subscriber", clean_session=True)

        # Set username/password if provided
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)

        # Enable TLS if required (for cloud brokers like HiveMQ)
        if self.use_tls:
            self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
            self.client.tls_insecure_set(False)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Store collected data organized by date and reservoir
        self.collected_data = defaultdict(lambda: defaultdict(list))
        self.message_count = 0

    def on_connect(self, client, userdata, flags, rc):
        """Callback for when client connects to broker"""
        if rc == 0:
            print(f"Connected to MQTT Broker at {self.broker_address}:{self.broker_port}")
            print("Subscribing to all reservoir topics...")

            # Subscribe to all reservoir WML topics using wildcard
            # This subscribes to ALL reservoirs automatically
            topic = "+/WML"  # + is wildcard for single level
            self.client.subscribe(topic, qos=1)
            print(f"  -> Subscribed to: {topic} (all reservoirs)")

        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        """
        Callback for when a message is received

        Args:
            msg: MQTT message containing reservoir data
        """
        try:
            # Parse message payload
            data = json.loads(msg.payload.decode())
            reservoir_id = data['reservoir_id']
            date = data['date']
            water_level = data['water_level_taf']

            # Store data organized by date and reservoir
            self.collected_data[date][reservoir_id].append(data)
            self.message_count += 1

            print(f"\n[Message {self.message_count}] Received from topic: {msg.topic}")
            print(f"  Reservoir: {reservoir_id}")
            print(f"  Date: {date}")
            print(f"  Water Level: {water_level} TAF")

        except Exception as e:
            print(f"Error processing message: {e}")

    def connect(self):
        """Connect to MQTT broker and start listening"""
        try:
            self.client.connect(self.broker_address, self.broker_port, keepalive=60)
            print(f"\nStarting MQTT subscriber...")
        except Exception as e:
            print(f"Error connecting to broker: {e}")
            raise

    def start_listening(self, duration=None):
        """
        Start listening for messages

        Args:
            duration: How long to listen in seconds (None for indefinite)
        """
        print(f"\nListening for messages... (Press Ctrl+C to stop)\n")
        print("="*60)

        try:
            if duration:
                self.client.loop_start()
                time.sleep(duration)
                self.client.loop_stop()
            else:
                self.client.loop_forever()

        except KeyboardInterrupt:
            print("\n\nSubscriber stopped by user")

    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.disconnect()
        print("\nDisconnected from MQTT broker")

    def generate_daily_report(self, output_dir=None):
        """
        Generate daily summary reports from collected data

        Args:
            output_dir: Directory to save reports (default: reports/)
        """
        if not self.collected_data:
            print("\nNo data collected to generate report")
            return

        if output_dir is None:
            output_dir = Path(__file__).parent / 'reports'

        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        print("\n" + "="*60)
        print("GENERATING DAILY REPORTS")
        print("="*60)

        # Generate report for each date
        all_reports = []

        for date in sorted(self.collected_data.keys()):
            print(f"\nDate: {date}")
            print("-" * 40)

            daily_summary = {
                "date": date,
                "reservoirs": {},
                "total_water_level_taf": 0,
                "report_generated_at": datetime.now().isoformat()
            }

            # Process each reservoir for this date
            for reservoir_id, records in self.collected_data[date].items():
                # Calculate statistics
                water_levels = [r['water_level_taf'] for r in records]
                avg_level = sum(water_levels) / len(water_levels)

                reservoir_summary = {
                    "reservoir_id": reservoir_id,
                    "average_water_level_taf": round(avg_level, 2),
                    "min_water_level_taf": min(water_levels),
                    "max_water_level_taf": max(water_levels),
                    "readings_count": len(water_levels),
                    "readings": records
                }

                daily_summary["reservoirs"][reservoir_id] = reservoir_summary
                daily_summary["total_water_level_taf"] += avg_level

                print(f"  {reservoir_id}:")
                print(f"    Average: {avg_level:.2f} TAF")
                print(f"    Min: {min(water_levels):.2f} TAF")
                print(f"    Max: {max(water_levels):.2f} TAF")
                print(f"    Readings: {len(water_levels)}")

            daily_summary["total_water_level_taf"] = round(
                daily_summary["total_water_level_taf"], 2
            )

            print(f"\n  Total Water (All Reservoirs): {daily_summary['total_water_level_taf']} TAF")

            all_reports.append(daily_summary)

        # Save comprehensive report to JSON
        report_file = output_dir / f"comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(all_reports, f, indent=2)

        print("\n" + "="*60)
        print(f"Report saved to: {report_file}")
        print(f"Total messages processed: {self.message_count}")
        print("="*60)

        # Save to MongoDB (if enabled)
        try:
            from db_config import DatabaseManager
            db = DatabaseManager()
            if db.mode == 'mongodb':
                print("\n[MongoDB] Saving reports to database...")
                db.save_daily_report(all_reports)
            db.close()
        except Exception as e:
            print(f"\n[MongoDB] Skipping database save: {e}")

        # Generate human-readable summary
        self.generate_text_report(all_reports, output_dir)

    def generate_text_report(self, reports, output_dir):
        """Generate human-readable text report"""
        report_file = output_dir / f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(report_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write("CALIFORNIA DEPARTMENT OF WATER RESOURCES\n")
            f.write("RESERVOIR WATER MARK LEVEL DAILY SUMMARY REPORT\n")
            f.write("="*80 + "\n\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Messages Collected: {self.message_count}\n")
            f.write(f"Reporting Period: {len(reports)} days\n")
            f.write("\n" + "="*80 + "\n\n")

            for daily_report in reports:
                f.write(f"DATE: {daily_report['date']}\n")
                f.write("-"*80 + "\n\n")

                for reservoir_id, data in daily_report['reservoirs'].items():
                    f.write(f"  {reservoir_id} RESERVOIR:\n")
                    f.write(f"    Average Water Level: {data['average_water_level_taf']:>10.2f} TAF\n")
                    f.write(f"    Minimum Water Level: {data['min_water_level_taf']:>10.2f} TAF\n")
                    f.write(f"    Maximum Water Level: {data['max_water_level_taf']:>10.2f} TAF\n")
                    f.write(f"    Number of Readings:  {data['readings_count']:>10}\n")
                    f.write("\n")

                f.write(f"  TOTAL WATER LEVEL (All Reservoirs): {daily_report['total_water_level_taf']:>10.2f} TAF\n")
                f.write("\n" + "="*80 + "\n\n")

        print(f"Text summary saved to: {report_file}")


def main():
    """Main function to run subscriber"""
    parser = argparse.ArgumentParser(description='Subscribe to reservoir WML data from MQTT')
    parser.add_argument('--broker', type=str, default='localhost',
                        help='MQTT broker address (default: localhost)')
    parser.add_argument('--port', type=int, default=1883,
                        help='MQTT broker port (default: 1883)')
    parser.add_argument('--duration', type=int, default=30,
                        help='How long to listen in seconds (default: 30)')

    args = parser.parse_args()

    # Print MQTT configuration
    print_config()

    # Initialize subscriber
    # If --broker is specified, use it; otherwise use config from mqtt_config
    if args.broker != 'localhost' or args.port != 1883:
        # Command-line args provided
        subscriber = ReservoirSubscriber(broker_address=args.broker, broker_port=args.port)
    else:
        # Use mqtt_config.py settings
        subscriber = ReservoirSubscriber()

    try:
        subscriber.connect()
        subscriber.start_listening(duration=args.duration)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        subscriber.disconnect()
        subscriber.generate_daily_report()


if __name__ == "__main__":
    main()
