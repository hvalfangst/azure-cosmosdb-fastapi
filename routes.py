from fastapi import APIRouter, HTTPException
from azure.cosmos import CosmosClient, exceptions
from pydantic import BaseModel
from typing import List, Optional, Dict

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


class AbilityScores(BaseModel):
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int


class SkillProficiencies(BaseModel):
    acrobatics: bool = False
    animal_handling: bool = False
    arcana: bool = False
    athletics: bool = False
    deception: bool = False
    history: bool = False
    insight: bool = False
    intimidation: bool = False
    investigation: bool = False
    medicine: bool = False
    nature: bool = False
    perception: bool = False
    performance: bool = False
    persuasion: bool = False
    religion: bool = False
    sleight_of_hand: bool = False
    stealth: bool = False
    survival: bool = False


class Equipment(BaseModel):
    weapon: Optional[str] = None
    armor: Optional[str] = None
    items: List[str] = []


class Spell(BaseModel):
    name: str
    level: int
    casting_time: str
    range: str
    components: List[str]
    duration: str


class DnDHero(BaseModel):
    id: str
    name: str
    race: str
    class_: str
    level: int
    background: Optional[str] = None
    alignment: Optional[str] = None

    # Nested fields
    ability_scores: AbilityScores
    skill_proficiencies: SkillProficiencies
    equipment: Equipment
    spells: Optional[List[Spell]] = None  # Optional, only for spellcasters

    hit_points: int
    armor_class: int
    speed: int

    # Additional optional features
    personality_traits: Optional[str] = None
    ideals: Optional[str] = None
    bonds: Optional[str] = None
    flaws: Optional[str] = None


# POST: Create a new DnD Hero
@router.post("/heroes/", response_model=DnDHero)
async def create_hero(hero: DnDHero):
    try:
        container.upsert_item(hero.model_dump())
        return hero
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


# GET: Retrieve a hero by ID
@router.get("/heroes/{hero_id}", response_model=DnDHero)
async def read_hero(hero_id: str):
    try:
        hero = container.read_item(hero_id, partition_key=hero_id)
        return hero
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Hero not found")


# GET: Retrieve all heroes
@router.get("/heroes/", response_model=List[DnDHero])
async def read_heroes():
    heroes = list(container.read_all_items())
    return heroes


# DELETE: Delete a hero by ID
@router.delete("/heroes/{hero_id}", response_model=dict)
async def delete_hero(hero_id: str):
    try:
        container.delete_item(hero_id, partition_key=hero_id)
        return {"message": f"Hero with id '{hero_id}' deleted successfully"}
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Hero not found")


@router.get("/heroes-fireball-low-ac", response_model=List[DnDHero])
async def get_fireball_heroes_with_low_ac():
    query = """
    SELECT *
    FROM c
    WHERE ARRAY_CONTAINS(c.spells, {"name": "Fireball"}, true)
    AND c.armor_class < 20
    """
    try:
        # Execute the query
        results = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        return results
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

