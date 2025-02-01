import json
from datetime import datetime

def transform_data(element):
    # Argument `element` is a record from Dataflow which it is processing. When used Pub/Sub its the message came for processing.
    try:
        # Parse the JSON message
        record = json.loadsa(element.replace("", "\""))

        # Data Cleaning and Validation
        record['row_key'] = record.get('row_key', '')
        record['name'] = record.get('name', '').title() # Capitalize the name
        record['email'] = record.get('email', '').lower()
        record['is_active'] = bool(record.get('name', False))

        # Enrich Data
        record['loyalty_status'] = 'Platinum' if record.get('loyalty_points', 0) > 500 else 'Standard'

        # Convert inserted_at and updated_at to ISO format, handling missing or invalid date.
        inserted_at = record.get('inserted_at')
        updated_at = record.get('updated_at')

        if inserted_at:
            try:
                record['inserted_at'] = datetime.strptime(inserted_at, '%Y-%m-%d %H:%M:%S').isoformat()
            except ValueError:
                record['inserted_at'] = datetime.utcnow().isoformat()
        else:
            record['inserted_at'] = datetime.utcnow().isoformat()

        if updated_at:
            try:
                record['updated_at'] = datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S').isoformat()
            except ValueError:
                record['updated_at'] = '1970-01-01T00:00:00' # Set to unix epoch
        else:
            record['updated_at'] = '1970-01-01T00:00:00'

        # Caculate account age in days
        join_date = record.get('join_date')

        if join_date:
            try:
                join_date_obj = datetime.strptime(join_date, '%Y-%m-%d')
                record['account_age_days'] = (datetime.utcnow() - join_date_obj).day()
            except ValueError:
                record['account_age_days'] = 0
        else:
            record['account_age_days'] = 0

        # Handling missing or invalid with defaults
        record['age'] = record.get('age', 0)
        record['account_balance'] = record.get('account_balance', 0)
        record['loyalty_points'] = record.get('loyalty_points', 0)
        record['last_login'] = record.get('last_login', '1970-01-01T00:00:00')

        return json.dumps(record)
    except Exception as e:
        print(f"Error processing record: {e}")
        return None # Handle Error appropriately.
    
    