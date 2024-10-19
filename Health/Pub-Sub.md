# Google Cloud Pub/Sub 


# Schema in Pub/Sub
In a pub/sub (publish/subscribe) messaging system, a schema defines the structure of the messages that are being sent and received. It specifies the format and types of data within a message, ensuring that both publishers and subscribers understand the content being exchanged. Using schemas helps maintain data integrity and enables validation of messages.

**Example: Using a Schema in a Pub/Sub System**
Let’s consider a simple example using a JSON schema for a pub/sub system where we publish messages related to user activities in an application. We'll use a hypothetical messaging library to illustrate this.

1. Define the Schema
We can define a JSON schema for user activity messages as follows:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "userId": {
      "type": "string"
    },
    "action": {
      "type": "string",
      "enum": ["login", "logout", "signup", "updateProfile"]
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    }
  },
  "required": ["userId", "action", "timestamp"]
}
```

This schema specifies that a valid user activity message must include:

userId: a string representing the user's identifier.
action: a string that must be one of the predefined actions.
timestamp: a string formatted as a date-time.

2. Publish a Message
Here’s an example of publishing a message that adheres to the defined schema:
```python
import json
import time
from datetime import datetime
from your_pubsub_library import PubSubClient

# Initialize Pub/Sub client
pubsub_client = PubSubClient()

# Message to publish
user_activity_message = {
    "userId": "user123",
    "action": "login",
    "timestamp": datetime.now().isoformat()
}

# Publish the message
pubsub_client.publish("user_activity_topic", json.dumps(user_activity_message))
```

3. Subscribe to Messages
Subscribers will receive messages and validate them against the schema:

```python
from jsonschema import validate, ValidationError

# Define the schema as a Python object
user_activity_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "userId": {"type": "string"},
        "action": {
            "type": "string",
            "enum": ["login", "logout", "signup", "updateProfile"]
        },
        "timestamp": {"type": "string", "format": "date-time"}
    },
    "required": ["userId", "action", "timestamp"]
}

def message_handler(message):
    try:
        # Validate the message against the schema
        message_data = json.loads(message)
        validate(instance=message_data, schema=user_activity_schema)
        print("Valid message received:", message_data)
    except ValidationError as e:
        print("Invalid message:", e.message)

# Subscribe to the topic
pubsub_client.subscribe("user_activity_topic", message_handler)
```

# Attach the Schema to Existing Pub/Sub Topic
Attaching a schema to an existing Pub/Sub topic can be done using both Terraform and the gcloud command-line tool. Here’s how you can do it with both methods.

## Using Terraform
To attach a schema to an existing Pub/Sub topic using Terraform, you will need to define the schema and associate it with the topic. Here’s an example:

1. Define the Schema:
```bash
resource "google_pubsub_schema" "user_activity_schema" {
  name        = "user_activity_schema"
  type        = "AVRO"  # or "PROTOCOL_BUFFER", depending on your needs
  definition  = <<EOF
{
  "type": "record",
  "name": "UserActivity",
  "fields": [
    {"name": "userId", "type": "string"},
    {"name": "action", "type": "string"},
    {"name": "timestamp", "type": "string"}
  ]
}
EOF
}
```

2. Attach Schema to Existing Topic:
Assuming you already have a Pub/Sub topic named my_existing_topic, you can attach the schema like this:
```bash
resource "google_pubsub_topic" "my_existing_topic" {
  name = "my_existing_topic"

  schema = google_pubsub_schema.user_activity_schema.id
}
```

Complete code will look like
```bash
provider "google" {
  project = "your-project-id"
  region  = "us-central1"
}

resource "google_pubsub_schema" "user_activity_schema" {
  name       = "user_activity_schema"
  type       = "AVRO"
  definition = <<EOF
{
  "type": "record",
  "name": "UserActivity",
  "fields": [
    {"name": "userId", "type": "string"},
    {"name": "action", "type": "string"},
    {"name": "timestamp", "type": "string"}
  ]
}
EOF
}

resource "google_pubsub_topic" "my_existing_topic" {
  name   = "my_existing_topic"
  schema = google_pubsub_schema.user_activity_schema.id
}
```

## Using gcloud Command
You can also attach a schema to an existing Pub/Sub topic using the gcloud command-line tool. Here’s how:

1. Create the Schema:
First, create the schema using the following command:
```bash
gcloud pubsub schemas create user_activity_schema \
  --type=AVRO \
  --definition='{
    "type": "record",
    "name": "UserActivity",
    "fields": [
      {"name": "userId", "type": "string"},
      {"name": "action", "type": "string"},
      {"name": "timestamp", "type": "string"}
    ]
  }'
```

2. Attach the Schema to an Existing Topic:
Now, you can attach the schema to your existing topic using this command:

```bash
gcloud pubsub topics update my_existing_topic \
  --schema=user_activity_schema
```



