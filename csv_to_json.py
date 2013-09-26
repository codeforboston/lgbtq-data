#!/usr/bin/python

# To convert Geomapping...xls
# Export as .csv with a , separator
# run ./csv_to_json.py Geomapping...csv output.json
# or
# run ./csv_to_json.py Geomapping...csv output.json --geocode


# Data formats:
# .xls
#   Organization Name
#   Address
#   Unit Number
#   Community
#   State
#   Zip Code
#   County
#   Services Offered 1...9
#   Website URL
#   Phone Number
#   Contact Name 1
#   Contact Email 1
#   Contact Name 2
#   Contact Email 2
#   Service Class 1...3
#   Target Population 1...3
#   Age Range
#   Additional Notes
#
# .json
# { locations: [
#     { organization_name: "String",
#       address: "String",
#       unit_number: "String",
#       community: "String,
#       state: "String",
#       zipcode: "String", #yes, a string
#       county: "String",
#       services_offered: ["String"],
#       website_url: "String",
#       phone_numbers: ["String"],
#       contact_names: ["String"],
#       contact_emails: ["String"],
#       target_populations: ["String"],
#       age_range: "String", #worth splitting into lower/upper bound?
#       notes: ["String"]
#       loc: {lat: Number, lng, Number}
#     }
#   ]
# }

import sys, json, csv, time
from geopy import geocoders
geocoder = geocoders.GoogleV3()

def parse(f, geocode=False):
  locations = []

  reader = csv.reader(f)
  for i, row in enumerate(reader):
    if i > 0:
      org = row[0]
      address = row[1]
      unit_num = row[2]
      community = row[3]
      state = row[4]
      zipcode = row[5]
      county = row[6]
      services = filter_out_empty(row[7:15])
      url = row[16]
      phones = [row[17]]
      names = filter_out_empty([row[18], row[20]])
      emails = filter_out_empty([row[19], row[21]])
      service_classes = filter_out_empty(row[22:24])
      target_populations = filter_out_empty(row[25:27])
      age_range = row[28]
      notes = filter_out_empty(row[29:])

      loc = {
          "organization_name": org,
          "address": address,
          "unit_number": unit_num,
          "community": community,
          "state": state,
          "zipcode": zipcode,
          "county": county,
          "services_offered": services,
          "web_url": url,
          "phone_numbers": expand_all(phones),
          "contact_names": expand_all(names),
          "contact_emails": expand_all(emails),
          "service_classes": service_classes,
          "target_populations": target_populations,
          "age_range": age_range,
          "additional_notes": notes
        }

                      #empty string is false-y
      if (geocode and address and county and state): 
        time.sleep(1) #rate limit
        try:
          full_address = address + "\n" + county + ", " + state +  " " + zipcode
          place, (lat, lng) = geocoder.geocode(full_address)
          loc["lat"] = lat
          loc["lng"] = lng
          print "~~~Geocoded"
          print full_address
          print (lat, lng)
        except Exception as ex:
          print "~~~failed to geocode"
          print full_address
          print ex
        sys.stdout.flush()

      locations.append(loc)
  return locations

# takes a list with "" and nulls in some fields
# returns a shortened list with only good data
def filter_out_empty(l):
  return filter(lambda x: x != None and x != "", l)

# takes a lit of strings, ["a", "b", "c;d;e"]
# splits any elements separated by semicolons
# -> ["a", "b", "c", "d", "e"]
def expand_all(l):
  new = []
  for element in l:
    if ';' in element:
      new += map(lambda x: x.strip(), element.split(';'))
    else:
      new.append(element)
  return new


if __name__ == "__main__":
  if len(sys.argv) >= 3:
    inp = open(sys.argv[1], 'r')
    out = open(sys.argv[2], 'w')

    g = False
    if (len(sys.argv) >= 4 and sys.argv[3] == "--geocode"):
      g=True

    data = parse(inp, geocode=g)
    j = json.dumps(data, indent=2)
    out.write(j)

    inp.close()
    out.close()
  else:
    print "./csv_to_json.py input.csv output.json"

