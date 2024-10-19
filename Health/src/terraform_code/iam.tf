
# Create a Service Account for Cloud Function
resource "google_service_account" "function_service_account" {
  account_id   = "function-service-account"
  display_name = "Function Service Account"
}