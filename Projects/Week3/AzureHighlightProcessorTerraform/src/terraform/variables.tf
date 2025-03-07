variable "subscription_id" {
  description = "The Azure Subscription ID."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the Azure Resource Group."
  type        = string
}

variable "location" {
  description = "The Azure region to deploy resources."
  type        = string
  default     = "eastus2"
}

variable "storage_account_name" {
  description = "The unique name of the Storage Account. Must be 3-24 lowercase characters."
  type        = string
}

variable "container_name" {
  description = "The name of the Blob Container for storing files."
  type        = string
}

variable "environment" {
  description = "Tag for the environment (e.g., dev, test, prod)."
  type        = string
  default     = "dev"
}
