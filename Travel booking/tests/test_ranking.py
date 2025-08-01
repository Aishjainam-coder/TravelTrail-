import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ranking import rank_flights, rank_hotels

class TestRanking(unittest.TestCase):
    def test_flight_ranking(self):
        mock_data = {
            "data": [
                {"price": {"total": "100"}, "itineraries": [{"duration": "PT2H"}]},
                {"price": {"total": "200"}, "itineraries": [{"duration": "PT1H"}]},
            ]
        }
        ranked = rank_flights(mock_data)
        self.assertEqual(len(ranked), 2)
        self.assertLessEqual(float(ranked[0]["price"]["total"]), float(ranked[1]["price"]["total"]))

    def test_hotel_ranking(self):
        mock_data = {
            "data": [
                {"offers": [{"price": {"total": "1000"}}], "amenities": ["WiFi"], "starRating": 5},
                {"offers": [{"price": {"total": "2000"}}], "amenities": ["WiFi", "Pool"], "starRating": 4},
            ]
        }
        ranked = rank_hotels(mock_data)
        self.assertEqual(len(ranked), 2)
        self.assertLessEqual(float(ranked[0]["offers"][0]["price"]["total"]), float(ranked[1]["offers"][0]["price"]["total"]))

if __name__ == "__main__":
    unittest.main() 