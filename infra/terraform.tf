provider "azurerm" {
  features {}
  tenant_id       = var.tenant_id
  subscription_id = var.subscription_id
}

# Resource Group for Cosmos DB resources
resource "azurerm_resource_group" "hvalfangst" {
  location = var.location
  name     = var.resource_group_name
}

# Cosmos DB Account
resource "azurerm_cosmosdb_account" "hvalfangst" {
  name                = var.cosmosdb_account_name   # Unique name for Cosmos DB account.
  location            = azurerm_resource_group.hvalfangst.location  # Location where the Cosmos DB account is hosted.
  resource_group_name = azurerm_resource_group.hvalfangst.name      # The resource group that Cosmos DB belongs to.

  offer_type = "Standard"  # Offer type for the Cosmos DB account. Use "Standard" for most use cases.
  # Other possible values:
  # - "Reserved": Reserved capacity offers a discounted rate in exchange for committing to a specific throughput capacity for a one- or three-year period.
  #               Suitable for predictable workloads with steady throughput requirements.


  kind      = "GlobalDocumentDB"  # Specifies the kind of database. Options include:
  # - GlobalDocumentDB (NoSQL database)
  # - MongoDB (MongoDB API)
  # - Cassandra (Cassandra API)
  # - Gremlin (Graph API)
  # - Table (Azure Table Storage API)

  automatic_failover_enabled = false  # When set to true, enables automatic failover to the secondary region in case of failure.

  # Consistency policy configuration for the Cosmos DB account.
  consistency_policy {
    consistency_level       = "BoundedStaleness"  # The consistency level applied to the database. Options include:
    # - Strong: Guarantees no data loss but has higher latency.
    # - BoundedStaleness: Allows some staleness but within defined limits.
    # - Session: Guarantees consistency within a session (user-specific consistency).
    # - ConsistentPrefix: Writes are always read in the order they're made.
    # - Eventual: Offers the lowest latency but eventual consistency.

    max_interval_in_seconds = 300  # Maximum lag (in seconds) between reads and writes in "BoundedStaleness" consistency.
    max_staleness_prefix    = 100000  # Maximum lag in terms of the number of operations in "BoundedStaleness" consistency.
  }

  geo_location {
    location          = azurerm_resource_group.hvalfangst.location  # Specifies the Azure region for Cosmos DB.
    failover_priority = 0  # Defines the priority of this region for failover (0 being the primary region).
  }
}

# SQL Database for Cosmos DB (using NoSQL API)
resource "azurerm_cosmosdb_sql_database" "hvalfangst" {
  name                = var.cosmosdb_database_name  # Name of the Cosmos DB SQL database.
  resource_group_name = azurerm_cosmosdb_account.hvalfangst.resource_group_name  # Resource group for the database.
  account_name        = azurerm_cosmosdb_account.hvalfangst.name  # Cosmos DB account to which this database belongs.
}

# SQL Container within the Cosmos DB SQL Database
resource "azurerm_cosmosdb_sql_container" "hvalfangst" {
  name                  = var.cosmosdb_container_name  # Name of the container (similar to a table).
  resource_group_name   = azurerm_cosmosdb_account.hvalfangst.resource_group_name  # Resource group for the container.
  account_name          = azurerm_cosmosdb_account.hvalfangst.name  # Cosmos DB account associated with the container.
  database_name         = azurerm_cosmosdb_sql_database.hvalfangst.name  # Name of the database that contains this container.

  partition_key_paths   = ["/id"]  # Partition key is used to distribute data across partitions for scalability.
  # Here, it's set to the "id" field. Partitioning helps in efficient query processing.

  partition_key_version = 1  # Specifies the partition key version. Default is 1.

  throughput            = 400  # Specifies the throughput (RU/s) for the container. Can be manually set or autoscale.

  # Indexing policy configuration for the container.
  indexing_policy {
    indexing_mode = "consistent"  # Options are:
    # - "consistent": Ensures that all items are indexed immediately.
    # - "lazy": Indexing is done asynchronously.
    # - "none": Indexing is disabled.

    # Define paths to include in indexing
    included_path {
      path = "/*"  # Include all paths for indexing. Can specify specific document fields as needed.
    }

    included_path {
      path = "/included/?"  # This path is also included for indexing. Can customize for specific queries.
    }

    # Define paths to exclude from indexing
    excluded_path {
      path = "/excluded/?"  # Paths that you do not want to be indexed (reduces costs for unnecessary fields).
    }
  }

  # Unique key constraints for the container.
  unique_key {
    paths = ["/idlong", "/idshort"]  # Ensures unique values for documents that have both "/idlong" and "/idshort" fields.
    # This prevents duplicates within a container.
  }
}
