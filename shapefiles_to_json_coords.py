'''
Converts Promise Zone shapefiles to JSON boundary coordinate files.

Download input shapefiles from:
http://egis.hud.opendata.arcgis.com/datasets/a10cbd9187a34bd2a28574a3cfe12e64_0
'''
import json
import os
import shapefile


INPUT = 'shapefiles/Promise_Zones'
NAME_FIELD = 'PZ_Name'
OUTPUT = 'coords'


sf = shapefile.Reader(INPUT)

for i, field in enumerate(sf.fields[1:]):
    if NAME_FIELD == field[0]:
        name_index = i

all_pzs = {}

if not os.path.exists(OUTPUT):
    os.makedirs(OUTPUT)

for sr in sf.iterShapeRecords():
    name = sr.record[name_index]
    filename = name.replace(' ', '_').lower() + '.json'
    points = list(map(tuple, sr.shape.points))

    all_pzs[name] = points

    with open(os.path.join(OUTPUT, filename), 'w') as f:
        f.write(json.dumps(points))

with open(os.path.join(OUTPUT, 'all.json'), 'w') as f:
    f.write(json.dumps(all_pzs))
