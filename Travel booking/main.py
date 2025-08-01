from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from amadeus_api import fetch_flights
from recommendation import router as recommendation_router

app = FastAPI()

# Enable CORS for Streamlit or any frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Simple API to fetch raw flights (bypasses ranking)
@app.get("/flights")
def get_flights(from_city: str, to_city: str, departure_date: str):
    return fetch_flights(from_city, to_city, departure_date)

# Include all endpoints (flights and hotels) from recommendation.py
app.include_router(recommendation_router, prefix="/travel")
