terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.36.0"
    }
  }
}

provider "google" {
  # Config options
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region

}


resource "google_storage_bucket" "terraform-demo-bucket" {
  name          = var.gcp_storage_name
  location      = var.location
  force_destroy = true
  storage_class = var.gcp_storage_class
  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}