import os
import subprocess


INPUT = 'tweets'
OUTPUT = 'geojson'


if not os.path.exists(OUTPUT):
    os.makedirs(OUTPUT)


for fn in os.listdir(INPUT):
    name = os.path.splitext(fn)[0]

    input_fn = os.path.join(INPUT, fn)
    output_fn = os.path.join(OUTPUT, '{}.geojson'.format(name))

    print('generating fuzzed geojson for {}'.format(name))
    cmd = ['../twarc/utils/geojson.py', '-c', '-f 0.01', input_fn]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)

    with open(output_fn, 'w') as f:
        f.write(p.stdout)
