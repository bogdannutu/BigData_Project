#!/usr/bin/env python3
"""reducer.py"""

from operator import itemgetter
import sys

locations = {}

for line in sys.stdin:
    line = line.strip()
    country_data = line.split('\t')

    country = country_data[0]

    deaths = country_data[1]
    cases = country_data[2:]

    cases_today = cases[-1]

    cases_month = 0
    for case in cases:
        try:
            cases_month += float(case)
        except ValueError:
            continue

    print(country + "," + cases_today + "," + str(cases_month) + "," + deaths)
