'''
Converts Promise Zone shapefiles to GeoJSON Polygon files. Also dumps out
center point (lat, lng) and radius in miles to the console.

Download input shapefiles from:
http://egis.hud.opendata.arcgis.com/datasets/a10cbd9187a34bd2a28574a3cfe12e64_0

Assumes input shapefiles in a local "shapefiles" subdirectory.
'''
from __future__ import print_function

import json
import os
import shapefile

from geopy.distance import vincenty


INPUT = 'shapefiles/Promise_Zones'
NAME_FIELD = 'PZ_Name'
OUTPUT = 'geojson'


def distance_miles(p1, p2):
    lat1 = p1[1]
    lng1 = p1[0]

    lat2 = p2[1]
    lng2 = p2[0]

    return vincenty((lat1, lng1), (lat2, lng2)).miles


sf = shapefile.Reader(INPUT)

for i, field in enumerate(sf.fields[1:]):
    if NAME_FIELD == field[0]:
        name_index = i

if not os.path.exists(OUTPUT):
    os.makedirs(OUTPUT)

for sr in sf.iterShapeRecords():
    name = sr.record[name_index]
    coords = list(map(tuple, sr.shape.points))

    bbox = sr.shape.bbox
    center = (
        (bbox[0] + bbox[2]) / 2.0,
        (bbox[1] + bbox[3]) / 2.0
    )

    radius = 0
    for coord in coords:
        distance = distance_miles(coord, center)
        if distance > radius:
            radius = distance

    geojson = {
        'type': 'Polygon',
        'coordinates': [list(map(list, coords))],
    }

    filename = name.replace(' ', '_').lower() + '.geojson'
    with open(os.path.join(OUTPUT, filename), 'w') as f:
        f.write(json.dumps(geojson))

    print('{}: {},{},{}mi'.format(name, center[1], center[0], radius))
