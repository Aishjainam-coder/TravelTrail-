from fastapi import APIRouter, Request, Query
import json
from ranking import rank_flights, rank_hotels
from amadeus_api import fetch_flights, fetch_hotels

router = APIRouter()

# ===== FLIGHT RECOMMENDATIONS =====
@router.get("/recommendations")
def get_top_flights(
    from_city: str = Query(..., description="Departure city"),
    to_city: str = Query(..., description="Arrival city"),
    departure_date: str = Query(..., description="YYYY-MM-DD format"),
    use_mock: bool = Query(False, description="Use mock data or real API")
):
    try:
        if use_mock:
            # Use mock data when explicitly requested
            with open("mock_flights.json") as f:
                mock_data = json.load(f)
            
            # Convert mock data to Amadeus API format
            converted_data = {
                "data": [
                    {
                        "price": {"total": str(flight["price_usd"])},
                        "itineraries": [{
                            "duration": flight["duration"],
                            "segments": [{
                                "departure": {"iataCode": from_city},
                                "arrival": {"iataCode": to_city}
                            }]
                        }],
                        "validatingAirlineCodes": [flight["airline"]],
                        "flight_number": flight["flight_number"],
                        "departure_time": flight["departure_time"],
                        "arrival_time": flight["arrival_time"],
                        "loyalty_score": flight["loyalty_score"]
                    }
                    for flight in mock_data
                ]
            }
            data = converted_data
        else:
            # Try to fetch real data first, fallback to mock if API fails
            try:
                data = fetch_flights(from_city, to_city, departure_date)
            except Exception as api_error:
                print(f"API Error: {api_error}")
                # Fallback to mock data
                with open("mock_flights.json") as f:
                    mock_data = json.load(f)
                
                converted_data = {
                    "data": [
                        {
                            "price": {"total": str(flight["price_usd"])},
                            "itineraries": [{
                                "duration": flight["duration"],
                                "segments": [{
                                    "departure": {"iataCode": from_city},
                                    "arrival": {"iataCode": to_city}
                                }]
                            }],
                            "validatingAirlineCodes": [flight["airline"]],
                            "flight_number": flight["flight_number"],
                            "departure_time": flight["departure_time"],
                            "arrival_time": flight["arrival_time"],
                            "loyalty_score": flight["loyalty_score"]
                        }
                        for flight in mock_data
                    ]
                }
                data = converted_data

        ranked = rank_flights(data)
        return {"data": ranked[:5]}  # top 5 results
    except Exception as e:
        return {"error": str(e)}

# ===== HOTEL RECOMMENDATIONS =====
@router.get("/hotels")
def get_hotels(
    city: str = Query(..., description="City code (e.g., BOM for Mumbai)"),
    check_in: str = Query(..., description="Check-in date (YYYY-MM-DD)"),
    check_out: str = Query(..., description="Check-out date (YYYY-MM-DD)"),
    adults: int = Query(1, description="Number of adults")
):
    """Get raw hotel data"""
    try:
        return fetch_hotels(city, check_in, check_out, adults)
    except Exception as e:
        return {"error": str(e)}

@router.get("/hotel-recommendations")
def get_top_hotels(
    city: str = Query(..., description="City code (e.g., BOM for Mumbai)"),
    check_in: str = Query(..., description="Check-in date (YYYY-MM-DD)"),
    check_out: str = Query(..., description="Check-out date (YYYY-MM-DD)"),
    adults: int = Query(1, description="Number of adults"),
    use_mock: bool = Query(False, description="Use mock data or real API")
):
    """Get top 5 ranked hotels"""
    try:
        if use_mock:
            # Use mock data when explicitly requested
            with open("mock_hotels.json") as f:
                mock_data = json.load(f)
            data = {"data": mock_data}
        else:
            # Try to fetch real data first, fallback to mock if API fails
            try:
                data = fetch_hotels(city, check_in, check_out, adults)
                if not data or not data.get("data"):
                    # If API returns empty data, use mock
                    with open("mock_hotels.json") as f:
                        mock_data = json.load(f)
                    data = {"data": mock_data}
            except Exception as api_error:
                print(f"Hotel API Error: {api_error}")
                # Fallback to mock data
                with open("mock_hotels.json") as f:
                    mock_data = json.load(f)
                data = {"data": mock_data}

        ranked = rank_hotels(data)
        return {"data": ranked[:5]}  # top 5 results
    except Exception as e:
        print(f"Hotel recommendation error: {e}")
        # Final fallback - return mock data directly
        try:
            with open("mock_hotels.json") as f:
                mock_data = json.load(f)
            return {"data": mock_data[:5]}
        except:
            return {"error": str(e)}
