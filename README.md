# Transit.land API wrapper

Simple Python wrapper around <transit.land> API.

## Install

```
pip install transitland_wrapper
```

## CLI

All CLI commands write a list of GeoJSON `Feature`s to stdout. This way minimal
results are kept in memory at once. If a `geometry` is passed, the geometry's
bounding box is given to the transit.land API, and results are tested for
intersection with the original geometry. The `geometry` file must be readable by
GeoPandas and will automatically be reprojected to EPSG 4326 if necessary. The
geometry type must be either `Point`, `Polygon`, `MultiPolygon`, `LineString`,
or `MultiLineString`.

### Operators

```
Usage: transitland operators [OPTIONS]

  Request operators info

Options:
  -b, --bbox TEXT      Bounding box to search within
  -g, --geometry PATH  File with geometry to use. Must be readable by
                       geopandas
  -r, --radius FLOAT   radius in meters to search around, default 100m for
                       Point geometries. Used only for Point geometries.
  --gtfs-id TEXT       ID used in a GTFS feed's agencies.txt file
  --help               Show this message and exit.
```


### Routes

```
Usage: transitland routes [OPTIONS]

  Request routes info

Options:
  -b, --bbox TEXT      Bounding box to search within
  -g, --geometry PATH  File with geometry to use. Must be readable by
                       geopandas
  -r, --radius FLOAT   radius in meters to search around, default 100m for
                       Point geometries. Used only for Point geometries.
  --operated-by TEXT   search by operator onestop_id or route onestop_id
  --vehicle-type TEXT  find all routes with vehicle type(s) by integer or
                       string. Possible values defined by the GTFS spec for
                       the route_type column and the Extended GTFS Route Types
  --gtfs-id TEXT       ID used in a GTFS feed's routes.txt file
  --include-geometry   Include route geometry
  --help               Show this message and exit.
```

### Stops

```
Usage: transitland stops [OPTIONS]

  Request stops info

Options:
  -b, --bbox TEXT      Bounding box to search within
  -g, --geometry PATH  File with geometry to use. Must be readable by
                       geopandas
  -r, --radius FLOAT   radius in meters to search around, default 100m for
                       Point geometries. Used only for Point geometries.
  --served-by TEXT     search by operator onestop_id or route onestop_id
  --gtfs-id TEXT       ID used in a GTFS feed's stops.txt file
  --help               Show this message and exit.
```

## Python API

```py
import transitland_wrapper
transitland_wrapper.stops()
transitland_wrapper.operators()
transitland_wrapper.routes()
```

### Stops

```
- geometry: either Point, to search a radius around a point, or a
  Polygon or MultiPolygon, to search for stops within the geometry. If a
  Polygon or MultiPolygon is provided, the search will be done by
  bounding box, and then results will be filtered for intersection.
- radius: radius in meters to search around, default 100m for Point
  geometries. Not used for Polygon geometries.
- served_by: search by operator onestop_id or route onestop_id
- gtfs_id: ID used in a GTFS feed's stops.txt file
```

### Operators

```
- geometry: either Point, to search a radius around a point, or a
  Polygon or MultiPolygon, to search for stops within the geometry. If a
  Polygon or MultiPolygon is provided, the search will be done by
  bounding box, and then results will be filtered for intersection.
- radius: radius in meters to search around, default 100m for Point
  geometries. Not used for Polygon geometries.
- gtfs_id: ID used in a GTFS feed's agencies.txt file
```

### Routes

```
- geometry: either Point, to search a radius around a point, or a
  Polygon or MultiPolygon, to search for stops within the geometry. If a
  Polygon or MultiPolygon is provided, the search will be done by
  bounding box, and then results will be filtered for intersection.
- radius: radius in meters to search around, default 100m for Point
  geometries. Not used for Polygon geometries.
- operated_by: search by operator onestop_id
- vehicle_type: find all routes with vehicle type(s) by integer or
  string. Possible values defined by the GTFS spec for the route_type
  column and the Extended GTFS Route Types.
- include_geometry: If True, includes route geometry. Default: True
- gtfs_id: ID used in a GTFS feed's routes.txt file
```
