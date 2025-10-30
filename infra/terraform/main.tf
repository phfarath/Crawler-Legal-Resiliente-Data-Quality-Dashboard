terraform {
  required_version = ">= 1.5.0"
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_storage_bucket" "crawler_data" {
  name     = var.gcs_bucket_name
  location = var.gcp_region
}
