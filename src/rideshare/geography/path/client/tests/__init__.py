from rideshare.geography.path.tests import places_points


def geocode_place(place, client=None):
    location = places_points.get(place)
    if location:
        return location
    elif client:
        return client.geocode(place)
    else:
        raise ValueError
