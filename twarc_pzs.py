import json
import os
import subprocess


INPUT = 'json'
OUTPUT = 'tweets'


if not os.path.exists(OUTPUT):
    os.makedirs(OUTPUT)


for fn in os.listdir(INPUT):
    name = os.path.splitext(fn)[0]

    if 'all' == name:
        continue

    with open(os.path.join(INPUT, fn), 'r') as f:
        data = json.loads(f.read())

    center = data['center']
    lat = center[1]
    lon = center[0]

    radius = data['radius_miles']

    loc_str = '{},{},{}mi'.format(lat, lon, radius)
    print('{}: using location {}'.format(name, loc_str))

    cmd = ['twarc.py', '--location', loc_str]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    tweets = list(filter(None, p.stdout.split(os.linesep)))

    output_fn = os.path.join(OUTPUT, '{}.json'.format(name))
    with open(output_fn, 'w') as f:
        for tweet in tweets:
            f.write(tweet + '\n')

    print('wrote {} tweet(s)'.format(len(tweets)))
