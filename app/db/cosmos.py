# app/config/cosmos.py

from azure.cosmos import CosmosClient, exceptions
from fastapi import HTTPException
from app.logger import logger  # Import logger
from app.config.cosmos import settings

# Initialize Cosmos DB Client
try:
    logger.info("Initializing Cosmos DB client...")
    logger.info(f"Connection string: {settings.COSMOS_CONNECTION_STRING}")

    client = CosmosClient.from_connection_string(settings.COSMOS_CONNECTION_STRING)
    database = client.get_database_client(settings.DATABASE_NAME)
    container = database.get_container_client(settings.CONTAINER_NAME)
    logger.info(f"Successfully connected to Cosmos DB: {settings.DATABASE_NAME}, container: {settings.CONTAINER_NAME}")
except ValueError as e:
    logger.error(f"ValueError during Cosmos DB initialization: {e}")
    raise HTTPException(status_code=400, detail=str(e))
except exceptions.CosmosHttpResponseError as e:
    logger.error(f"CosmosHttpResponseError: {e.message} (Status code: {e.status_code})")
    raise HTTPException(status_code=e.status_code, detail=str(e))
except Exception as e:
    logger.critical(f"Unexpected error during Cosmos DB initialization: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail="Internal Server Error")
