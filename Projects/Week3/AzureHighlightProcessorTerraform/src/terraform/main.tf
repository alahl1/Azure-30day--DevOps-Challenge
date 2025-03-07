provider "azurerm" {
  features {}
  subscription_id = var.subscription_id  # Pass subscription ID from variables.tf
}

# Create the Resource Group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# Create the Storage Account
resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  
  tags = {
    environment = var.environment
  }
}

# Create the Blob Container using the storage_account_id attribute
resource "azurerm_storage_container" "container" {
  name                  = var.container_name
  storage_account_id    = azurerm_storage_account.storage.id  # Use storage_account_id instead of deprecated storage_account_name
  container_access_type = "private"
}
