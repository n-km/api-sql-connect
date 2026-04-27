"""
API for User Management (SQL-Connect)

Main entry point of the application. It initializes the FastAPI app 
and connects the different module routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.routes import router

# Initialize the FastAPI app
app = FastAPI(
    title="API SQL Connect",
    description="A backend service to manage user data in an SQLite database.",
    version="1.0.0"
)

# CORS configuration: Allows requests from any website
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect all routes from the modules folder
app.include_router(router)