#!/usr/bin/env python

import sys
import json
from subprocess import call

config_file = 'sims.cfg'
cmd = 'pyxis CFG=/sims.cfg LOG=/results/output.log OUTFILE=/results/results ' \
      'OUTDIR=/results azishe'


def write_config(parsed_json):
    print(parsed_json)
    with open('/' + config_file, 'w') as f:
        f.write(parsed_json[config_file])


def parse_args():
    if len(sys.argv) != 2:
        print("usage: %s <json string containing config>")
        print(str(sys.argv))
        sys.exit()

    return json.loads(sys.argv[1])


def run_simulation():
    call(cmd.split())


if __name__ == '__main__':
    parsed = parse_args()
    write_config(parsed)
    run_simulation()
