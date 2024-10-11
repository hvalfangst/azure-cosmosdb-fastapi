# app/routers/heroes.py

from fastapi import APIRouter, HTTPException
from typing import List
from azure.cosmos import exceptions
from app.models.dnd_hero import DnDHero
from app.db.cosmos import container
from app.logger import logger

router = APIRouter()


# POST: Create a new Hero
@router.post("/heroes/", response_model=DnDHero)
async def create_hero(hero: DnDHero):
    try:
        logger.info(f"Attempting to create a new hero: {hero.name}")
        container.upsert_item(hero.dict())
        logger.info(f"Hero '{hero.name}' created successfully.")
        return hero
    except exceptions.CosmosHttpResponseError as e:
        logger.error(f"Error creating hero '{hero.name}': {e}")
        raise HTTPException(status_code=e.status_code, detail=str(e))


# GET: Retrieve a hero by ID
@router.get("/heroes/{hero_id}", response_model=DnDHero)
async def read_hero(hero_id: str):
    try:
        logger.info(f"Fetching hero with ID: {hero_id}")
        hero = container.read_item(hero_id, partition_key=hero_id)
        logger.info(f"Hero '{hero_id}' retrieved successfully.")
        return hero
    except exceptions.CosmosResourceNotFoundError:
        logger.warning(f"Hero with ID '{hero_id}' not found.")
        raise HTTPException(status_code=404, detail="Hero not found")
    except exceptions.CosmosHttpResponseError as e:
        logger.error(f"Error retrieving hero '{hero_id}': {e}")
        raise HTTPException(status_code=e.status_code, detail=str(e))


# GET: Retrieve all heroes
@router.get("/heroes/", response_model=List[DnDHero])
async def read_heroes():
    try:
        logger.info("Fetching all heroes.")
        heroes = list(container.read_all_items())
        logger.info(f"Retrieved {len(heroes)} heroes.")
        return heroes
    except exceptions.CosmosHttpResponseError as e:
        logger.error(f"Error retrieving heroes: {e}")
        raise HTTPException(status_code=e.status_code, detail=str(e))


# DELETE: Delete a hero by ID
@router.delete("/heroes/{hero_id}", response_model=dict)
async def delete_hero(hero_id: str):
    try:
        logger.info(f"Attempting to delete hero with ID: {hero_id}")
        container.delete_item(hero_id, partition_key=hero_id)
        logger.info(f"Hero '{hero_id}' deleted successfully.")
        return {"message": f"Hero with id '{hero_id}' deleted successfully"}
    except exceptions.CosmosResourceNotFoundError:
        logger.warning(f"Hero with ID '{hero_id}' not found for deletion.")
        raise HTTPException(status_code=404, detail="Hero not found")
    except exceptions.CosmosHttpResponseError as e:
        logger.error(f"Error deleting hero '{hero_id}': {e}")
        raise HTTPException(status_code=e.status_code, detail=str(e))


# GET: Custom query to retrieve heroes with Fireball spell and AC < 20
@router.get("/heroes-fireball-low-ac", response_model=List[DnDHero])
async def get_fireball_heroes_with_low_ac():
    query = """
    SELECT *
    FROM c
    WHERE ARRAY_CONTAINS(c.spells, {"name": "Fireball"}, true)
    AND c.armor_class < 20
    """
    try:
        logger.info("Fetching heroes with Fireball spell and AC < 20.")
        # Execute the query
        results = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        logger.info(f"Found {len(results)} heroes with Fireball and AC < 20.")
        return results
    except exceptions.CosmosHttpResponseError as e:
        logger.error(f"Error fetching Fireball heroes with low AC: {e}")
        raise HTTPException(status_code=e.status_code, detail=str(e))
