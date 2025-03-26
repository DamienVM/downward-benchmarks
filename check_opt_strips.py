#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from collections import defaultdict
from pathlib import Path

from suites import suite_optimal_strips

domain_dir_list = suite_optimal_strips()
with open('opt_plan_data.json', 'r') as file:
    opt_data = json.load(file)

missing_domains = set()
missing_tasks = defaultdict(set)

task_count = 0
missing_tasks_count = 0
for domains_dir in domain_dir_list:
    domain = domains_dir
    missing_domain = False
    if domain not in opt_data:
        missing_domains.add(domain)
        missing_domain = True
    domains_dir = Path(domains_dir)
    domain_task_count = 0
    for task in domains_dir.iterdir():
        task = task.name
        if "domain" in task:
            continue
        domain_task_count += 1
        if not missing_domain:
            if task in opt_data[domain]:
                continue
        missing_tasks[domain].add(task)

    print(f"{domain_task_count-len(missing_tasks[domain])}/{domain_task_count}\t| {domain}")
    task_count += domain_task_count
    missing_tasks_count += len(missing_tasks[domain])

print(f"Missing {missing_tasks_count}: {task_count-missing_tasks_count}/{task_count}")

if(missing_tasks_count > 0):
    asw = input("Print missing data? [Y/n]")
    if not asw.capitalize() == "Y":
        exit()

    for domain in missing_domains:
        print(f"Missing domain {domain}")

    for domain in missing_tasks:
        if len(missing_tasks[domain]) == 0:
            continue
        print(f"Domain {domain:}")
        for task in missing_tasks[domain]:
            print(f"\t{task}")

