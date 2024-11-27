from opensky_api import OpenSkyApi
from geopy.distance import geodesic
import json


def get_aircraft_data(lat, lon, radius):
    """
    Fetches live positional data for aircraft around a given location.

    Args:
        lat (float): Latitude of the center point.
        lon (float): Longitude of the center point.
        radius (int): Radius in kilometers to search around the location.

    Returns:
        list: A list of aircraft data, including position and other metadata.
    """
    api = OpenSkyApi()

    try:
        # Get states from the API
        states = api.get_states()

        if not states or not states.states:
            print("No aircraft data available.")
            return []

        aircraft_data = []

        # Filter aircraft based on the given radius
        for aircraft in states.states:
            if aircraft.latitude is not None and aircraft.longitude is not None:
                # Calculate distance using geopy
                distance = geodesic(
                    (lat, lon), (aircraft.latitude, aircraft.longitude)
                ).km
                if distance <= radius:
                    aircraft_data.append(
                        {
                            "icao24": aircraft.icao24,
                            "callsign": (
                                aircraft.callsign.strip()
                                if aircraft.callsign
                                else "Unknown"
                            ),
                            "origin_country": aircraft.origin_country,
                            "latitude": aircraft.latitude,
                            "longitude": aircraft.longitude,
                            "altitude": aircraft.baro_altitude,
                            "velocity": aircraft.velocity,
                            "true_track": aircraft.true_track,  # Correct attribute name
                            "vertical_rate": aircraft.vertical_rate,
                        }
                    )

        return aircraft_data

    except Exception as e:
        print(f"An error occurred while fetching aircraft data: {e}")
        return []
