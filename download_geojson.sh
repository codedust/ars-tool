#!/bin/bash

SERVICE_NAME='wfs_vz250_1231'
DOWNLOAD_URL="https://sgx.geodatenzentrum.de/$SERVICE_NAME?service=WFS&request=GetFeature&version=2.0.0&typeNames=vz250_1231%3Avz250&outputFormat=application%2Fjson&resultType=results"

wget --show-progress -O "data/$SERVICE_NAME.geojson" $DOWNLOAD_URL
