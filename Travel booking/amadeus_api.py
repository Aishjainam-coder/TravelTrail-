import requests
import json
import time
import os


CLIENT_ID = "crn7WV8YQoM17RrkoAY38ekKhS57rxGw"
CLIENT_SECRET = "HMCGvXA6GvTMxShh"

# Cache for access token to avoid repeated requests
_access_token = None
_token_expiry = 0

def get_access_token():
    global _access_token, _token_expiry
    
    # Check if we have a valid cached token
    if _access_token and time.time() < _token_expiry:
        return _access_token
    
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    try:
        response = requests.post(url, data=data, timeout=5)  # Reduced timeout
        if response.status_code == 200:
            token_data = response.json()
            _access_token = token_data["access_token"]
            # Cache token for 20 minutes (token expires in 30 minutes)
            _token_expiry = time.time() + 1200
            return _access_token
        else:
            print(f"Token request failed: {response.status_code}")
            raise Exception(f"Failed to get access token: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Network error getting token: {e}")
        raise Exception(f"Network error: {e}")

# ===== FLIGHT API FUNCTIONS =====
def fetch_flights(from_city, to_city, departure_date):
    try:
        access_token = get_access_token()
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        params = {
            "originLocationCode": from_city,
            "destinationLocationCode": to_city,
            "departureDate": departure_date,
            "adults": 1,
            "max": 5,
            "currencyCode": "INR"  # Get prices in INR
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Reduced timeout for faster response
        response = requests.get(url, headers=headers, params=params, timeout=8)

        if response.status_code == 200:
            # Save the response to a local JSON file for debugging
            with open("mock_flights.json", "w") as f:
                json.dump(response.json(), f, indent=2)
            return response.json()
        elif response.status_code == 429:
            print("API rate limit exceeded. Using mock data instead.")
            raise Exception("API rate limit exceeded")
        elif response.status_code == 401:
            print("API authentication failed. Using mock data instead.")
            raise Exception("API authentication failed")
        else:
            print(f"Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            raise Exception(f"Flight data fetch failed with status {response.status_code}")

    except requests.exceptions.Timeout:
        print("Request timed out. Using mock data instead.")
        raise Exception("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        raise Exception(f"Network error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise e

# ===== HOTEL API FUNCTIONS =====
def fetch_hotels(city_code, check_in, check_out, adults=1):
    """
    Fetch hotels using Amadeus API
    city_code: IATA city code (e.g., 'BOM' for Mumbai)
    check_in: YYYY-MM-DD format
    check_out: YYYY-MM-DD format
    """
    try:
        access_token = get_access_token()
        url = "https://test.api.amadeus.com/v2/reference-data/locations/hotels/by-city"
        
        # First, get hotel list for the city
        params = {
            "cityCode": city_code,
            "radius": 5,
            "radiusUnit": "KM"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(url, headers=headers, params=params, timeout=8)
        
        if response.status_code == 200:
            hotels_list = response.json()
            
            # Get hotel offers for available hotels
            hotel_offers = []
            for hotel in hotels_list.get("data", [])[:10]:  # Limit to 10 hotels
                hotel_id = hotel.get("hotelId")
                if hotel_id:
                    offers = get_hotel_offers(hotel_id, check_in, check_out, adults, access_token)
                    if offers:
                        hotel_offers.extend(offers)
            
            # Save to mock file for debugging
            with open("mock_hotels.json", "w") as f:
                json.dump(hotel_offers, f, indent=2)
            
            return {"data": hotel_offers}
        elif response.status_code == 429:
            print("API rate limit exceeded. Using mock data instead.")
            raise Exception("API rate limit exceeded")
        elif response.status_code == 401:
            print("API authentication failed. Using mock data instead.")
            raise Exception("API authentication failed")
        else:
            print(f"Request failed: {response.status_code}")
            raise Exception(f"Hotel data fetch failed with status {response.status_code}")

    except requests.exceptions.Timeout:
        print("Request timed out. Using mock data instead.")
        raise Exception("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        raise Exception(f"Network error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise e

def get_hotel_offers(hotel_id, check_in, check_out, adults, access_token):
    """Get offers for a specific hotel"""
    try:
        url = "https://test.api.amadeus.com/v3/shopping/hotel-offers"
        params = {
            "hotelIds": hotel_id,
            "checkInDate": check_in,
            "checkOutDate": check_out,
            "adults": adults,
            "currency": "INR"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(url, headers=headers, params=params, timeout=8)
        
        if response.status_code == 200:
            return response.json().get("data", [])
        else:
            return []
    except:
        return []
