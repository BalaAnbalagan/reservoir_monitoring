"""
Quick test script to verify MQTT connectivity
Tests both local and cloud MQTT configurations
"""
import os
import sys
from mqtt_config import get_mqtt_config, print_config

def test_mqtt():
    """Test MQTT configuration and connectivity"""

    print("\n" + "="*60)
    print("MQTT CONNECTIVITY TEST")
    print("="*60)

    # Show current configuration
    print_config()

    config = get_mqtt_config()

    print("\n[TEST] Testing connection to MQTT broker...")
    print(f"   Broker: {config['broker']}")
    print(f"   Port: {config['port']}")
    print(f"   TLS: {config.get('use_tls', False)}")

    # Try to import paho-mqtt
    try:
        import paho.mqtt.client as mqtt
        import ssl
        print("[OK] paho-mqtt library found")
    except ImportError:
        print("[ERROR] paho-mqtt not installed!")
        print("   Install with: pip install paho-mqtt")
        return False

    # Create test client
    client = mqtt.Client(client_id="test_client", clean_session=True)

    # Set credentials if provided
    if config.get('username') and config.get('password'):
        client.username_pw_set(config['username'], config['password'])
        print(f"[OK] Using authentication (user: {config['username']})")

    # Enable TLS if required
    if config.get('use_tls'):
        try:
            client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
            client.tls_insecure_set(False)
            print("[OK] TLS/SSL enabled")
        except Exception as e:
            print(f"[ERROR] TLS setup failed: {e}")
            return False

    # Connection callbacks
    connection_success = [False]

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            connection_success[0] = True
            print("\n[SUCCESS] CONNECTION SUCCESSFUL!")
            print(f"   Connected to {config['broker']}:{config['port']}")
        else:
            print(f"\n[ERROR] Connection failed with code {rc}")
            error_messages = {
                1: "Incorrect protocol version",
                2: "Invalid client identifier",
                3: "Server unavailable",
                4: "Bad username or password",
                5: "Not authorized"
            }
            print(f"   Error: {error_messages.get(rc, 'Unknown error')}")

    client.on_connect = on_connect

    # Try to connect
    try:
        print("\n[WAIT] Connecting...")
        client.connect(config['broker'], config['port'], keepalive=60)
        client.loop_start()

        # Wait a bit for connection
        import time
        time.sleep(3)

        client.loop_stop()
        client.disconnect()

        if connection_success[0]:
            print("\n[SUCCESS] MQTT broker is ready to use!")
            return True
        else:
            print("\n[ERROR] Could not establish connection")
            return False

    except Exception as e:
        print(f"\n[ERROR] Connection error: {e}")
        print("\nTroubleshooting:")
        print("  1. Check broker address is correct")
        print("  2. Verify username and password")
        print("  3. Ensure port is correct (8883 for TLS, 1883 for non-TLS)")
        print("  4. Check your internet connection (for cloud MQTT)")
        return False

if __name__ == "__main__":
    # Check if user wants to test specific environment
    if len(sys.argv) > 1:
        if sys.argv[1] in ['local', 'cloud']:
            os.environ['MQTT_ENV'] = sys.argv[1]
            print(f"\n[TEST] Testing {sys.argv[1].upper()} MQTT configuration")

    success = test_mqtt()

    if success:
        print("\n" + "="*60)
        print("[SUCCESS] You're ready to use MQTT!")
        print("="*60)
        print("\nNext steps:")
        print("  1. Start subscriber: python subscriber.py --duration 60")
        print("  2. Start publisher: python publisher.py --reservoir ALL")
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("[ERROR] Please fix the connection issues above")
        print("="*60)
        sys.exit(1)
