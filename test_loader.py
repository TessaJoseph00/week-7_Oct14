import unittest
import pandas as pd
from loader import get_geolocator, fetch_location_data, build_geo_dataframe


class TestLoader(unittest.TestCase):

    def test_valid_locations(self):
        """Test known valid locations with expected coordinates and type."""
        geolocator = get_geolocator()

        expected_data = [
            {
                "name": "Museum of Modern Art",
                "latitude": 40.7618552,
                "longitude": -73.9782438,
                "type": "museum"
            },
            {
                "name": "USS Alabama Battleship Memorial Park",
                "latitude": 30.684373,
                "longitude": -88.015316,
                "type": "park"
            }
        ]

        for place in expected_data:
            result = fetch_location_data(geolocator, place["name"])
            self.assertIsInstance(result, dict, f"Expected dict for {place['name']}.")

            # Allow small rounding differences
            self.assertAlmostEqual(result["latitude"], place["latitude"], places=2)
            self.assertAlmostEqual(result["longitude"], place["longitude"], places=2)

            # Allow 'unknown' in case geo_type is missing
            result_type = result["type"].lower() if result["type"] else "unknown"
            self.assertIn(result_type, [place["type"].lower(), "unknown"],
                          f"Expected type to be '{place['type']}' or 'unknown', but got '{result['type']}'.")

    def test_invalid_location(self):
        """Invalid location should return NaN values"""
        geolocator = get_geolocator()
        locations = ["asdfqwer1234"]
        df = build_geo_dataframe(geolocator, locations)

        self.assertEqual(df.shape[0], 1, "DataFrame should contain one row.")
        self.assertEqual(df.loc[0, "location"], "asdfqwer1234")
        self.assertTrue(pd.isna(df.loc[0, "latitude"]), "Latitude should be NaN.")
        self.assertTrue(pd.isna(df.loc[0, "longitude"]), "Longitude should be NaN.")
        self.assertTrue(pd.isna(df.loc[0, "type"]), "Type should be NaN.")


if __name__ == "__main__":
    unittest.main()