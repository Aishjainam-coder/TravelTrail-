import streamlit as st
import requests
from datetime import date, timedelta

# --- Page Config ---
st.set_page_config(page_title="TravelTrail - Flight & Hotel Finder", page_icon="✈️")
st.title("✈️🏨 TravelTrail - Flight & Hotel Finder")

# --- Tab Selection ---
tab1, tab2 = st.tabs(["✈️ Flight Search", "🏨 Hotel Search"])

# --- Base URL ---
BASE_URL = "http://127.0.0.1:8000"

# ===== FLIGHT SEARCH TAB =====
with tab1:
    st.header("Flight Search")
    
    # Flight input fields
    col1, col2 = st.columns(2)
    with col1:
        from_city = st.text_input("From (Airport Code)", value="DEL", key="flight_from")
    with col2:
        to_city = st.text_input("To (Airport Code)", value="BOM", key="flight_to")
    
    departure_date = st.date_input("Departure Date", min_value=date.today(), key="flight_date").strftime("%Y-%m-%d")
    
    # Flight data source toggle
    use_mock_flights = st.checkbox("Use Mock Data (Demo Mode)", value=False, key="flight_mock", help="Use mock data for demonstration.")
    
    # Flight search button
    if st.button("Search Flights", key="flight_search"):
        with st.spinner("Searching for flights..."):
            url = f"{BASE_URL}/travel/recommendations?from_city={from_city}&to_city={to_city}&departure_date={departure_date}&use_mock={use_mock_flights}"
            
            try:
                response = requests.get(url, timeout=15)
                
                if response.status_code == 200:
                    flights = response.json()
                    
                    if not flights or not flights.get("data"):
                        st.warning("No flights found.")
                    else:
                        # Show data source info
                        if use_mock_flights:
                            st.info("📋 Showing mock flight data for demonstration")
                        else:
                            st.success("🌐 Showing real flight data from Amadeus API")
                        
                        for flight in flights["data"]:
                            try:
                                airline = flight.get('validatingAirlineCodes', ['Unknown'])[0]
                                segments = flight.get('itineraries', [{}])[0].get('segments', [])
                                departure_code = segments[0].get('departure', {}).get('iataCode', 'N/A') if segments else 'N/A'
                                arrival_code = segments[-1].get('arrival', {}).get('iataCode', 'N/A') if segments else 'N/A'
                                price = flight.get('price', {}).get('total', 'N/A')
                                duration = flight.get('itineraries', [{}])[0].get('duration', 'N/A')
                                departure_time = flight.get('departure_time', 'N/A')
                                arrival_time = flight.get('arrival_time', 'N/A')

                                st.markdown(f"""
                                    ✈️ **Airline:** {airline}  
                                    🛫 **From:** {departure_code}  
                                    🛬 **To:** {arrival_code}  
                                    💰 **Price:** ₹{price}  
                                    🕐 **Duration:** {duration}  
                                    📅 **Departure:** {departure_time}  
                                    📅 **Arrival:** {arrival_time}  
                                    ---
                                """)
                            except Exception as e:
                                st.error(f"Error displaying a flight: {e}")
                else:
                    st.error(f"Failed to fetch flights: {response.status_code}")
            except requests.exceptions.Timeout:
                st.error("Request timed out. The API might be slow or overloaded.")
                st.info("💡 Try using mock data for faster results!")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
                st.info("💡 Try using mock data for faster results!")

# ===== HOTEL SEARCH TAB =====
with tab2:
    st.header("Hotel Search")
    
    # Hotel input fields
    col1, col2 = st.columns(2)
    with col1:
        city = st.text_input("City Code (e.g., BOM for Mumbai)", value="BOM", key="hotel_city")
    with col2:
        adults = st.number_input("Number of Adults", min_value=1, max_value=10, value=1, key="hotel_adults")
    
    col3, col4 = st.columns(2)
    with col3:
        check_in = st.date_input("Check-in Date", min_value=date.today(), key="checkin_date")
    with col4:
        check_out = st.date_input("Check-out Date", min_value=check_in + timedelta(days=1), key="checkout_date")
    
    # Hotel data source toggle
    use_mock_hotels = st.checkbox("Use Mock Data (Demo Mode)", value=False, key="hotel_mock", help="Use mock data for demonstration.")
    
    # Hotel search button
    if st.button("Search Hotels", key="hotel_search"):
        with st.spinner("Searching for hotels..."):
            url = f"{BASE_URL}/travel/hotel-recommendations?city={city}&check_in={check_in}&check_out={check_out}&adults={adults}&use_mock={use_mock_hotels}"
            
            try:
                response = requests.get(url, timeout=15)
                
                if response.status_code == 200:
                    hotels = response.json()
                    
                    if not hotels or not hotels.get("data"):
                        st.warning("No hotels found.")
                    else:
                        # Show data source info
                        if use_mock_hotels:
                            st.info("📋 Showing mock hotel data for demonstration")
                        else:
                            st.success("🌐 Showing real hotel data from Amadeus API")
                        
                        for hotel in hotels["data"]:
                            try:
                                name = hotel.get('name', 'Unknown Hotel')
                                city_name = hotel.get('address', {}).get('cityName', 'Unknown City')
                                price = hotel.get('offers', [{}])[0].get('price', {}).get('total', 'N/A')
                                star_rating = hotel.get('starRating', 'N/A')
                                amenities = hotel.get('amenities', [])
                                room_type = hotel.get('offers', [{}])[0].get('room', {}).get('type', 'Standard Room')

                                st.markdown(f"""
                                    🏨 **Hotel:** {name}  
                                    🌍 **City:** {city_name}  
                                    💰 **Price:** ₹{price}  
                                    ⭐ **Rating:** {star_rating} stars  
                                    🛏️ **Room:** {room_type}  
                                    🎯 **Amenities:** {', '.join(amenities[:3])}  
                                    ---
                                """)
                            except Exception as e:
                                st.error(f"Error displaying a hotel: {e}")
                else:
                    st.error(f"Failed to fetch hotels: {response.status_code}")
            except requests.exceptions.Timeout:
                st.error("Request timed out. The API might be slow or overloaded.")
                st.info("💡 Try using mock data for faster results!")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
                st.info("💡 Try using mock data for faster results!")

# --- Footer ---
st.markdown("---")
st.markdown("**TravelTrail** - Your complete travel companion for flights and hotels! ✈️🏨") 