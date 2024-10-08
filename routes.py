from fastapi import APIRouter, HTTPException
from azure.cosmos import CosmosClient, exceptions
from pydantic import BaseModel
from typing import List, Optional

# Create a FastAPI router
router = APIRouter()

# Initialize Cosmos DB Client using a connection string
COSMOS_CONNECTION_STRING = "KELLERESSEN70"
DATABASE_NAME = "KELLERESSEN70"
CONTAINER_NAME = "KELLERESSEN70"

# Placeholder validation function
def validate_cosmosdb_config():
    placeholder_value = "KELLERESSEN70"
    if COSMOS_CONNECTION_STRING == placeholder_value:
        raise ValueError("Invalid Cosmos DB connection string. Please set the correct value.")
    if DATABASE_NAME == placeholder_value:
        raise ValueError("Invalid Cosmos DB database name. Please set the correct value.")
    if CONTAINER_NAME == placeholder_value:
        raise ValueError("Invalid Cosmos DB container name. Please set the correct value.")

# Validate configuration before proceeding
validate_cosmosdb_config()

try:
    # Initialize Cosmos DB client
    client = CosmosClient.from_connection_string(COSMOS_CONNECTION_STRING)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except exceptions.CosmosHttpResponseError as e:
    raise HTTPException(status_code=e.status_code, detail=str(e))

# Definition can be optional if not always present
class Definition(BaseModel):
    id: Optional[str] = None

class Item(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    definition: Optional[Definition] = None

@router.post("/items/", response_model=Item)
async def create_item(item: Item):
    try:
        container.upsert_item(item.model_dump())
        return item
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    try:
        item = container.read_item(item_id, partition_key=item_id)
        return item
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")

@router.get("/items/", response_model=List[Item])
async def read_items():
    items = list(container.read_all_items())
    return items

@router.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    try:
        container.delete_item(item_id, partition_key=item_id)
        return {"message": f"Item with id '{item_id}' deleted successfully"}
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")
