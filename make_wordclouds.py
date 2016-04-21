import os
import subprocess


INPUT = 'tweets'
OUTPUT = 'wordclouds'


if not os.path.exists(OUTPUT):
    os.makedirs(OUTPUT)


for fn in os.listdir(INPUT):
    name = os.path.splitext(fn)[0]

    input_fn = os.path.join(INPUT, fn)
    output_fn = os.path.join(OUTPUT, '{}.html'.format(name))

    print('generating wordcloud for {}'.format(name))
    cmd = ['../twarc/utils/wordcloud.py', input_fn]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)

    with open(output_fn, 'w') as f:
        f.write(p.stdout)
