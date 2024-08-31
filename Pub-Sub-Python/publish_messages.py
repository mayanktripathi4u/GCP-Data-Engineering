from google.cloud import pubsub_v1

def publish_message(project_id: str, topic_id: str, message: str):
    # Initialize a Publisher client
    publisher = pubsub_v1.PublisherClient()

    # Construct the fully qualified topic path
    topic_path = publisher.topic_path(project_id, topic_id)

    # Encode the message as bytes
    data = message.encode('utf-8')

    # Publish the message to the topic
    future = publisher.publish(topic_path, data=data)
    print(f'Published message ID: {future.result()}')

if __name__ == '__main__':
    # Replace with your project and topic names
    project_id = 'your-project-id'
    topic_id = 'your-topic-id'
    
    # Example message
    message = 'Hello, Pub/Sub!'
    publish_message(project_id, topic_id, message)
