output "resource_group_name" {
  description = "The name of the resource group created."
  value       = azurerm_resource_group.rg.name
}

output "storage_account_name" {
  description = "The name of the storage account created."
  value       = azurerm_storage_account.storage.name
}

output "storage_account_primary_key" {
  description = "The primary access key for the storage account."
  value       = azurerm_storage_account.storage.primary_access_key
  sensitive   = true
}

output "container_name" {
  description = "The name of the blob container created."
  value       = azurerm_storage_container.container.name
}
