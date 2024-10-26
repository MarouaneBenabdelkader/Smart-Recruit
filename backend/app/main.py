from fastapi import FastAPI, HTTPException, Depends, status
from pymongo.errors import DuplicateKeyError
from models.user import User
from database import get_database
from database import connect_to_mongo, close_mongo_connection

from router.auth_router import router as auth_router

from pydantic import BaseModel, EmailStr
from resources.nlp_loader import NLPResources
from router.resume_router import router as resume_router

app = FastAPI()


async def startup_event():
    # This function will be called when the application starts.
    await connect_to_mongo()
    resources = NLPResources.get_instance()
    print("Resources loaded and ready to use.")


async def shutdown_event():
    # This function will be called when the application shuts down.
    await close_mongo_connection()


app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)
app.include_router(auth_router)
app.include_router(resume_router)
