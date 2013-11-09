lgbtq-data
==========

Data for the MA Commission for LGBTQ


The workflow for converting the Cambridge data from an excel file into a usable geojson format.

Steps:
* resource.xlsx, save as a .csv file, comma and newline seperated
* ./csv_to_json.py file.csv output.json --geocode
* ./json_to_geojson output.json data.geojson
