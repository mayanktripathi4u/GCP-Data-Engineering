resource "kubernetes_namespace" "mllp" {
  metadata {
    name = "mllp-adapter"
  }
}

resource "kubernetes_deployment" "mllp_adapter" {
  metadata {
    name      = "mllp-adapter"
    namespace = kubernetes_namespace.mllp.metadata[0].name
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "mllp-adapter"
      }
    }
    template {
      metadata {
        labels = {
          app = "mllp-adapter"
        }
      }
      spec {
        container {
          name  = "mllp-adapter"
          image = "gcr.io/cloud-healthcare-containers/mllp-adapter:latest"
          env {
            name  = "HL7V2_STORE"
            value = google_healthcare_hl7_v2_store.hl7v2_store.name
          }
        }
      }
    }
  }
}

resource "google_healthcare_dataset" "healthcare_dataset" {
  name     = "hl7v2-dataset"
  location = var.region
}

resource "google_healthcare_hl7_v2_store" "hl7v2_store" {
  name      = "hl7v2-store"
  dataset   = google_healthcare_dataset.healthcare_dataset.id
  hl7_v2_config {}
}
