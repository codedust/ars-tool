#!/bin/bash

SERVICE_NAME='wfs_vz250_1231'
FEATURE_TYPE='vz250_1231:vz250'
EPSG_CRS='4326' # coordinate reference system based on the Earth's center of mass, used by the GPS among others (default coordinate system of leaflet)

DOWNLOAD_URL="https://sgx.geodatenzentrum.de/$SERVICE_NAME?service=WFS&request=GetFeature&version=2.0.0&typeNames=$FEATURE_TYPE&outputFormat=application%2Fjson&srsName=urn:ogc:def:crs:EPSG::$EPSG_CRS&resultType=results"
echo $DOWNLOAD_URL
wget --show-progress -O "data/${SERVICE_NAME}_epsg_${EPSG_CRS}.geojson" $DOWNLOAD_URL
