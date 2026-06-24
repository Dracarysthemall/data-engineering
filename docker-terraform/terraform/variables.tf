variable "credentials" {
  description = "service account credential "
  default     = "./keys/service_account_key.json"

}


variable "project" {
  description = "Project name"
  default     = "terraform-project-499512"
}




variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "region" {
  description = "Project Region"
  default     = "europe-west9"
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcp_storage_name" {
  description = "name for google cloud storage bucket"
  default     = "terraform-project-499512-demo-bucket"
}

variable "gcp_storage_class" {
  description = "class for google cloud storage bucket"
  default     = "STANDARD"
}