
# Create the Cloud Function
resource "google_cloudfunctions_function" "publish_hl7_function" {
  name        = "publish_hl7"
  runtime     = "python39"
  entry_point = "publish_hl7"
  region      = "us-central1"
  
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.function_zip.name

  trigger_http = true

  environment_variables = {
    PUBSUB_TOPIC = google_pubsub_topic.hl7_topic.name
  }

  # Ensure that the function can publish to the topic
  available_memory_mb = 128

  # IAM role for the function to publish to Pub/Sub
  service_account_email = google_service_account.function_service_account.email

  # Allow the function to access Pub/Sub
  lifecycle {
    ignore_changes = [source_archive_object]
  }
}
