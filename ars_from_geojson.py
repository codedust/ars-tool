import copy
import json
import sys
from pyproj import Transformer

transformer = Transformer.from_crs("epsg:25832", "epsg:4326")
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

with open('data/wfs_vz250_1231.geojson') as file:
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

        geojson = copy.deepcopy(GEOJSON_TEMPLATE)
        geojson['features'] = [feature]
        ars = feature['properties']['ars_g']

        assert len(geojson['features']) == 1

        for i, polygon_coordinate_array in enumerate(geojson['features'][0]['geometry']['coordinates']):
            for j, linear_ring_coordinate_array in enumerate(polygon_coordinate_array):
                geojson['features'][0]['geometry']['coordinates'][i][j] = list(map(lambda x: transformer.transform(x[0], x[1])[::-1], geojson['features'][0]['geometry']['coordinates'][i][j]))

        assert len(geojson['features'][0]['bbox']) == 4
        bbox = geojson['features'][0]['bbox']
        geojson['features'][0]['bbox'] = transformer.transform(bbox[0], bbox[1])[::-1] + transformer.transform(bbox[2], bbox[3])[::-1]

        filename = f'web/geojson/{ars}.geojson.json'
        with open(filename, 'w') as f:
            print(f"Writing {filename}")
            f.write(json.dumps(geojson))

filename = 'web/ars_from_geojson.json'
with open(filename, 'w') as f:
    print(f"Writing {filename}")
    f.write(json.dumps(ars_dict))
