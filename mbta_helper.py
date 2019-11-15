# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://open.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = "yVdtBiZA6oLGT8mE9AkXYYszWmPsx1rD"
MBTA_API_KEY = "22c19fd52b5e4c2ea304b61e8bbee70d"


# A little bit of scaffolding if you want to use it

import json
import urllib.request
from pprint import pprint


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """
    location = place_name.replace(' ', '%20')
    MAPQUEST = f'http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location={location}'
    response = get_json(MAPQUEST)
    latitude_longitude = response['results'][0]['locations'][0]['displayLatLng']
    latitude = latitude_longitude['lat']
    longitude = latitude_longitude['lng']
    return (latitude, longitude)


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """
    MBTA = f'{MBTA_BASE_URL}?api_key={MBTA_API_KEY}&filter[latitude]={latitude}&filter[longitude]={longitude}&sort=distance'
    response2 = get_json(MBTA)
    for *station_name, wheelchair_accessible in response2:
        station_name = response2['data'][0]['attributes']['name']
        wheelchair_accessible = response2['data'][0]['attributes']['wheelchair_boarding']
        return (station_name, wheelchair_accessible)
    return None, None


def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    latitude, longitude = get_lat_long(place_name)
    station, wheelchair = get_nearest_station(latitude, longitude)
    if wheelchair == 2:
        return "Inaccessible"
    elif wheelchair == 1:
        return "Accessible"
    else:
        return "No information"
    return (station, wheelchair)
    


def main():
    """
    You can all the functions here
    """
    #print(get_lat_long('Faneuil Hall Marketplace'))
    #print(get_nearest_station(42.36048, -71.05414))
    # print(find_stop_near('Prudential Center'))


if __name__ == '__main__':
    main()
