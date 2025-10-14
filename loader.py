from geopy.geocoders import Nominatim
import pandas as pd


def get_geolocator(agent='h501-student'):
    """
    Initiates a Nominatim geolocator instance with a custom user agent.
    """
    return Nominatim(user_agent=agent)


def fetch_location_data(geolocator, loc):
    """
    Fetch latitude, longitude, and type for a given location string.

    If the location is not found or an error occurs, return None for data fields.
    """
    try:
        location = geolocator.geocode(loc, timeout=10)
        if location is None:
            raise ValueError("Location not found.")

        return {
            "location": loc,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "type": getattr(location, "geo_type", None)
        }

    except Exception as e:
        # Optional: log errors for debugging
        print(f"Error fetching data for '{loc}': {e}")
        return {
            "location": loc,
            "latitude": None,
            "longitude": None,
            "type": None
        }


def build_geo_dataframe(geolocator, locations):
    """
    Builds a pandas DataFrame from a list of location names using the geolocator.
    """
    geo_data = [fetch_location_data(geolocator, loc) for loc in locations]
    return pd.DataFrame(geo_data)


if __name__ == "__main__":
    geolocator = get_geolocator()

    locations = [
        "Museum of Modern Art",
        "iuyt8765(*&)",  # Invalid
        "Alaska",
        "Franklin's Barbecue",
        "Burj Khalifa"
    ]

    df = build_geo_dataframe(geolocator, locations)
    df.to_csv("geo_data.csv", index=False)
    print("Geo data saved to geo_data.csv")
