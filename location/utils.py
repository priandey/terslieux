import requests


def coordinate_to_address(lat, lon):
    filler_address = "Unable to find address"
    payload = {
        'lon': lon,
        'lat': lat,
    }
    r = requests.get("https://api-adresse.data.gouv.fr/reverse/", params=payload)
    r = r.json()
    try:
        if r["features"]:
            cursor = r["features"][0]
            address = cursor['properties']['label']
        else:
            address = filler_address
    except KeyError:
        address = filler_address

    return address


def address_to_coordinate(address):
    payload = {
        "q": address,
        "limit": 1
    }
    r = requests.get("https://api-adresse.data.gouv.fr/search/", params=payload)
    r = r.json()
    try:
        if r["features"]:
            cursor = r["features"][0]
            latitude = cursor["geometry"]["coordinates"][1]
            longitude = cursor["geometry"]["coordinates"][0]
        else:
            latitude = None
            longitude = None
    except KeyError:
        latitude = None
        longitude = None

    return latitude, longitude


def get_near_localities(point):
    """
    Get near localities from french public geo API only ftm
    URL: https://geo.api.gouv.fr/adresse
    :param point: point is a Tuple object (longitude, latitude) in radians
    :return: Return a list of locality model instance
    """
    payload = {
        'lon': point[0],
        'lat': point[1]
    }
    r = requests.get("https://api-adresse.data.gouv.fr/reverse/", params=payload)
    r = r.json()
    if r["features"]:
        cursor = r["features"][0]
        localities = [
            (cursor["properties"]["type"], cursor["properties"]["name"]),
            ("city", cursor["properties"]["city"]),
            ("departement", cursor["properties"]["context"][:2]),
            ("region", cursor["properties"]["context"].split(" ")[2]),
        ]

        try:
            localities.append(("district", cursor["properties"]["district"]))
        except KeyError:
            pass
        result = []
        for loc in localities:
            locality_type = LocalityType.objects.get(label=loc[0])
            locality = Locality.objects.get_or_create(name=loc[1], type=locality_type)
            result.append(locality[0])

        return result
    else:
        return []