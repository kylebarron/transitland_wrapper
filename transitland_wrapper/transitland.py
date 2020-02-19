import sys
from collections.abc import Iterable
from datetime import datetime
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

ALL_ENDPOINT_TYPES = {
    'stops': '.geojson',
    'operators': '.geojson',
    'routes': '.geojson',
    'route_stop_patterns': '.geojson',
    'schedule_stop_pairs': '',
    'onestop_id': '',
}


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
        - per_page: number of results per page, by default 50
        - page_all: page over all responses
    """
    allowed_keys = [
        'geometry', 'radius', 'served_by', 'gtfs_id', 'per_page', 'page_all'
    ]
    if any(k not in allowed_keys for k in kwargs.keys()):
        msg = f'invalid parameter; allowed parameters are:\n{allowed_keys}'
        raise ValueError(msg)
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
        - per_page: number of results per page, by default 50
        - page_all: page over all responses
    """
    allowed_keys = ['geometry', 'radius', 'gtfs_id', 'per_page', 'page_all']
    if any(k not in allowed_keys for k in kwargs.keys()):
        msg = f'invalid parameter; allowed parameters are:\n{allowed_keys}'
        raise ValueError(msg)

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
        - per_page: number of results per page, by default 50
        - page_all: page over all responses
    """
    allowed_keys = [
        'geometry',
        'radius',
        'operated_by',
        'vehicle_type',
        'include_geometry',
        'gtfs_id',
        'per_page',
        'page_all',
    ]
    if any(k not in allowed_keys for k in kwargs.keys()):
        msg = f'invalid parameter; allowed parameters are:\n{allowed_keys}'
        raise ValueError(msg)

    return base(endpoint='routes', **kwargs)


def route_stop_patterns(**kwargs):
    """Request route_stop_pattern info

    Args:
        - geometry: either Polygon or MultiPolygon, to search for stops within
          the geometry. If a Polygon or MultiPolygon is provided, the search
          will be done by bounding box, and then results will be filtered for
          intersection.
        - traversed_by: find all Route Stop Patterns belonging to route
        - stops_visited: any one or more stop Onestop IDs, separated by comma. Finds Route Stop Patterns with stops_visited in stop_pattern.
        - trips: any one or more trip ids, separated by comma. Finds Route Stop Patterns with specified trips in trips.
        - per_page: number of results per page, by default 50
        - page_all: page over all responses
    """
    allowed_keys = [
        'geometry',
        'traversed_by',
        'stops_visited',
        'trips',
        'per_page',
        'page_all',
    ]
    if any(k not in allowed_keys for k in kwargs.keys()):
        msg = f'invalid parameter; allowed parameters are:\n{allowed_keys}'
        raise ValueError(msg)

    return base(endpoint='route_stop_patterns', **kwargs)


def schedule_stop_pairs(**kwargs):
    """Request schedule_stop_pairs info

    Args:
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
        - per_page: number of results per page, by default 50
        - page_all: page over all responses
    """
    allowed_keys = [
        'geometry',
        'origin_onestop_id',
        'destination_onestop_id',
        'date',
        'service_from_date',
        'service_before_date',
        'origin_departure_between',
        'trip',
        'route_onestop_id',
        'operator_onestop_id',
        'active',
        'per_page',
        'page_all',
    ]
    if any(k not in allowed_keys for k in kwargs.keys()):
        msg = f'invalid parameter; allowed parameters are:\n{allowed_keys}'
        raise ValueError(msg)

    # Validate dates
    date_keys = ['date', 'service_from_date', 'service_before_date']
    for key, val in kwargs.items():
        if key in date_keys:
            if val:
                validate_date(val)

    return base(endpoint='schedule_stop_pairs', **kwargs)


def onestop_id(oid):
    """Request onestop_id info

    Args:
        - oid: a Onestop ID for any type of entity (for example, a stop or an
          operator)
    """
    return _request_transit_land('onestop_id', params={'id': oid})


def base(
        endpoint,
        gtfs_id=None,
        geometry=None,
        radius=None,
        include_geometry=True,
        active=False,
        per_page=50,
        page_all=True,
        **kwargs):
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

    if not include_geometry:
        params['include_geometry'] = False

    if active:
        params['active'] = True

    # 50 is default pagination
    if per_page != 50:
        params['per_page'] = per_page

    for key, value in kwargs.items():
        if key:
            if isinstance(value, str):
                params[key] = value
            elif isinstance(value, Iterable):
                params[key] = ','.join(value)
            else:
                params[key] = value

    features_iter = _request_transit_land(
        endpoint, params=params, page_all=page_all)

    endpoint_type = ALL_ENDPOINT_TYPES[endpoint]
    if ((endpoint_type == '.geojson') and (geometry is not None)
            and (geometry.type in ALLOWED_GEOMETRY_INTERSECTION_TYPES)):
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
        # Not sure why, but this works and just
        # return features_iter
        # didn't actually go through the iterator?
        for x in features_iter:
            yield x


def _request_transit_land(endpoint, params=None, page_all=True):
    """Wrapper to transit.land API to page over all results

    Args:
        - endpoint: endpoint to send requests to
        - params: None or dict of params for sending requests
        - page_all: page over all responses

    Returns:
        dict of transit.land output
    """
    assert endpoint in ALL_ENDPOINT_TYPES.keys(), 'Invalid endpoint'
    endpoint_type = ALL_ENDPOINT_TYPES[endpoint]
    if endpoint == 'onestop_id':
        url = f'https://transit.land/api/v1/{endpoint}/{params["id"]}'
    else:
        url = f'https://transit.land/api/v1/{endpoint}{endpoint_type}'

    # Page over responses if necessary
    # If there are more responses in another page, there will be a 'next'
    # key in the meta with the url to request
    while True:
        r = _send_request(url, params=params)
        d = r.json()

        if endpoint_type == '.geojson':
            assert d['type'] == 'FeatureCollection'
            assert set(d.keys()) == {'features', 'meta', 'type'}
            yield d['features']
        elif endpoint == 'onestop_id':
            yield d
            break
        else:
            assert set(d.keys()) == {endpoint, 'meta'}
            yield d[endpoint]

        if not page_all:
            break

        # If the 'next' key does not exist, done; so break
        if d['meta'].get('next') is None:
            break

        # Otherwise, keep paging
        url = d['meta']['next']
        params = None


def _send_request(url, params=None, sleep_time=2):
    """Make request to transit.land API

    Wrapper for requests to transit.land API to stay within rate limit

    You can make 60 requests per minute to the transit.land API, which
    presumably resets after each 60-second period. (It's not per 1-second
    period, because I was able to make 60 requests in like 10 seconds).

    Given this, when I hit r.status_code, I'll sleep for 2 seconds before
    trying again.
    """
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return r

    elif r.status_code == 429:
        sleep(sleep_time)
        return _send_request(url, params=params)

    else:
        print(f'returned with status code: {r.status_code}', file=sys.stderr)
        print(f'url: {url}', file=sys.stderr)
        if params is not None:
            print(f'params: {params}', file=sys.stderr)

        sleep(sleep_time)
        return _send_request(url, params=params)

    return r


def validate_date(date_text):
    """Validate dates to be YYYY-MM-DD
    """
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")
