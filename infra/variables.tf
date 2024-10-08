
# - - - - - - - - - - - - - SENSITIVE - - - - - - - - - - - - -

# The below variables have to be overridden in a "terraform.tfvars" file, which should NEVER be committed to SCM.

variable "tenant_id" {
  description = "The Tenant ID of the Azure AD where the Service Principal resides"
  type        = string
}

variable "subscription_id" {
  description = "The Subscription ID to deploy Azure resources"
  type        = string
}

# - - - - - - - - - - - - - NON-SENSITIVE - - - - - - - - - - - - -

# Generic variables related to location, resource groups and metadata for requested resources - such as cosmos db account, database and container

variable "location" {
  description = "The Azure region where resources will be created"
  type        = string
  default     = "Norway East"  # Replace/override this as you see fit
}

variable "resource_group_name" {
  description = "The name of the Azure Resource Group"
  type        = string
  default     = "hvalfangstresourcegroup"  # Replace/override this as you see fit
}

variable "cosmosdb_account_name" {
  description = "The name of the Cosmos DB account"
  type        = string
  default     = "hvalfangstcosmosdb"  # Replace/override this as you see fit
}

variable "cosmosdb_database_name" {
  description = "The name of the Cosmos DB database"
  type        = string
  default     = "hvalfangstdb"  # Replace/override this as you see fit
}

variable "cosmosdb_container_name" {
  description = "The name of the Cosmos DB container"
  type        = string
  default     = "hvalfangstcontainer"  # Replace/override this as you see fit
}