terraform {
  required_providers {
    google  = {
        source = "hashicorp/google"
        version = "5.18.0"
    }
  }
}

provider "google" {
    project = "my-project-1234a"
    region = "us-central"
    credentials = file("keys.json")

    
  
}