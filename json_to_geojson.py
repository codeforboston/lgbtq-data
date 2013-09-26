#!/usr/bin/python

import sys, json
from collections import OrderedDict

if __name__ == "__main__":
  if len(sys.argv) == 3:
    inp = open(sys.argv[1], 'r')
    out = open(sys.argv[2], 'w')

    data = json.loads("".join(inp.readlines()))
    features = []

    for d in data:
      if "lat" in d.keys() and "lng" in d.keys():

        geometry = OrderedDict()
        geometry["type"] = "Point"
        geometry["coordinates"] = [d["lng"], d["lat"]]

        properties = OrderedDict()
        for key in d.keys():
          if key != "lat" and key != "lng":
            properties[key] = d[key]

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


