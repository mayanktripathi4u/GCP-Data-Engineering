import logging
import base64

def pubsub_trigger(event, context):
    """Triggered from a message on a Pub/Sub topic.
    Args:
        event (dict): The dictionary with data from Pub/Sub.
        context (google.cloud.functions.Context): The context object for the event.
    """
    # Get the message data
    if 'data' in event:
        # Decode the Pub/Sub message
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    else:
        pubsub_message = 'No data found in the event.'

    # Log the message
    logging.info(f"Received message: {pubsub_message}")

    # Here you can add processing logic for the message
    # For example, you can parse it, store it in a database, etc.

    # Log that processing is complete
    logging.info("Message processing completed.")
