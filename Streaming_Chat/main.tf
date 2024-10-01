
#------ Terraform Provider---------#
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.27.0"
    }
  }
}

#------ Google Provider---------#
provider "google" {
  credentials = "key1.json"
  project     = var.project_id
  region      = var.region
  zone        = var.zone
}

#------ Storge Bucket and Objects---------#
resource "google_storage_bucket" "streaming_project_bucket" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = true

  lifecycle {
    prevent_destroy = false
  }

}

resource "google_storage_bucket_object" "conversations_json" {
  name   = "conversations.json"
  bucket = google_storage_bucket.streaming_project_bucket.name
  source = "conversations.json"

  lifecycle {
    prevent_destroy = false
  }

}

#------ Cloud Pub/sub for Streaming------------------------------#
resource "google_pubsub_topic" "topic" {
  name = var.topic_name
}

resource "google_pubsub_subscription" "subscription" {
  name  = var.subscription_name
  topic = google_pubsub_topic.topic.name
}

#------ Bigquery Datasets, Conversation Table, Order Table ---------#
resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = var.dataset_id
  friendly_name               = "dt_chat"
  location                    = "US"
  default_table_expiration_ms = null
  delete_contents_on_destroy = true
}

resource "google_bigquery_table" "conversations" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = var.table_conversations_name


  schema = <<EOF
[
  {
    "name": "senderAppType",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "courierId",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "fromId",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "toId",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "chatStartedByMessage",
    "type": "BOOLEAN",
    "mode": "NULLABLE"
  },
  {
    "name": "orderId",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "orderStage",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "customerId",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "messageSentTime",
    "type": "TIMESTAMP",
    "mode": "NULLABLE"
  }
]
EOF
}

resource "google_bigquery_table" "orders" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = var.table_orders_name
  lifecycle {
    prevent_destroy = false
  }

  schema = <<EOF
[
  {
    "name": "cityCode",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "orderId",
    "type": "INTEGER",
    "mode": "NULLABLE"
  }
]
EOF
}