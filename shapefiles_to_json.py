'''
Converts Promise Zone shapefiles to JSON files with bounding box, coordinates,
center point, and effective radius in miles. All coordinates are lon, lat.

Download input shapefiles from:
http://egis.hud.opendata.arcgis.com/datasets/a10cbd9187a34bd2a28574a3cfe12e64_0
'''
import json
import os
import shapefile

from geopy.distance import vincenty


INPUT = 'shapefiles/Promise_Zones'
NAME_FIELD = 'PZ_Name'
OUTPUT = 'json'


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

all_pzs = {}

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

    pz_data = {
        'bbox': list(bbox),
        'coords': coords,
        'center': center,
        'radius_miles': radius,
    }

    filename = name.replace(' ', '_').lower() + '.json'
    with open(os.path.join(OUTPUT, filename), 'w') as f:
        f.write(json.dumps(pz_data))

    all_pzs[name] = pz_data

with open(os.path.join(OUTPUT, 'all.json'), 'w') as f:
    f.write(json.dumps(all_pzs))
