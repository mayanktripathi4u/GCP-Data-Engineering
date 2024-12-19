resource "google_container_cluster" "gke_cluster" {
  name               = "hl7v2-gke-cluster"
  location           = var.region
  initial_node_count = 1
  node_config {
    machine_type = "e2-medium"
  }
}

resource "google_container_node_pool" "default_pool" {
  cluster    = google_container_cluster.gke_cluster.name
  location   = var.region
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = "e2-medium"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}
