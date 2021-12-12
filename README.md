<!--
SPDX-FileCopyrightText: 2021 codedust

SPDX-License-Identifier: EUPL-1.2
-->

# ARS-Tool

Simple tool to explore [Amtliche Regionalschlüssel (ARS)](https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/_inhalt.html) of German regions.
A live version of this tool can be found [here](https://www.opengovtech.de/ars/).

## Update geojson shapes
First, download geojson data by executing the `download_geojson.sh` script:

```console
$ chmod +x ./download_geojson.sh
$ ./download_geojson.sh
```


Next, update `web/ars_from_geojson.json` and all geojson files in `web/geojson/` by executing the `ars_from_geojson.py` script:

```console
$ poetry install
$ poetry run python convert_vz250.py
```

## Serving static contents
The contents of the 'web/' directory can now be statically served.

```console
$ cd web
$ python -m http.server
```

## License
Licensed under the [EUPL](./LICENSE.txt).
