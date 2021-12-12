import copy
import json
import sys

ars_dict = {}

def insert_ars(ars_dict, ars, name):
    if ars == '---':
        return ars_dict

    if ars in ars_dict:
        if ars_dict[ars] != name:
            print("Error: duplicate entry:", ars, name)
            sys.exit(0)
    else:
        ars_dict[ars] = name
    return ars_dict

GEOJSON_TEMPLATE = {
  "type": "FeatureCollection",
  "features": []
}

with open('data/wfs_vz250_1231_epsg_4326.geojson') as file:
    data = json.load(file)
    for feature in data['features']:
        # add ars to ars dict
        ars_dict = insert_ars(ars_dict, feature['properties']['ars_g'], feature['properties']['gen_g'] + ' (' + feature['properties']['bez_g'] + ')' )
        ars_dict = insert_ars(ars_dict, feature['properties']['ars_v'], feature['properties']['gen_v'] + ' (' + feature['properties']['bez_v'] + ')' )
        ars_dict = insert_ars(ars_dict, feature['properties']['ars_k'], feature['properties']['gen_k'] + ' (' + feature['properties']['bez_k'] + ')' )
        ars_dict = insert_ars(ars_dict, feature['properties']['ars_r'], feature['properties']['gen_r'] + ' (' + feature['properties']['bez_r'] + ')' )
        ars_dict = insert_ars(ars_dict, feature['properties']['ars_l'], feature['properties']['gen_l'] + ' (' + feature['properties']['bez_l'] + ')' )

        # create geojson file
        if feature['properties']['gf'] != 4: # GF=2 => water area (Baltic See and Lake Constance); GF=4 => land mass
            continue
            # TODO: integrate water areas into land mass geojson files

        # write geojson file for each ars
        geojson = copy.deepcopy(GEOJSON_TEMPLATE)
        geojson['features'] = [feature]

        ars = feature['properties']['ars_g']
        filename = f'web/geojson/{ars}.geojson.json'

        with open(filename, 'w') as f:
            print(f"Writing {filename}")
            f.write(json.dumps(geojson))

# write ars database
filename = 'web/ars_from_geojson.json'
with open(filename, 'w') as f:
    print(f"Writing {filename}")
    f.write(json.dumps(ars_dict))
