provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  type = string
  default = "gcphde-prim-dev-data"
}

variable "region" {
  type = string
  default = "us-central1"
}


resource "google_pubsub_topic" "data_topic" {
  name = "data-topic"
}

resource "google_pubsub_subscription" "data_subscription" {
  name  = "data-subscription"
  topic = google_pubsub_topic.data_topic.name
}

resource "google_bigquery_dataset" "data_dataset" {
  dataset_id = "my_dataset"
  location   = var.region
}

resource "google_bigquery_table" "data_table" {
  dataset_id = google_bigquery_dataset.data_dataset.dataset_id
  table_id   = "processed_data"
  schema     = jsonencode([
    {
      name = "status"
      type = "STRING"
    },
    {
      name = "other_field"
      type = "STRING"
    }
  ])
}

resource "google_dataflow_job" "dataflow_job" {
  name               = "dataflow-etl-job"
  template           = "gs://dataflow-templates/latest/Stream_Streaming_Data"
  temp_gcs_location  = "gs://your-bucket-name/temp/"  # Update this to your GCS bucket for temp files

  parameters = {
    "inputTopic"      = google_pubsub_topic.data_topic.id
    "outputTable"     = "${google_bigquery_dataset.data_dataset.dataset_id}.${google_bigquery_table.data_table.table_id}"
    "project"         = var.project_id
    "gcs_location"    = "gs://your-bucket-name/dataflow_transform.py"  # Path to your Python file in GCS
    "workerMachineType" = "n1-standard-1"  # Optional: Specify the machine type for Dataflow workers
  }
}

