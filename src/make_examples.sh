#!/usr/bin/env bash

#python -m rideshare.create_data "Gothenburg Central Station" "Stockholm Central Station" "Malmoe Central Station" "Uppsala Central Station" --out "out/poly/large"  --engine "google_polyline"
#python -m rideshare.create_data "Lindome station, Mölndal" "Liseberg, Örgrytevägen 5, 402 22 Göteborg" "Kållered, Mölndal" "ICA Supermarket Olskroken, Göteborg" --out "out/poly/medium"  --engine "google_polyline"
#python -m rideshare.create_data "Doktor Forselius Backe 17, 413 26 Göteborg" "Lindholmen, Göteborg" "Maskingränd 2, 412 58 Göteborg" "Lindholmen, Göteborg" --out "out/poly/small"  --engine "google_polyline"
#
#python -m rideshare.create_data "Gothenburg Central Station" "Stockholm Central Station" "Malmoe Central Station" "Uppsala Central Station" --out "out/step/large" --engine "google_step"
#python -m rideshare.create_data "Lindome station, Mölndal" "Liseberg, Örgrytevägen 5, 402 22 Göteborg" "Kållered, Mölndal" "ICA Supermarket Olskroken, Göteborg" --out "out/step/medium" --engine "google_step"
#python -m rideshare.create_data "Doktor Forselius Backe 17, 413 26 Göteborg" "Lindholmen, Göteborg" "Maskingränd 2, 412 58 Göteborg" "Lindholmen, Göteborg" --out "out/step/small" --engine "google_step"
#
#python -m rideshare.create_data "Gothenburg Central Station" "Stockholm Central Station" "Malmoe Central Station" "Uppsala Central Station" --out "out/here/large" --engine "heremaps"
#python -m rideshare.create_data "Lindome station, Mölndal" "Liseberg, Örgrytevägen 5, 402 22 Göteborg" "Kållered, Mölndal" "ICA Supermarket Olskroken, Göteborg" --out "out/here/medium" --engine "heremaps"
#python -m rideshare.create_data "Doktor Forselius Backe 17, 413 26 Göteborg" "Lindholmen, Göteborg" "Maskingränd 2, 412 58 Göteborg" "Lindholmen, Göteborg" --out "out/here/small" --engine "heremaps"

# python -m rideshare.create_data "Gothenburg Central Station" "Stockholm Central Station" "Malmoe Central Station" "Uppsala Central Station" --out "out/osm/large" --engine "OSM"
# python -m rideshare.create_data "Alingsås Golfklubb, SVANVIKSVÄGEN 1, 441 95 Alingsås" "Stockholm Central Station" "Hjälmared allé" "Clarion, Östra Järnvägsgatan, Stockholm" --out "out/osm/tricky" --engine "OSM"
# python -m rideshare.create_data "Alingsås Golfklubb, SVANVIKSVÄGEN 1, 441 95 Alingsås" "Elfviks Gård, Elfviksvägen, 181 90 Lidingö" "Hjälmared allé" "Drottningholm Palace, Stockholm" --out "out/osm/impossible" --engine "OSM"
# python -m rideshare.create_data "Lindome station, Mölndal" "Liseberg, Örgrytevägen 5, 402 22 Göteborg" "Kållered, Mölndal" "ICA Supermarket Olskroken, Göteborg" --out "out/osm/medium" --engine "OSM"
python -m rideshare.create_data "Doktor Forselius Backe 17, 413 26 Göteborg" "Lindholmen, Göteborg" "Maskingränd 2, 412 58 Göteborg" "Lindholmen, Göteborg" --out "damn_out/osm/small" --engine "OSM"
# python -m rideshare.create_data "Partille Station" "Mora, Dalarna" "Göteborg SKF" "Vemdalen, Härjedalen" --out "out/osm/hybrid" --engine "OSM"
# python -m rideshare.create_data "Gothenburg Central Station" "Vara Station" "Jönköping Station" "Uppsala Central Station" --out "out/osm/extras" --engine "OSM"
