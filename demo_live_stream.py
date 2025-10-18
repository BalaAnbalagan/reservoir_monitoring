"""
Demo Live Stream Publisher
Simulates real-time data streaming by publishing messages slowly
Perfect for demonstrations to show MQTT in action
"""

import json
import time
import argparse
from datetime import datetime
from pathlib import Path
import paho.mqtt.client as mqtt


class LiveStreamDemo:
    """Simulate live streaming for demonstration purposes"""

    def __init__(self, broker_address="localhost", broker_port=1883, delay=2):
        """
        Initialize demo publisher

        Args:
            broker_address: MQTT broker address
            broker_port: MQTT broker port
            delay: Seconds between messages (default 2 for demo effect)
        """
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.delay = delay
        self.client = mqtt.Client(client_id="demo_live_stream", clean_session=True)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish

    def on_connect(self, client, userdata, flags, rc):
        """Callback for when client connects to broker"""
        if rc == 0:
            print(f"✓ Connected to MQTT Broker at {self.broker_address}:{self.broker_port}")
        else:
            print(f"✗ Failed to connect, return code {rc}")

    def on_publish(self, client, userdata, mid):
        """Callback for when message is published"""
        print(f"  ✓ Message published (ID: {mid})")

    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.broker_address, self.broker_port, keepalive=60)
            self.client.loop_start()
            time.sleep(1)
        except Exception as e:
            print(f"Error connecting to broker: {e}")
            raise

    def stream_from_json(self, json_file):
        """
        Stream data from existing JSON file with delay to simulate live data

        Args:
            json_file: Path to JSON data file
        """
        json_path = Path(json_file)

        if not json_path.exists():
            print(f"Error: {json_file} not found")
            return

        with open(json_path, 'r') as f:
            data = json.load(f)

        # Extract reservoir name from filename
        reservoir_name = json_path.stem.replace('_WML', '')
        topic = f"{reservoir_name}/WML"

        print(f"\n{'='*60}")
        print(f"LIVE STREAM DEMO - {reservoir_name}")
        print(f"{'='*60}")
        print(f"Topic: {topic}")
        print(f"Records: {len(data)}")
        print(f"Delay: {self.delay} seconds between messages")
        print(f"{'='*60}\n")

        for i, record in enumerate(data, 1):
            # Add live streaming metadata
            message = {
                **record,
                "published_at": datetime.now().isoformat(),
                "source": "LIVE_STREAM_DEMO",
                "message_number": i,
                "total_messages": len(data)
            }

            # Publish message
            payload = json.dumps(message, indent=2)
            result = self.client.publish(topic, payload, qos=1)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"[{i}/{len(data)}] 📡 Streaming: {record['date']} - {record['water_level_taf']} TAF")
            else:
                print(f"[{i}/{len(data)}] ✗ Failed to publish")

            # Wait before next message (creates live effect)
            if i < len(data):
                print(f"     ⏳ Waiting {self.delay} seconds for next reading...")
                time.sleep(self.delay)

        print(f"\n{'='*60}")
        print(f"✓ Stream complete - {len(data)} messages sent")
        print(f"{'='*60}\n")

    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from MQTT broker")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Live stream demo - Publish data slowly to simulate real-time streaming'
    )
    parser.add_argument(
        '--reservoir',
        type=str,
        default='SHASTA',
        help='Reservoir name (default: SHASTA)'
    )
    parser.add_argument(
        '--delay',
        type=int,
        default=2,
        help='Seconds between messages (default: 2 for demo effect)'
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

    args = parser.parse_args()

    # Find JSON file
    data_dir = Path(__file__).parent / 'data'
    json_file = data_dir / f'{args.reservoir}_WML.json'

    if not json_file.exists():
        print(f"Error: {json_file} not found")
        print(f"Available files:")
        for f in data_dir.glob('*_WML.json'):
            print(f"  - {f.stem.replace('_WML', '')}")
        return

    # Initialize demo publisher
    demo = LiveStreamDemo(
        broker_address=args.broker,
        broker_port=args.port,
        delay=args.delay
    )

    try:
        demo.connect()
        demo.stream_from_json(json_file)
        time.sleep(2)  # Wait for final messages

    except KeyboardInterrupt:
        print("\n\nDemo stopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        demo.disconnect()


if __name__ == "__main__":
    main()
