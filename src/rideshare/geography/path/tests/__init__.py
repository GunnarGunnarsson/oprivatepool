# -*- coding: utf-8 -*-
from rideshare.geography.geopoint import GeoPoint
from rideshare.geography.path.osm_engine import OSMMapPath

GOTEBORG = 0
STOCKHOLM = 1
MALMO = 2
UPPSALA = 3
LINDOME = 4
LISEBERG = 5
KALLERED = 6
OLSKROKEN = 7
HOME = 8
LINDHOLMEN = 9
WORK = 10
ALINGSAS = 11
HJALMARED = 12
EJDERG = 13
SKF = 14
MORA = 15
VEMDALEN = 16

places = [
    u"Gothenburg Central Station",
    u"Stockholm Central Station",
    u"Malmö",
    u"Uppsala Central Station",
    u"Lindome station, Mölndal",
    u"Lisebergshallen, Göteborg",
    u"Kållered, Mölndal",
    u"ICA Supermarket Olskroken, Göteborg",
    u"Doktor Forselius Backe, Göteborg",
    u"Lindholmen, Göteborg",
    u"Maskingränd 2, Göteborg",
    u"Alingsås Golfklubb, SVANVIKSVÄGEN 1, 441 95 Alingsås",
    u"Hjälmared allé",
    u"Göteborg Ejdergatan",
    u"Göteborg SKF",
    u"Vasaloppets Hus, Mora, Dalarna",
    u"Vemdalen Centrum, Vemdalen, Härjedalen"
]

places_points = {
    u"Gothenburg Central Station": GeoPoint(57.7091812, 11.9730036),
    u"Stockholm Central Station": GeoPoint(59.3322881, 18.062902),
    u"Malmö": GeoPoint(55.6052931, 13.0001566),
    u"Uppsala Central Station": GeoPoint(59.85820965, 17.646583181),
    u"Lindome station, Mölndal": GeoPoint(57.5757255, 12.0804409),
    u"Lisebergshallen, Göteborg": GeoPoint(57.69683065, 11.9918264083),
    u"Kållered, Mölndal": GeoPoint(57.61023, 12.0498343),
    u"ICA Supermarket Olskroken, Göteborg": GeoPoint(57.7149085, 12.0005777),
    u"Doktor Forselius Backe, Göteborg": GeoPoint(57.6780556, 11.9805532),
    u"Lindholmen, Göteborg": GeoPoint(57.71081355, 11.9446016575),
    u"Maskingränd 2, Göteborg": GeoPoint(57.6883373, 11.978988),
    u"Alingsås Golfklubb, SVANVIKSVÄGEN 1, 441 95 Alingsås": GeoPoint(57.9300205, 12.5362113),
    u"Hjälmared allé": GeoPoint(57.8949642, 12.5492333),
    u"Göteborg Ejdergatan": GeoPoint(57.720553, 12.0057673),
    u"Göteborg SKF": GeoPoint(57.7291724, 12.0132253),
    u"Vasaloppets Hus, Mora, Dalarna": GeoPoint(61.004878, 14.537003),
    u"Vemdalen Centrum, Vemdalen, Härjedalen": GeoPoint(62.4473975, 13.8627961),
}

map_paths = [
    # ('Google', GoogleMapPath()),
    # ('HERE', HereMapPath()),
    ('OSM', OSMMapPath())
]
