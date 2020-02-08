from time import sleep

import requests
from shapely.geometry import asShape
from shapely.prepared import prep

ALLOWED_GEOMETRY_INTERSECTION_TYPES = [
    'Polygon',
    'MultiPolygon',
    'LineString',
    'MultiLineString',
] # yapf: disable


def stops(**kwargs):
    """Request stops info

    Args:
        - geometry: either Point, to search a radius around a point, or a
          Polygon or MultiPolygon, to search for stops within the geometry. If a
          Polygon or MultiPolygon is provided, the search will be done by
          bounding box, and then results will be filtered for intersection.
        - radius: radius in meters to search around, default 100m for Point
          geometries. Not used for Polygon geometries.
        - served_by: search by operator onestop_id or route onestop_id
        - gtfs_id: ID used in a GTFS feed's stops.txt file
    """
    return base(endpoint='stops', **kwargs)


def operators(**kwargs):
    """Request operators info

    Args:
        - geometry: either Point, to search a radius around a point, or a
          Polygon or MultiPolygon, to search for stops within the geometry. If a
          Polygon or MultiPolygon is provided, the search will be done by
          bounding box, and then results will be filtered for intersection.
        - radius: radius in meters to search around, default 100m for Point
          geometries. Not used for Polygon geometries.
        - gtfs_id: ID used in a GTFS feed's agencies.txt file
    """
    return base(endpoint='operators', **kwargs)


def routes(**kwargs):
    """Request routes info

    Args:
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
    """
    return base(endpoint='operators', **kwargs)


def base(
        endpoint,
        operated_by=None,
        gtfs_id=None,
        geometry=None,
        radius=None,
        served_by=[],
        vehicle_type=[],
        include_geometry=True):
    params = {}
    if gtfs_id is not None:
        params['imported_with_gtfs_id'] = True
        params['gtfs_id'] = gtfs_id

    if geometry is not None:
        if geometry.type == 'Point':
            lon, lat = geometry.coords[0][:2]
            params['lon'] = lon
            params['lat'] = lat
            if radius is not None:
                params['r'] = radius

        elif geometry.type in ALLOWED_GEOMETRY_INTERSECTION_TYPES:
            params['bbox'] = ','.join(map(str, geometry.bounds))

        else:
            msg = f'Geometry type must be one of {ALLOWED_GEOMETRY_INTERSECTION_TYPES}'
            raise ValueError(msg)

    if served_by:
        params['served_by'] = ','.join(served_by)

    if operated_by is not None:
        params['operated_by'] = operated_by

    if vehicle_type:
        params['vehicle_type'] = ','.join(vehicle_type)

    if not include_geometry:
        params['include_geometry'] = False

    features_iter = _request_transit_land(endpoint, params=params)

    if geometry is not None and geometry.type in ALLOWED_GEOMETRY_INTERSECTION_TYPES:
        # "To test one polygon containment against a large batch of points, one
        # should first use the prepared.prep() function"
        prepared_geometry = prep(geometry)
        for features in features_iter:
            kept_features = []
            for feature in features:
                if prepared_geometry.intersects(asShape(feature['geometry'])):
                    kept_features.append(feature)

            yield kept_features
    else:
        return features_iter


def _request_transit_land(endpoint, params=None):
    """Wrapper to transit.land API to page over all results

    Args:
        - url: url to send requests to
        - params: None or dict of params for sending requests

    Returns:
        dict of transit.land output
    """
    allowed_endpoints = ['stops', 'operators', 'routes']
    assert endpoint in allowed_endpoints, 'Invalid endpoint'

    url = f'https://transit.land/api/v1/{endpoint}.geojson'

    # Page over responses if necessary
    # If there are more responses in another page, there will be a 'next'
    # key in the meta with the url to request
    while True:
        r = _send_request(url, params=params)
        d = r.json()

        assert d['type'] == 'FeatureCollection'
        assert set(d.keys()) == {'features', 'meta', 'type'}

        yield d['features']

        # If the 'next' key does not exist, done; so break
        if d['meta'].get('next') is None:
            break

        # Otherwise, keep paging
        url = d['meta']['next']
        params = None


def _send_request(url, params=None):
    """Make request to transit.land API

    Wrapper for requests to transit.land API to stay within rate limit

    You can make 60 requests per minute to the transit.land API, which
    presumably resets after each 60-second period. (It's not per 1-second
    period, because I was able to make 60 requests in like 10 seconds).

    Given this, when I hit r.status_code, I'll sleep for 2 seconds before
    trying again.
    """
    r = requests.get(url, params=params)
    if r.status_code == 429:
        sleep(2)
        return _send_request(url, params=params)

    return r
