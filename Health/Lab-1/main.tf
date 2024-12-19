provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_project_service" "enable_services" {
  for_each = toset([
    "container.googleapis.com",
    "healthcare.googleapis.com",
    "compute.googleapis.com"
  ])
  project = var.project_id
  service = each.key
}

variable "project_id" {}
variable "region" {}
