"""
MQTT Configuration - Supports both local and cloud MQTT brokers
"""
import os

# Environment: 'local' or 'cloud'
MQTT_ENV = os.environ.get('MQTT_ENV', 'local')

# Local MQTT Configuration (Mosquitto on your machine)
LOCAL_CONFIG = {
    'broker': 'localhost',
    'port': 1883,
    'username': None,
    'password': None,
    'use_tls': False
}

# Cloud MQTT Configuration (HiveMQ Cloud)
# IMPORTANT: Set these in environment variables - no defaults for security
CLOUD_CONFIG = {
    'broker': os.environ.get('MQTT_CLOUD_BROKER', None),  # Must be set via environment variable
    'port': int(os.environ.get('MQTT_CLOUD_PORT', '8883')),
    'username': os.environ.get('MQTT_CLOUD_USER', None),  # Must be set via environment variable
    'password': os.environ.get('MQTT_CLOUD_PASS', None),  # Must be set via environment variable
    'use_tls': True
}

# Select configuration based on environment
if MQTT_ENV == 'cloud':
    MQTT_CONFIG = CLOUD_CONFIG
    print(f"[CLOUD] Using CLOUD MQTT: {CLOUD_CONFIG['broker']}")
else:
    MQTT_CONFIG = LOCAL_CONFIG
    print(f"[LOCAL] Using LOCAL MQTT: {LOCAL_CONFIG['broker']}")

# Common MQTT settings
QOS = 1
TIMEOUT = 60


def get_mqtt_config():
    """Get the current MQTT configuration"""
    return MQTT_CONFIG.copy()


def print_config():
    """Print current MQTT configuration (without password)"""
    config = get_mqtt_config()
    safe_config = {k: v for k, v in config.items() if k != 'password'}
    if config.get('password'):
        safe_config['password'] = '***'

    print("\n" + "="*50)
    print(f"MQTT Configuration ({MQTT_ENV.upper()})")
    print("="*50)
    for key, value in safe_config.items():
        print(f"  {key:12} : {value}")
    print("="*50 + "\n")
