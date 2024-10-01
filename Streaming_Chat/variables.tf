variable "project_id" {
  description = "The ID of the Google Cloud project"
  type        = string
  default     = "projecta-418002"
}

variable "region" {
  description = "The region for the resources"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "The zone for the resources"
  type        = string
  default     = "us-central1-a"
}

variable "bucket_name" {
  description = "The name of the GCS bucket"
  type        = string
  default     = "my-bucket-etl-1987"
}

variable "topic_name" {
  description = "The name of the Pub/Sub topic"
  type        = string
  default     = "topic-conversation"
}

variable "subscription_name" {
  description = "The name of the Pub/Sub subscription"
  type        = string
  default     = "submessages"
}

variable "dataset_id" {
  description = "The ID of the BigQuery dataset"
  type        = string
  default     = "myetldataset"
}

variable "table_conversations_name" {
  description = "The name of the BigQuery conversations table"
  type        = string
  default     = "conversations"
}

variable "table_orders_name" {
  description = "The name of the BigQuery orders table"
  type        = string
  default     = "orders"
}