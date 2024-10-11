import logging

from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic_settings import BaseSettings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    COSMOS_CONNECTION_STRING: str
    DATABASE_NAME: str
    CONTAINER_NAME: str

    class Config:
        env_file = ".env_cosmosdb"


def initialize_settings():
    try:
        # Create an instance of Settings
        local_settings = Settings()

        # Check if the required fields are set
        if not local_settings.COSMOS_CONNECTION_STRING or not local_settings.DATABASE_NAME or not local_settings.CONTAINER_NAME:
            logger.error("One or more required environment variables are missing.")
            raise HTTPException(status_code=500,
                                detail="Configuration error: Required environment variables are missing.")

        logger.info("Settings loaded successfully.")
        return local_settings
    except FileNotFoundError:
        logger.critical(".env file not found.")
        raise HTTPException(status_code=500, detail="Configuration error: .env file not found.")
    except Exception as e:
        logger.critical(f"Error loading settings: {e}")
        raise HTTPException(status_code=500, detail="Configuration error: An error occurred while loading settings.")


# Initialize settings
settings = initialize_settings()
