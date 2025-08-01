# ===== FLIGHT RANKING FUNCTIONS =====
def rank_flights(flight_data):
    results = []
    for flight in flight_data["data"]:
        price = float(flight["price"]["total"])
        duration_str = flight["itineraries"][0]["duration"]  # e.g. "PT2H30M"
        duration_minutes = parse_duration(duration_str)
        loyalty_score = 3  # hardcoded for now

        # Lower score = better flight
        score = 0.5 * price + 0.3 * duration_minutes - 0.2 * loyalty_score
        results.append((score, flight))

    # sort by score (lower is better)
    results.sort(key=lambda x: x[0])
    return [item[1] for item in results[:5]]

def parse_duration(duration_str):
    import re
    h = re.search(r'(\d+)H', duration_str)
    m = re.search(r'(\d+)M', duration_str)
    hours = int(h.group(1)) if h else 0
    minutes = int(m.group(1)) if m else 0
    return hours * 60 + minutes

# ===== HOTEL RANKING FUNCTIONS =====
def rank_hotels(hotel_data):
    """
    Rank hotels by cost, location, amenities, and loyalty score
    Lower score = better hotel
    """
    results = []
    
    for hotel in hotel_data.get("data", []):
        try:
            # Extract price
            price = float(hotel.get("offers", [{}])[0].get("price", {}).get("total", "999999"))
            
            # Extract location score (distance from city center)
            location_score = 50  # Default score, could be calculated from coordinates
            
            # Extract amenities score
            amenities = hotel.get("amenities", [])
            amenities_score = len(amenities) * 10  # More amenities = better
            
            # Mock loyalty score (could be based on user preferences)
            loyalty_score = 5  # Default score
            
            # Star rating (1-5 stars)
            star_rating = hotel.get("starRating", 3)
            star_score = (6 - star_rating) * 20  # Lower score for higher stars
            
            # Calculate weighted score
            # Weight: Price (40%), Location (20%), Amenities (20%), Loyalty (10%), Star Rating (10%)
            score = (0.4 * price) + (0.2 * location_score) + (0.2 * (100 - amenities_score)) + (0.1 * loyalty_score) + (0.1 * star_score)
            
            results.append((score, hotel))
            
        except Exception as e:
            print(f"Error ranking hotel: {e}")
            continue
    
    # Sort by score (lower is better)
    results.sort(key=lambda x: x[0])
    return [item[1] for item in results[:5]]  # Return top 5

def parse_hotel_info(hotel):
    """Extract key information from hotel data"""
    try:
        hotel_name = hotel.get("name", "Unknown Hotel")
        city = hotel.get("address", {}).get("cityName", "Unknown City")
        price = hotel.get("offers", [{}])[0].get("price", {}).get("total", "N/A")
        star_rating = hotel.get("starRating", "N/A")
        amenities = hotel.get("amenities", [])
        
        return {
            "name": hotel_name,
            "city": city,
            "price": price,
            "star_rating": star_rating,
            "amenities": amenities[:5]  # Top 5 amenities
        }
    except Exception as e:
        print(f"Error parsing hotel info: {e}")
        return {
            "name": "Unknown Hotel",
            "city": "Unknown City", 
            "price": "N/A",
            "star_rating": "N/A",
            "amenities": []
        }
