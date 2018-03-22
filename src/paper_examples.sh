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

python -m rideshare.create_data \
    "Edwards Stadium, 2223 Fulton Street, Berkeley, CA 94704, United States"\
    "Familia Cristiana Verbo, 2798 Bay Rd, Redwood City, CA 94063, United States"\
    "City of Berkeley - Civic Center, 2180 Milvia Street, Berkeley, CA 94704, United States"\
    "Pets In Need, 871 Fifth Avenue, Redwood City, CA 94063, United States"\
    --out "out/paper/ucb_rwc" --engine "OSM"

#python -m rideshare.create_data \
#    "Mexico Lindo, 33306 Alvarado-Niles Road, Union City, CA 94587, United States"\
#    "ARCO, 1200 Geneva Avenue, San Francisco, CA 94112, United States"\
#    "Filoli, 86 Cañada Road, Woodside, CA 94062, United States"\
#    "Thornhill Nursery, 6250 Thornhill Drive, Oakland, CA 94611, United States"\
#    --out "out/paper/psi" --engine "OSM"


#python -m rideshare.create_data \
#    "Edwards Stadium, 2223 Fulton Street, Berkeley, CA 94704, United States"\
#    "Familia Cristiana Verbo, 2798 Bay Rd, Redwood City, CA 94063, United States"\
#    "Alameda de las Pulgas & W 20th Ave, San Mateo, CA 94403, United States"\
#    "Usborne Books and More, 26724 Lauderdale Ave, Hayward, CA 94545, USA"\
#    --out "out/paper/psi1" --engine "OSM"
#
#
# python -m rideshare.create_data \
#     "James Bateman, RPH, 27212 Calaroga Avenue, Hayward, CA 94545, Hayward, CA 94545, United States"\
#     "DMV San Mateo, 425 N Amphlett Blvd, San Mateo, CA 94401, USA"\
#     "Alameda de las Pulgas & W 20th Ave, San Mateo, CA 94403, United States"\
#     "Hayward Police Department, 300 W Winton Ave, Hayward, CA 94544, USA"\
#     --out "out/paper/psi2" --engine "OSM"

python -m rideshare.plotty