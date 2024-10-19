variable "project_id" {
  type = string
  default = "gcphde-prim-dev-data"
  description = "Project ID"
}

variable "region" {
  type = string
  default = "us-central1"
  description = "Default Region"
}

variable "deploy_cf_flag" {
  type = bool
  default = false
  description = "Feature Flag for Cloud Function to Deploy in a Project or not."
}