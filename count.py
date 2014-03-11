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

all_service_classes = {}
all_target_populations = {}
all_services_offered = {}

for item in data["features"]:
  d = item['properties']
  for sc in d.get("service_classes"):
    add_to_map(all_service_classes, sc)
  for tp in d.get("target_populations"):
    add_to_map(all_target_populations, tp)
  for so in d.get("services_offered"):
    add_to_map(all_services_offered, so)

print "\nSERVICE CLASSES"
print_alphabetic(all_service_classes)

print "\nTARGET POPULATIONS"
print_alphabetic(all_target_populations)

print "\nSERVICES OFFERED"
print_alphabetic(all_services_offered)


