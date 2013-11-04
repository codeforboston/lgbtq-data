#!/usr/bin/python

import sys, json
from collections import OrderedDict

ORDERED_KEYS = ["organization_name",
    #"address",
    #"unit_number",
    #"county",
    #"state",
    #"zipcode",
    "community",
    "services_offered",
    "web_url",
    "phone_numbers",
    "contact_names",
    "contact_emails",
    "service_classes",
    "target_populations",
    "age_range",
    "additional_notes"]

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
        full_address += d["county"] + ", " + d["state"] + " " + d["zipcode"]
        properties["address"] = full_address

        # other properties
        for key in ORDERED_KEYS:
          properties[key] = d[key]

        # format full feature object
        feature = OrderedDict()
        feature["type"] = "Feature"
        feature["geometry"] = geometry
        feature["properties"] = properties

        features.append(feature)

    collection = OrderedDict()
    collection["type"] = "FeatureCollection"
    collection["features"] = features

    out.write(json.dumps(collection))

  else:
    print "./json_to_json.py input.json output.geojson"


