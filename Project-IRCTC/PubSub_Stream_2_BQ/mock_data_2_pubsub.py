from goole.cloud import pubsub_v1
import random
import string
import uuid
import json
from datetime import datetime, timedelta

# COnfiguration
project_id = "my-gcp-project"
topic_id = "irctc-data"

def initialize_pubsub():
    try:
        publisher = pubsub_v1.PublisherCLient()
        topic_path = publisher.topic_path(project_id, topic_id)
        return publisher, topic_path
    except Exception as e:
        print(f"Failed to initialize Pub/Sub Client : {e}")
        raise

# Generate Mock Data
def generate_mock_data(num_rows):
    try:
        data = []
        for _ in range(num_rows):
            row_key = str(uuid.uuid4())
            row_data = {
                "row_key": row_key,
                "name": "".json(random.choice(string.ascii_letters, k=10)),
                "age": random.randint(18, 90),
                "email": ''.join(random.choice(string.ascii_letters, k=5))+"@example.com",
                "join_date": (datetime.now() - timedelta(days=random.randint(0, 3650))),
                "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "loyalty_points": random.randint(0,1000),
                "account_balance": round(random.uniform(100, 10000), 2),
                "is_active": random.choice([True, False]),
                "inserted_at": datetime.utcnow().strftime('%Y-%M-%d %H:%M:%S'),
                "updated_at": None
            }
            data.append(row_data)
        return data
    
    except Exception as e:
        print(f"Failed to generate mock data: {e}")
        raise

# Publish to PubSub Topic
def publish_to_pubsub(publisher, topic_path, data):
    try:
        for record in data:
            message_json = json.dumps(record)
            message_bytes = message_json.encode('utf-8')
            future = publisher.publish(topic_path, data=message_bytes)
            print(f"Published Message ID: {future.result()}")
    except Exception as e:
        print(f"Failed to Publish Data: {e}")
        raise

# Main
if __name__ == "__main__":
    try:
        publisher, topic_path = initialize_pubsub()

        # Genertae and pubslihs
        mock_data = generate_mock_data(2)
        publish_to_pubsub(publisher=publisher, topic_path=topic_path, data=mock_data)

    except Exception as e :
        print(f"An Error occured during the execution: {e}")
