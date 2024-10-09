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

  # Consistency policy configuration for the Cosmos DB account.
  # Bounded Staleness consistency is selected here, which offers a balance between strong consistency and higher availability.
  # It allows some staleness but within defined limits of time (in seconds) or operation count (staleness prefix).
  consistency_policy {
    consistency_level       = "BoundedStaleness"  # Consistency level set to "BoundedStaleness"
    max_interval_in_seconds = 300  # Reads can lag behind writes by up to 300 seconds (5 minutes).
    max_staleness_prefix    = 100000  # Reads can lag by up to 100,000 operations.

    # Other possible consistency levels and their descriptions:

    # 1. Strong Consistency:
    # consistency_level = "Strong"
    # Example: All reads return the most recent committed write, ensuring no stale data. Suitable for mission-critical applications where data must always be up to date (e.g., banking transactions).

    # 2. Session Consistency:
    # consistency_level = "Session"
    # Example: Ensures consistency within a user session, so a user will always read their own writes (read-your-writes). Suitable for scenarios like shopping carts or user-specific data (e.g., cloud document editing).

    # 3. Consistent Prefix:
    # consistency_level = "ConsistentPrefix"
    # Example: Guarantees that writes are seen in order, but data may be stale. If updates A → B → C are made, a read will never show C → A or B → A, but may show A → B or A. Suitable for scenarios where ordering is important, but up-to-date information is less critical (e.g., activity logs).

    # 4. Eventual Consistency:
    # consistency_level = "Eventual"
    # Example: Provides the lowest latency but no guarantees on order or staleness. Suitable for scenarios where high performance is required and consistency can be relaxed (e.g., social media feed updates).
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
  partition_key_paths   = ["/id"]
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
    paths = ["/idlong", "/idshort"]
  }
}