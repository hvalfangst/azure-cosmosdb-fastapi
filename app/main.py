# app/main.py

from fastapi import FastAPI
from app.routers import heroes

app = FastAPI(
    title="Hero API",
    description="An API to manage heroes using Azure Cosmos DB",
    version="1.0.0"
)

# Include the heroes router
app.include_router(heroes.router, prefix="/api", tags=["Heroes"])


# Optional root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Hero API"}