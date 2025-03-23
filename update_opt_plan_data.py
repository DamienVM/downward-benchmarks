#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("properties", type=str, help="properties in json format")
args = parser.parse_args()

exit_code = 0
with open('opt_plan_data.json', 'r') as file:
    data = json.load(file)

with open(args.properties, 'r') as file:
    new_data = json.load(file)

are_changes = False
for run in new_data:
    run_id = new_data[run]["id"]
    domain = run_id[1]
    task = run_id[2]

    if new_data[run]["coverage"] == 1:
        opt_cost = int(new_data[run]["cost"])
        opt_plan_length = new_data[run]["plan_length"]

        if domain not in data:
            data[domain] = dict()
        else:
            if task in data[domain]:
                if not data[domain][task]["opt_cost"] == opt_cost:
                    print(f"WARNING: optimal cost are not the same for {domain}:{task}")
                    exit_code = 1
                continue
        are_changes = True
        print(f"New task {domain}:{task}")
        data[domain][task] = dict()
        data[domain][task]["opt_cost"] = opt_cost
        data[domain][task]["opt_plan_length"] = opt_plan_length

if are_changes:
    if input("\nDo you wish to update the data? [Y,n]").capitalize() == 'Y':
        with open('opt_plan_data.json', 'w') as file:
            file.write(json.dumps(data, indent=4))
        print("New data written to opt_plan_data.json")

else:
    print("Nothing new")

exit(exit_code)
