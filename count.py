#!/usr/bin/python

import sys, json
from pprint import pprint


def add_to_map(m, item):
  if item in m.keys():
    m[item] += 1
  else:
    m[item] = 1

def print_alphabetic(m):
  for key, value in sorted(m.items(), cmp=compare_keys):
    print key, m[key]

def compare_keys(x, y):
  if (x[1] > y[1]):
    return -1
  if (x[1] < y[1]):
    return 1
  else:
    if (x[0] > y[0]):
      return -1
    if (x[0] < y[0]):
      return 1
    else:
      return 0


#main

inp = open("data.geojson")
data = json.loads("".join(inp.readlines()))

service_class = {}
all_target_populations = {}
youth_category = {}

for item in data["features"]:
  d = item['properties']
  for sc in d.get("service_class_level_2"):
    add_to_map(service_class, sc)
  for tp in d.get("target_populations"):
    add_to_map(all_target_populations, tp)
  for so in d.get("youth_category"):
    add_to_map(youth_category, so)

print "\nSSERVICE CLASS"
print_alphabetic(service_class)

print "\nTARGET POPULATIONS"
print_alphabetic(all_target_populations)

print "\nYOUTH CATEGORY"
print_alphabetic(youth_category)


