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

### Route Stop Patterns

```
Usage: transitland route-stop-patterns [OPTIONS]

  Request routes info

Options:
  -b, --bbox TEXT       Bounding box to search within
  -g, --geometry PATH   File with geometry to use. Must be readable by
                        geopandas
  --traversed-by TEXT   find all Route Stop Patterns belonging to route
  --stops-visited TEXT  any one or more stop Onestop IDs, separated by comma.
                        Finds Route Stop Patterns with stops_visited in
                        stop_pattern
  --trips TEXT          any one or more trip ids, separated by comma. Finds
                        Route Stop Patterns with specified trips in trips
  --help                Show this message and exit.
```

### Schedule Stop Pairs

```
Usage: transitland schedule-stop-pairs [OPTIONS]

  Request schedule stop pairs info

Options:
  -b, --bbox TEXT                 Bounding box to search within
  -g, --geometry PATH             File with geometry to use. Must be readable
                                  by geopandas
  --origin-onestop-id TEXT        Find all Schedule Stop Pairs from origin
  --destination-onestop-id TEXT   Find all Schedule Stop Pairs to a
                                  destination
  --date TEXT                     Find all Schedule Stop Pairs from origin on
                                  date
  --service-from-date TEXT        Find all Schedule Stop Pairs in effect from
                                  a date
  --service-before-date TEXT      Find all Schedule Stop Pairs in effect
                                  before a date
  --origin-departure-between TEXT
                                  Find all Schedule Stop Pairs with
                                  origin_departure_time in a range
  --trip TEXT                     Find all Schedule Stop Pairs by trip
                                  identifier
  --route-onestop-id TEXT         Find all Schedule Stop Pairs by route
  --operator-onestop-id TEXT      Find all Schedule Stop Pairs by operator
  --active                        Schedule Stop Pairs from active FeedVersions
  --help                          Show this message and exit.
```

### Onestop ID

```
Usage: transitland onestop-id [OPTIONS]

Options:
  --oid TEXT       a Onestop ID for any type of entity (for example, a stop or
                   an operator)
  -f, --file PATH  a file with one or more Onestop IDs, with each on their own
                   line.
  --help           Show this message and exit.
```

## Python API

Each function returns a _generator_ of results, because there could be an
unknown amount of paging involved. Each item of the iterator is a list of
GeoJSON `Feature`s.

```py
import transitland_wrapper
transitland_wrapper.stops()
transitland_wrapper.operators()
transitland_wrapper.routes()
transitland_wrapper.route_stop_patterns()
transitland_wrapper.schedule_stop_pairs()
transitland_wrapper.onestop_id()
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

### Route Stop Patterns

```
- geometry: either Polygon or MultiPolygon, to search for stops within
  the geometry. If a Polygon or MultiPolygon is provided, the search
  will be done by bounding box, and then results will be filtered for
  intersection.
- traversed_by: find all Route Stop Patterns belonging to route
- stops_visited: any one or more stop Onestop IDs, separated by comma. Finds Route Stop Patterns with stops_visited in stop_pattern.
- trips: any one or more trip ids, separated by comma. Finds Route Stop Patterns with specified trips in trips.
```

### Schedule Stop Pairs

```
- geometry: either Polygon or MultiPolygon, to search for stops within
  the geometry. If a Polygon or MultiPolygon is provided, the search
  will be done by bounding box, and then results will be filtered for
  intersection.
- origin_onestop_id: Find all Schedule Stop Pairs from origin. Accepts multiple Onestop IDs, separated by commas
- destination_onestop_id: Find all Schedule Stop Pairs to a destination. Accepts multiple Onestop IDs, separated by commas
- date: Find all Schedule Stop Pairs from origin on date
- service_from_date: Find all Schedule Stop Pairs in effect from a date
- service_before_date: Find all Schedule Stop Pairs in effect before a date
- origin_departure_between: Find all Schedule Stop Pairs with origin_departure_time in a range
- trip: Find all Schedule Stop Pairs by trip identifier
- route_onestop_id: Find all Schedule Stop Pairs by route. Accepts multiple Onestop IDs, separated by commas.
- operator_onestop_id: Find all Schedule Stop Pairs by operator. Accepts multiple Onestop IDs, separated by commas.
- active: Schedule Stop Pairs from active FeedVersions
```

### Onestop ID

```
- oid: a Onestop ID for any type of entity (for example, a stop or an operator)
```


## Contributing

To release to PyPI:
```
bumpversion minor
python setup.py sdist
twine upload dist/transitland_wrapper-0.1.0.tar.gz
```
