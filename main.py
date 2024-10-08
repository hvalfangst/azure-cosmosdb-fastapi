from fastapi import FastAPI
from routes import router

app = FastAPI()

# Register routes
app.include_router(router)
