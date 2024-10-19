import os
import random
import base64
from google.cloud import pubsub_v1
from flask import escape

def publish_hl7(request):
    project_id = os.environ["GCP_PROJECT"]
    topic_id = os.environ["PUBSUB_TOPIC"]

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Generate random number of messages (between 4 and 10)
    num_messages = random.randint(4, 10)

    for _ in range(num_messages):
        # Generate a fake HL7v2 message
        hl7_message = "MSH|^~\\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|202310111200||ORM^O01|123456|P|2.3"
        
        # Encode the message to bytes
        message_bytes = hl7_message.encode("utf-8")
        
        # Publish the message
        future = publisher.publish(topic_path, message_bytes)
        print(f"Published message ID: {future.result()}")

    return "Messages published.", 200
