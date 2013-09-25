#!/usr/bin/python

# To convert Geomapping...xls
# Export as .csv with a , separator
# run ./csv_to_json.py Geomapping...csv output.json

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
#       phone_number: "String",
#       contacts: [ { name: "String",
#                     email: "String" }
#                 ],
#       target_populations: ["String"],
#       age_range: "String", #worth splitting into lower/upper bound?
#       notes: ["String"]
#     }
#   ]
# }

import sys, json, csv

def parse(f):
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
      phone = row[17]
      contact_name1 = row[18]
      contact_email1 = row[19]
      contact_name2 = row[20]
      contact_email2 = row[21]
      service_classes = filter_out_empty(row[22:24])
      target_populations = filter_out_empty(row[25:27])
      age_range = row[28]
      notes = filter_out_empty(row[29:])

      contacts = []

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
          "phone_number": phone,
          "contacts": contacts,
          "service_classes": service_classes,
          "target_populations": target_populations,
          "age_range": age_range,
          "additional_notes": notes
        }

      locations.append(loc)
  return locations

#takes a list with "" and nulls in some fields
# returns a shortened list with only good data
def filter_out_empty(l):
  return filter(lambda x: x != None and x != "", l)


if __name__ == "__main__":
  if len(sys.argv) == 3:
    inp = open(sys.argv[1], 'r')
    out = open(sys.argv[2], 'w')

    data = parse(inp)
    j = json.dumps(data)
    out.write(j)

    inp.close()
    out.close()
  else:
    print "./csv_to_json.py input.csv output.json"

