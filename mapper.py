#!/usr/bin/env python3
"""mapper.py"""

import sys
from datetime import datetime

current_year = datetime.now().strftime('%Y')
current_month = datetime.now().strftime('%m')
current_day = datetime.now().strftime('%d')

locations = {}

for line in sys.stdin:
    line = line.strip()
    country_data = line.split(',')

    country = country_data[2]
    if country not in locations:
        locations[country] = {}

    date = country_data[3]

    date = date.split('-')
    year = date[0]
    month = date[1]
    day = date[2]

    if year == current_year and month == current_month:
        new_cases = country_data[5]
        if "cases" not in locations[country]:
            locations[country]["cases"] = []

        if not new_cases:
            new_cases = "0.0"

        locations[country]["cases"].append(new_cases)

        if day == current_day:
            total_deaths = country_data[7]
            if not total_deaths:
                total_deaths = "0.0"
            locations[country]["deaths"] = total_deaths

locations.pop("World", None)
for key in locations:
    cases = ["0.0"]
    deaths = "\t0.0"

    if "cases" in locations[key]:
        cases = locations[key]["cases"]

    if "deaths" in locations[key]:
        deaths = "\t" + locations[key]["deaths"]

    cases_str = ""
    for case in cases:
        cases_str += "\t" + case

    print(key + deaths + cases_str)
