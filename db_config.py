"""
Database Configuration - MongoDB Atlas
Supports both local JSON files (development) and MongoDB (production)
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime

# Database mode: 'mongodb' or 'json'
DB_MODE = os.environ.get('DB_MODE', 'json')

# MongoDB connection string from environment variable
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb+srv://reservoir_admin:zfUFiqhZgD48NO8W@reservoir-monitoring.lmdpkq6.mongodb.net/?retryWrites=true&w=majority&appName=reservoir-monitoring')

# Database and collection names
DATABASE_NAME = 'reservoir_monitoring'
COLLECTION_NAME = 'daily_reports'


class DatabaseManager:
    """Manages database operations for both MongoDB and JSON"""

    def __init__(self):
        self.mode = DB_MODE
        self.client = None
        self.db = None
        self.collection = None

        if self.mode == 'mongodb' and MONGODB_URI:
            try:
                self.client = MongoClient(
                    MONGODB_URI,
                    serverSelectionTimeoutMS=30000,
                    connectTimeoutMS=30000,
                    socketTimeoutMS=30000,
                    retryWrites=True,
                    w='majority'
                )
                # Test connection
                self.client.admin.command('ping')
                self.db = self.client[DATABASE_NAME]
                self.collection = self.db[COLLECTION_NAME]
                print(f"[MongoDB] Connected to database: {DATABASE_NAME}")
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                print(f"[MongoDB] Connection failed: {e}")
                print("[MongoDB] Falling back to JSON mode")
                self.mode = 'json'
        else:
            print(f"[DB] Using {self.mode.upper()} mode")

    def save_daily_report(self, report_data):
        """
        Save daily report data

        Args:
            report_data: List of daily records or single record
        """
        if self.mode == 'mongodb':
            return self._save_to_mongodb(report_data)
        else:
            return self._save_to_json(report_data)

    def get_all_reports(self):
        """
        Get all daily reports

        Returns:
            List of daily records
        """
        if self.mode == 'mongodb':
            return self._get_from_mongodb()
        else:
            return self._get_from_json()

    def _save_to_mongodb(self, report_data):
        """Save data to MongoDB"""
        try:
            if isinstance(report_data, list):
                # Batch insert/update
                operations = []
                for record in report_data:
                    # Add metadata
                    record['updated_at'] = datetime.utcnow()
                    record['_id'] = record.get('date')  # Use date as unique ID

                    # Upsert (update if exists, insert if not)
                    operations.append({
                        'replaceOne': {
                            'filter': {'_id': record['_id']},
                            'replacement': record,
                            'upsert': True
                        }
                    })

                if operations:
                    result = self.collection.bulk_write(operations)
                    print(f"[MongoDB] Saved {len(report_data)} records")
                    print(f"  - Inserted: {result.upserted_count}")
                    print(f"  - Modified: {result.modified_count}")
                    return True
            else:
                # Single record
                report_data['updated_at'] = datetime.utcnow()
                report_data['_id'] = report_data.get('date')

                result = self.collection.replace_one(
                    {'_id': report_data['_id']},
                    report_data,
                    upsert=True
                )
                print(f"[MongoDB] Saved record for {report_data.get('date')}")
                return True

        except Exception as e:
            print(f"[MongoDB] Error saving data: {e}")
            return False

    def _get_from_mongodb(self):
        """Get data from MongoDB"""
        try:
            # Get all records, sorted by date
            cursor = self.collection.find({}).sort('_id', 1)
            records = list(cursor)

            # Remove MongoDB _id from output (keep date field)
            for record in records:
                if '_id' in record and 'date' not in record:
                    record['date'] = record['_id']

            print(f"[MongoDB] Retrieved {len(records)} records")
            return records

        except Exception as e:
            print(f"[MongoDB] Error retrieving data: {e}")
            return []

    def _save_to_json(self, report_data):
        """Save data to JSON file (fallback/local dev)"""
        from pathlib import Path
        import json

        reports_dir = Path(__file__).parent / 'reports'
        reports_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = reports_dir / f'comprehensive_report_{timestamp}.json'

        with open(json_file, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"[JSON] Saved to: {json_file.name}")
        return True

    def _get_from_json(self):
        """Get data from latest JSON file (fallback/local dev)"""
        from pathlib import Path
        import json

        reports_dir = Path(__file__).parent / 'reports'

        if not reports_dir.exists():
            return []

        json_files = sorted(reports_dir.glob('comprehensive_report_*.json'))

        if not json_files:
            return []

        latest_file = json_files[-1]

        try:
            with open(latest_file, 'r') as f:
                data = json.load(f)
            print(f"[JSON] Loaded from: {latest_file.name}")
            return data
        except Exception as e:
            print(f"[JSON] Error loading file: {e}")
            return []

    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("[MongoDB] Connection closed")


def test_connection():
    """Test database connection"""
    print("\n" + "="*60)
    print("DATABASE CONNECTION TEST")
    print("="*60)

    db = DatabaseManager()

    if db.mode == 'mongodb':
        print("[SUCCESS] MongoDB connection established!")
        print(f"  Database: {DATABASE_NAME}")
        print(f"  Collection: {COLLECTION_NAME}")
    else:
        print("[INFO] Using JSON file mode")

    print("="*60 + "\n")

    return db


if __name__ == "__main__":
    # Test the connection
    db = test_connection()
    db.close()
