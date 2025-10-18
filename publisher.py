"""
MQTT Publisher for Reservoir Sensors
Simulates reservoir sensors publishing Water Mark Level (WML) data to MQTT topics
Each reservoir publishes to its own topic: RESERVOIR_ID/WML
"""

import json
import time
import argparse
from pathlib import Path
import paho.mqtt.client as mqtt
from datetime import datetime


class ReservoirPublisher:
    """MQTT Publisher for reservoir sensor data"""

    def __init__(self, broker_address="localhost", broker_port=1883):
        """
        Initialize MQTT publisher

        Args:
            broker_address: MQTT broker address
            broker_port: MQTT broker port
        """
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311)
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

    def publish_data(self, reservoir_id, data):
        """
        Publish reservoir data to MQTT topic

        Args:
            reservoir_id: Reservoir identifier (e.g., 'SHASTA')
            data: List of data records to publish
        """
        topic = f"{reservoir_id}/WML"
        print(f"\nPublishing data for {reservoir_id} to topic: {topic}")

        for record in data:
            # Add publishing timestamp
            message = {
                **record,
                "published_at": datetime.now().isoformat()
            }

            # Publish message
            payload = json.dumps(message)
            result = self.client.publish(topic, payload, qos=1)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Published: {record['date']} - {record['water_level_taf']} TAF")
            else:
                print(f"Failed to publish message")

            time.sleep(0.5)  # Small delay between messages

    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
        print("\nDisconnected from MQTT broker")


def load_json_data(json_file_path):
    """Load reservoir data from JSON file"""
    with open(json_file_path, 'r') as f:
        return json.load(f)


def main():
    """Main function to run publisher"""
    parser = argparse.ArgumentParser(description='Publish reservoir WML data to MQTT')
    parser.add_argument('--reservoir', type=str, choices=['SHASTA', 'OROVILLE', 'SONOMA', 'ALL'],
                        default='ALL', help='Reservoir to publish data for')
    parser.add_argument('--broker', type=str, default='localhost',
                        help='MQTT broker address (default: localhost)')
    parser.add_argument('--port', type=int, default=1883,
                        help='MQTT broker port (default: 1883)')

    args = parser.parse_args()

    data_dir = Path(__file__).parent / 'data'

    # Initialize publisher
    publisher = ReservoirPublisher(broker_address=args.broker, broker_port=args.port)

    try:
        publisher.connect()

        reservoirs = ['SHASTA', 'OROVILLE', 'SONOMA'] if args.reservoir == 'ALL' else [args.reservoir]

        for reservoir_id in reservoirs:
            json_file = data_dir / f'{reservoir_id}_WML.json'

            if json_file.exists():
                print(f"\n{'='*60}")
                print(f"Loading data for {reservoir_id}")
                data = load_json_data(json_file)
                publisher.publish_data(reservoir_id, data)
            else:
                print(f"Warning: {json_file} not found. Run csv_to_json.py first.")

        time.sleep(2)  # Wait for all messages to be sent

    except KeyboardInterrupt:
        print("\n\nPublisher stopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        publisher.disconnect()


if __name__ == "__main__":
    main()
