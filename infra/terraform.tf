provider "azurerm" {
  features {}
  tenant_id       = var.tenant_id
  subscription_id = var.subscription_id
}

resource "azurerm_resource_group" "hvalfangst" {
  location = var.location
  name     = var.resource_group_name
}

resource "azurerm_cosmosdb_account" "hvalfangst" {
  name                = var.cosmosdb_account_name
  location            = azurerm_resource_group.hvalfangst.location
  resource_group_name = azurerm_resource_group.hvalfangst.name
  offer_type = "Standard"
  kind      = "GlobalDocumentDB"

  automatic_failover_enabled = false

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = azurerm_resource_group.hvalfangst.location
    failover_priority = 0
  }
}

# Cosmos DB SQL Database
resource "azurerm_cosmosdb_sql_database" "hvalfangst" {
  name                = var.cosmosdb_database_name
  resource_group_name = azurerm_cosmosdb_account.hvalfangst.resource_group_name
  account_name        = azurerm_cosmosdb_account.hvalfangst.name
}

# Cosmos DB SQL Container
resource "azurerm_cosmosdb_sql_container" "hvalfangst" {
  name                  = var.cosmosdb_container_name
  resource_group_name   = azurerm_cosmosdb_account.hvalfangst.resource_group_name
  account_name          = azurerm_cosmosdb_account.hvalfangst.name
  database_name         = azurerm_cosmosdb_sql_database.hvalfangst.name
  partition_key_paths   = ["/definition/id"]
  partition_key_version = 1
  throughput            = 400

  indexing_policy {
    indexing_mode = "consistent"

    included_path {
      path = "/*"
    }

    included_path {
      path = "/included/?"
    }

    excluded_path {
      path = "/excluded/?"
    }
  }

  unique_key {
    paths = ["/definition/idlong", "/definition/idshort"]
  }
}