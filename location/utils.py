import requests

from .models import Locality, LocalityType


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
        print(result)

        return result
    else:
        return []