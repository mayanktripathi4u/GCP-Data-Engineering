To create a simple Google Cloud Function that gets triggered by a Pub/Sub topic and processes the incoming message while logging its activity, you'll need to follow these steps:

1. Create a Pub/Sub Topic.
2. Write the Cloud Function.
3. Deploy the Cloud Function.

# Step 1: Create a Pub/Sub Topic
You can create a Pub/Sub topic using the gcloud command-line tool. Here’s how:
```bash
gcloud pubsub topics create enrollment-topic
```

# Step 2: Write the Cloud Function
Create a file named `main.py` with the [code](/GCP-Data-Engineering/ETL-Project-2/src/main.py).

# Step 3: Create a requirements.txt File
Create a `requirements.txt` file to specify any dependencies for your Cloud Function. Since this example only uses the standard `logging` library, you can leave it empty or specify your function's dependencies if you have any.

# Step 4: Deploy the Cloud Function
Use the `gcloud` command to deploy the function, linking it to the Pub/Sub topic created earlier:
```bash
# Deploy the function
gcloud functions deploy pubsub_trigger \
    --runtime python39 \
    --trigger-topic enrollment-topic \
    --entry-point pubsub_trigger \
    --region us-central1 \
    --set-env-vars LOG_LEVEL=INFO \
    --source src
```
Make sure you're running this command from the directory that contains the src folder.
```bash
ETL-Project-2/
│
├── src/
│   ├── main.py
│   └── requirements.txt
└── (other files if necessary)
```

# Step 5: Publish Messages to the Pub/Sub Topic
You can publish messages to the Pub/Sub topic using the gcloud command:
```bash
# Publish a message to the topic
gcloud pubsub topics publish enrollment-topic --message "Hello, this is a test message."
```

# Step 6: Viewing Logs
After deploying your Cloud Function and publishing messages, you can view the logs in the Google Cloud Console under `Logging > Logs Explorer`, or you can use the gcloud command:
```bash
gcloud functions logs read pubsub_trigger
```
