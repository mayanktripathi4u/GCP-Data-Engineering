# Create Pub/Sub Schema
resource "google_pubsub_schema" "hl7_schema" {
  name     = "hl7_schema"
  type     = "AVRO"
  definition = file("HL7v2-Pub-Sub-Schema.json")
}

# Create a Pub/Sub Topic
resource "google_pubsub_topic" "hl7_topic" {
  name = "hl7-topic"
  depends_on = [google_pubsub_schema.hl7_schema]
  schema_settings {
    schema = "projects/my-project-name/schemas/hl7_schema"
    encoding = "JSON"
  }
  # schema = google_pubsub_schema.hl7_schema
}

resource "google_pubsub_topic_iam_member" "function_pubsub_invoker" {
  topic = google_pubsub_topic.hl7_topic.name
  role  = "roles/pubsub.publisher"
  member = "serviceAccount:${google_service_account.function_service_account.email}"
}