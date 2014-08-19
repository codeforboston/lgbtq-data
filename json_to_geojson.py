#!/usr/bin/python

import sys, json, re
from collections import OrderedDict

ORDERED_KEYS = ["organization_name",
    #"address",
    #"unit_number",
    #"county",
    #"state",
    #"zipcode",
    #"city",
    "web_url",
    "phone_numbers",
    "contact_names",
    "contact_emails",
    "youth_category",
    "new_search_class",
    "service_class_level_1",
    "service_class_level_2",
    "target_populations",
    #"min_age",
    #"max_age",
    "additional_notes"]

#labels to title case
TITLES = ["city",
          "youth_category",
          "new_search_class",
          "service_class_level_1",
          "service_class_level_2",
          "target_populations"]

articles = ['a', 'an', 'of', 'the', 'is', 'and', 'lgbtq']

def title_case(s):
  word_list = re.split(' ', s)       #re.split behaves as expected

  if word_list[0].isupper():
    final = [word_list[0]]
  else:
    final = [word_list[0].capitalize()]

  for word in word_list[1:]:
    if word in articles: #don't capitalize articles
      final.append(word)
    elif word.isupper(): #don't capitalize acronyms
      print(word)
      final.append(word)
    else:
      final.append(word.capitalize())
  return " ".join(final)

def clean_string(s):
  return title_case(s.strip())

if __name__ == "__main__":
  if len(sys.argv) == 3:
    inp = open(sys.argv[1], 'r')
    out = open(sys.argv[2], 'w')

    data = json.loads("".join(inp.readlines()))
    features = []

    for d in data:
      if "lat" in d.keys() and "lng" in d.keys():

        # geo point
        geometry = OrderedDict()
        geometry["type"] = "Point"
        geometry["coordinates"] = [d["lng"], d["lat"]]

        properties = OrderedDict()

        # address
        full_address = d["address"] + '\n';
        if ("unit_number" in d and d["unit_number"] != ""):
          full_address += d["unit_number"] + '\n'
        full_address += d["city"] + ", " + d["state"] + " " + d["zipcode"]
        properties["address"] = full_address

        # other properties
        for key in ORDERED_KEYS:
          if key in TITLES:
            value = d[key]

            if isinstance(value, str): #single element
              properties[key] = clean_string(value)
            else: #list
              properties[key] = [clean_string(v) for v in value]
          else:
            properties[key] = d[key] #just do a normal assignment

        # format full feature object
        feature = OrderedDict()
        feature["type"] = "Feature"
        feature["geometry"] = geometry
        feature["properties"] = properties

        features.append(feature)

    collection = OrderedDict()
    collection["type"] = "FeatureCollection"
    collection["features"] = features

    out.write(json.dumps(collection, indent=2))

  else:
    print("./json_to_json.py input.json output.geojson")


