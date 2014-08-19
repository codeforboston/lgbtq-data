#!/usr/local/bin/python3

# To convert Geomapping...xls
# Export as .csv with a , separator
# run ./csv_to_json.py Geomapping...csv output.json
# or
# run ./csv_to_json.py Geomapping...csv output.json --geocode


# Data formats:
# .csv
#   Organization
#   Search Category 1...6
#   Revised Service Class Level 1 1...5
#   Revised Service Class Level 2 1...7
#   Website URL
#   Address
#   Unit Number
#   Community
#   State
#   Zip Code
#   County
#   Services Offered 1...9
#   Phone Number
#   Contact Name 1
#   Contact Email 1
#   Contact Name 2
#   Contact Email 2
#   Target Population 1...3
#   Age Range
#   Mission Statement
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
#       search_class: ["String"],
#       services_class_1: ["String"],
#       services_class_2: ["String"],
#       website_url: "String",
#       phone_numbers: ["String"],
#       contact_names: ["String"],
#       contact_emails: ["String"],
#       target_populations: ["String"],
#       age_range: "String",
#       notes: ["String"]
#       loc: {lat: Number, lng, Number}
#     }
#   ]
# }

import sys, json, time, codecs
#import unicodecsv as csv
import csv
from geopy import geocoders
from collections import OrderedDict
from pprint import pprint

geocoder = geocoders.GoogleV3()

def parse(f, geocode=False):
  locations = []

  reader = csv.reader(f, delimiter='\t')
  for i, row in enumerate(reader):
    if i > 0:
      #pprint(row)
      org = row[0]

      new_search_class = filter_out_empty(row[1:2])

      search_class = filter_out_empty(row[3:8])
      service_class_L1 = filter_out_empty(row[9:12])
      service_class_L2 = filter_out_empty(row[13:19])

      #idk = filter_out_empty(row[21:23])

      url = row[22]

      address = row[23]
      unit_num = row[24]
      city = row[25]
      state = row[26]
      zipcode = row[27]
      county = row[28]

      phones = [row[29]]
      names = filter_out_empty([row[30]])
      # row 31 name is not for public use
      emails = cleanup_emails(filter_out_empty([row[32]]))
      # row 33 email is not for public use

      target_populations = filter_out_empty(row[34:36])
      min_age = numberify(row[37])
      max_age = numberify(row[38])

      notes = row[39]


      loc = OrderedDict()
      loc["organization_name"] = org
      loc["address"] = address
      loc["unit_number"] = unit_num
      loc["county"] = county
      loc["state"] = state
      loc["zipcode"] = zipcode
      loc["city"] = city
      loc["web_url"] = url
      loc["phone_numbers"] = expand_all(phones)
      loc["contact_names"] = expand_all(names)
      loc["contact_emails"] = expand_all(emails)
      loc["youth_category"] = search_class
      loc["new_search_class"] = new_search_class
      loc["service_class_level_1"] = service_class_L1
      loc["service_class_level_2"] = service_class_L2
      loc["target_populations"] = target_populations
      loc["min_age"] = min_age
      loc["max_age"] = max_age
      loc["additional_notes"] = notes

                      #empty string is false-y
      if (geocode and address and city and state): 
        time.sleep(1) #rate limit
        try:
          full_address = address + "\n" + city + ", " + state +  " " + zipcode
          place, (lat, lng) = geocoder.geocode(full_address)
          loc["lat"] = lat
          loc["lng"] = lng
          print("~~~Geocoded")
          print(full_address)
          print((lat, lng))
        except Exception as ex:
          print("~~~failed to geocode")
          print(full_address)
          print(ex)
        sys.stdout.flush()

      locations.append(loc)
  clean(locations)
  #pprint(locations)
  return locations

def clean(l):
  #pprint("cleaning")
  for element in l:
    for key in element:
      value = element[key]
      if isinstance(value, float):
        pass
      elif isinstance(value, int):
        pass
      elif isinstance(value, str):
        element[key] = value.replace(u'\xa0', u' ') #replace non-breaking space
        #print(("str", value))
      else:
        for i, v in enumerate(value):
          value[i] = v.replace(u'\xa0', u' ')
        #print(("not str", value))

def numberify(n):
  if n is not "":
    return int(n)
  else:
    return float('NaN')

# takes a list with "" and nulls in some fields
# returns a shortened list with only good data
def filter_out_empty(l):
  return list(filter(lambda x: x != None and x != "", l))

def expand_all(l):
  """
  takes a list of strings, ["a", "b", "c;d;e"]
  splits any elements separated by semicolons
  -> ["a", "b", "c", "d", "e"]

  """
  new = []
  for element in l:
    new.extend([x.strip() for x in element.split(';')])
  return new


def cleanup_emails(s):
  """
  Remove any 'mailto:' at the beginning of an email addresses

  Parameters
  ----------
  s: sequence of strings representing email addresses

  Returns
  -------
  Sequence of cleaned up emails

  """
  lookfor = 'mailto:'
  fixed = []
  for email in s:
    if email.startswith(lookfor):
      email = email[len(lookfor):]
    fixed.append(email)

  return fixed
  

'''
def unicode_csv_reader(utf8_data, **kwargs):
  csv_reader = csv.reader(utf8_data, **kwargs)
  for row in csv_reader:
    yield [cell for cell in row]
'''

def main(argv):
  if len(argv) >= 3:
    inp = open(argv[1], 'r')
    out = open(argv[2], 'w')

    g = False
    if (len(argv) >= 4 and argv[3] == "--geocode"):
      g=True

    data = parse(inp, geocode=g)
    j = json.dumps(data, indent=2)
    out.write(j)

    inp.close()
    out.close()
  else:
    print("./csv_to_json.py input.csv output.json")

if __name__ == "__main__":
  import sys
  main(sys.argv)
