
# Output the Pub/Sub topic and Cloud Function URL
output "pubsub_topic" {
  value = google_pubsub_topic.hl7_topic.name
}

output "cloud_function_url" {
  value = google_cloudfunctions_function.publish_hl7_function.https_trigger_url
}
