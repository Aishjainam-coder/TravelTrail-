# TravelTrail – Business-Travel Optimizer

## Overview
TravelTrail is a web service that helps business travelers find and rank the best flight and hotel options using free-tier APIs. It combines cost, duration, and loyalty (mocked) for flights, and cost, amenities, and star rating for hotels, displaying the top recommendations in a user-friendly web UI.

---

## Features
- 🔑 Uses free/sandbox Amadeus API for flights and hotels (single API key)
- 🏆 Ranks options by cost, time, and loyalty (flights) or amenities (hotels)
- 🖥️ Modern web UI (Streamlit) with tabs for flights and hotels
- 🧪 Mock data fallback for both flights and hotels
- 📊 Top 5 recommendations returned and displayed
- 📝 Easy to extend and test

---

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/Aishjainam-coder/TravelTrail-.git
   cd TravelTrail-
   ```

2. **Install dependencies**
   ```bash
   pip install fastapi uvicorn streamlit requests
   ```

3. **Set up Amadeus API keys**
   - Get free sandbox keys from [Amadeus for Developers](https://developers.amadeus.com/self-service-apis)
   - Add your `CLIENT_ID` and `CLIENT_SECRET` in `amadeus_api.py`

4. **Run the backend**
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

5. **Run the UI**
   ```bash
   streamlit run streamlit_app.py
   ```

---

## API Endpoints

- **Flights:**  
  `GET /travel/flights?from_city=DEL&to_city=BOM&departure_date=2025-08-01`
- **Hotels:**  
  `GET /travel/hotels?city=BOM&check_in=2025-08-01&check_out=2025-08-02`
- **Flight Recommendations:**  
  `GET /travel/recommendations?...`
- **Hotel Recommendations:**  
  `GET /travel/hotel-recommendations?...`

---

## UI Usage

- Open [http://localhost:8502](http://localhost:8502)
- Use the tabs to search for flights or hotels
- Enter your parameters and click search
- Results are ranked and displayed instantly

---

## Project Structure

```
TravelTrail/
├── README.md
├── prompt_log.md
├── .gitignore
├── main.py
├── amadeus_api.py
├── recommendation.py
├── ranking.py
├── streamlit_app.py
├── mock_flights.json
├── mock_hotels.json
└── tests/
    └── test_ranking.py
```

---

## Mock Data

- `mock_flights.json` and `mock_hotels.json` are used if the API fails or you select "Use Mock Data".

---

## Testing

- See `tests/test_ranking.py` for ranking logic tests.
- You can run tests with:
  ```bash
  python -m unittest discover tests
  ```

---

## License

MIT 