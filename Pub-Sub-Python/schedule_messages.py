import time
import json
import schedule
from google.cloud import pubsub_v1
from faker import Faker
from datetime import datetime

# Initialize Faker and Pub/Sub client
fake = Faker()
publisher = pubsub_v1.PublisherClient()

# Replace these variables with your project and topic names
project_id = 'your-project-id'
topic_id = 'your-topic-id'
topic_path = publisher.topic_path(project_id, topic_id)

def generate_fake_message():
    # Generate fake data
    message = {
        "Name": fake.name(),
        "Age": fake.random_int(min=18, max=80),
        "Steps Walked": fake.random_number(digits=5),
        "Temperature": fake.random_number(digits=2),
        "Current Date-Time": datetime.now().isoformat(),
        "City": fake.city(),
        "Humidity": fake.random_number(digits=2)
    }
    
    return message

def publish_message():
    # Generate the fake message
    message = generate_fake_message()
    
    # Convert the message to JSON and encode to bytes
    message_json = json.dumps(message)
    data = message_json.encode('utf-8')
    
    # Publish the message to the Pub/Sub topic
    future = publisher.publish(topic_path, data=data)
    print(f'Published message ID: {future.result()}')

def main():
    # Schedule the task to run every minute
    schedule.every(1).minute.do(publish_message)
    
    print("Starting to send messages every minute...")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
