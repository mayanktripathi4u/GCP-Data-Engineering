# Write to Pub/Sub Topic using Python
To send messages to a Google Cloud Pub/Sub topic using Python, you can use the google-cloud-pubsub library. This library provides a client for interacting with Google Cloud Pub/Sub services.

## Steps to Send Messages to Pub/Sub Topic
1. Set Up Google Cloud Project:
   * Ensure you have a Google Cloud project with Pub/Sub API enabled.
   * Create a Pub/Sub topic if you haven't already.
2. Install the Google Cloud Pub/Sub Client Library:
   * Install the google-cloud-pubsub package via pip:
   ```
   pip install google-cloud-pubsub
   ```
3. Authenticate Your Application:
Make sure your Google Cloud credentials are set up. You can use a service account key file. Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your service account key file.
    ```
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
    ```
4. Write Python Code to Send Messages:
Here’s a sample Python script to send messages to a Pub/Sub topic:
```
from google.cloud import pubsub_v1

# Replace these variables with your project and topic names
project_id = 'your-project-id'
topic_id = 'your-topic-id'

# Initialize a Publisher client
publisher = pubsub_v1.PublisherClient()

# Construct the fully qualified topic path
topic_path = publisher.topic_path(project_id, topic_id)

def publish_message(message: str):
    # Encode the message as bytes
    data = message.encode('utf-8')

    # Publish the message to the topic
    future = publisher.publish(topic_path, data=data)
    print(f'Published message ID: {future.result()}')

if __name__ == '__main__':
    # Example message
    message = 'Hello, Pub/Sub!'
    publish_message(message)

```
5. Additional Information
    * Error Handling: You might want to add error handling to manage exceptions, such as network issues or invalid credentials.
    * Asynchronous Publishing: The publish() method is asynchronous. You can use future.result() to block until the message is acknowledged, or handle the future asynchronously.

## Complete Example
Here's a complete example script: [publish_messages.py](/GCP-Data-Engineering/Pub-Sub-Python/publish_messages.py)


# Python Script to Send Fake Messages every X minute (Scheduled)
Here's a complete Python script that generates fake data and sends it to a Pub/Sub topic every minute: [scheule_messages.py](/GCP-Data-Engineering/Pub-Sub-Python/schedule_messages.py)

## Explanation
1. Imports:
* `time`, `json`, and `datetime` for handling time, data formatting, and fake data generation.
* `schedule` for scheduling the task.
* `Faker` for generating fake data.
* `pubsub_v1` from `google.cloud` for interacting with Google Cloud Pub/Sub.
2. Initialize Clients and Faker:
* `fake` is an instance of `Faker` to generate fake data.
    * publisher is a PublisherClient instance for sending messages to Pub/Sub.
3. Generate Fake Data:
* `generate_fake_message()` creates a dictionary with fake data.
* `publish_message()` converts the dictionary to JSON, encodes it as bytes, and publishes it to the Pub/Sub topic.
4. Scheduling:
* `schedule.every(1).minute.do(publish_message)` schedules the `publish_message` function to run every minute.
  * `while True` loop keeps the script running and executes pending scheduled tasks.
5. Main Function:
* The `main()` function starts the scheduling and keeps the script running indefinitely.

## Running the Script
* Ensure Authentication: Make sure you have authenticated your Google Cloud environment. Set the **GOOGLE_APPLICATION_CREDENTIALS** environment variable to your service account key file path.
* Run the Script: Execute the script in your Python environment. The script will continuously send fake messages to your Pub/Sub topic every minute.
```
python your_script_name.py
```

This script will generate and publish a message with fake data to the specified Pub/Sub topic every minute, and it will keep running until manually stopped.

