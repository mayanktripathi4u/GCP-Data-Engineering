resource "google_pubsub_topic" "demp-topic" {
  name = "demo-topic"
}

resource "google_pubsub_subscription" "demp_subscription" {
    name = "demo-subscription"
    topic = google_pubsub_topic.demp-topic
}  

resource "google_cloud_scheduler_job" "data-job" {
  name = "demo-job"
  schedule = "* * * * *"
  time_zone = "Asian/Kolkata"

  pubsub_target {
    topic_name = google_pubsub_topic.demp-topic
    data = base64encode("Message from Job")
  }
}