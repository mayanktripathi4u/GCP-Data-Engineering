
# Create a Cloud Scheduler Job
resource "google_cloud_scheduler_job" "publish_hl7_job" {
  name        = "publish-hl7-job"
  description = "Trigger Cloud Function to publish HL7 messages every minute"
  schedule    = "*/1 * * * *" # Every minute
  time_zone   = "UTC"

  http_target {
    uri        = google_cloudfunctions_function.publish_hl7_function.https_trigger_url
    http_method = "POST"
    headers = {
      "Content-Type" = "application/json"
    }
  }
}