import json

import click
from shapely.geometry import box

from . import transitland


@click.group()
def main():
    pass


@click.command()
@click.option(
    '-b',
    '--bbox',
    required=False,
    default=None,
    type=str,
    help='Bounding box to search within')
@click.option(
    '-g',
    '--geometry',
    required=False,
    default=None,
    type=click.Path(exists=True, file_okay=True, readable=True),
    help='File with geometry to use. Must be readable by geopandas')
@click.option(
    '-r',
    '--radius',
    required=False,
    default=None,
    type=float,
    help=
    'radius in meters to search around, default 100m for Point geometries. Used only for Point geometries.'
)
@click.option(
    '--served-by',
    required=False,
    default=None,
    multiple=True,
    type=str,
    help='search by operator onestop_id or route onestop_id')
@click.option(
    '--gtfs-id',
    required=False,
    default=None,
    type=str,
    help="ID used in a GTFS feed's stops.txt file")
def stops(**kwargs):
    """Request stops info"""
    kwargs = handle_geometry(**kwargs)
    features_iter = transitland.stops(**kwargs)
    write_to_stdout(features_iter)


@click.command()
@click.option(
    '-b',
    '--bbox',
    required=False,
    default=None,
    type=str,
    help='Bounding box to search within')
@click.option(
    '-g',
    '--geometry',
    required=False,
    default=None,
    type=click.Path(exists=True, file_okay=True, readable=True),
    help='File with geometry to use. Must be readable by geopandas')
@click.option(
    '-r',
    '--radius',
    required=False,
    default=None,
    type=float,
    help=
    'radius in meters to search around, default 100m for Point geometries. Used only for Point geometries.'
)
@click.option(
    '--gtfs-id',
    required=False,
    default=None,
    type=str,
    help="ID used in a GTFS feed's agencies.txt file")
def operators(**kwargs):
    """Request operators info"""
    kwargs = handle_geometry(**kwargs)
    features_iter = transitland.operators(**kwargs)
    write_to_stdout(features_iter)


@click.command()
@click.option(
    '-b',
    '--bbox',
    required=False,
    default=None,
    type=str,
    help='Bounding box to search within')
@click.option(
    '-g',
    '--geometry',
    required=False,
    default=None,
    type=click.Path(exists=True, file_okay=True, readable=True),
    help='File with geometry to use. Must be readable by geopandas')
@click.option(
    '-r',
    '--radius',
    required=False,
    default=None,
    type=float,
    help=
    'radius in meters to search around, default 100m for Point geometries. Used only for Point geometries.'
)
@click.option(
    '--operated-by',
    required=False,
    default=None,
    type=str,
    help='search by operator onestop_id or route onestop_id')
@click.option(
    '--vehicle-type',
    required=False,
    default=None,
    multiple=True,
    type=str,
    help=
    'find all routes with vehicle type(s) by integer or string. Possible values defined by the GTFS spec for the route_type column and the Extended GTFS Route Types'
)
@click.option(
    '--gtfs-id',
    required=False,
    default=None,
    type=str,
    help="ID used in a GTFS feed's routes.txt file")
@click.option(
    '--include-geometry',
    is_flag=True,
    default=True,
    type=bool,
    help="Include route geometry")
def routes(**kwargs):
    """Request routes info"""
    kwargs = handle_geometry(**kwargs)
    features_iter = transitland.routes(**kwargs)
    write_to_stdout(features_iter)


@click.command()
@click.option(
    '-b',
    '--bbox',
    required=False,
    default=None,
    type=str,
    help='Bounding box to search within')
@click.option(
    '-g',
    '--geometry',
    required=False,
    default=None,
    type=click.Path(exists=True, file_okay=True, readable=True),
    help='File with geometry to use. Must be readable by geopandas')
@click.option(
    '--traversed-by',
    required=False,
    default=None,
    type=str,
    help='find all Route Stop Patterns belonging to route')
@click.option(
    '--stops-visited',
    required=False,
    default=None,
    multiple=True,
    type=str,
    help=
    'any one or more stop Onestop IDs, separated by comma. Finds Route Stop Patterns with stops_visited in stop_pattern'
)
@click.option(
    '--trips',
    required=False,
    default=None,
    multiple=True,
    type=str,
    help=
    'any one or more trip ids, separated by comma. Finds Route Stop Patterns with specified trips in trips'
)
def route_stop_patterns(**kwargs):
    """Request routes info"""
    kwargs = handle_geometry(**kwargs)
    features_iter = transitland.route_stop_patterns(**kwargs)
    write_to_stdout(features_iter)


@click.command()
@click.option(
    '-b',
    '--bbox',
    required=False,
    default=None,
    type=str,
    help='Bounding box to search within')
@click.option(
    '-g',
    '--geometry',
    required=False,
    default=None,
    type=click.Path(exists=True, file_okay=True, readable=True),
    help='File with geometry to use. Must be readable by geopandas')
@click.option(
    '--origin-onestop-id',
    required=False,
    multiple=True,
    default=None,
    type=str,
    help='Find all Schedule Stop Pairs from origin')
@click.option(
    '--destination-onestop-id',
    required=False,
    multiple=True,
    default=None,
    type=str,
    help='Find all Schedule Stop Pairs to a destination')
@click.option(
    '--date',
    required=False,
    default=None,
    type=str,
    help='Find all Schedule Stop Pairs from origin on date')
@click.option(
    '--service-from-date',
    required=False,
    default=None,
    type=str,
    help='Find all Schedule Stop Pairs in effect from a date')
@click.option(
    '--service-before-date',
    required=False,
    default=None,
    type=str,
    help='Find all Schedule Stop Pairs in effect before a date')
@click.option(
    '--origin-departure-between',
    required=False,
    default=None,
    type=str,
    help='Find all Schedule Stop Pairs with origin_departure_time in a range')
@click.option(
    '--trip',
    required=False,
    default=None,
    type=str,
    help='Find all Schedule Stop Pairs by trip identifier')
@click.option(
    '--route-onestop-id',
    required=False,
    multiple=True,
    default=None,
    type=str,
    help='Find all Schedule Stop Pairs by route')
@click.option(
    '--operator-onestop-id',
    required=False,
    multiple=True,
    default=None,
    type=str,
    help='Find all Schedule Stop Pairs by operator')
@click.option(
    '--active',
    is_flag=True,
    default=False,
    type=bool,
    help='Schedule Stop Pairs from active FeedVersions')
def schedule_stop_pairs(**kwargs):
    """Request schedule stop pairs info"""
    kwargs = handle_geometry(**kwargs)
    features_iter = transitland.schedule_stop_pairs(**kwargs)
    write_to_stdout(features_iter)


def handle_geometry(**kwargs):
    bbox = kwargs.pop('bbox')
    geometry_file = kwargs.pop('geometry')

    if sum(list(map(bool, [bbox, geometry_file]))) > 1:
        raise ValueError('must provide either bbox or geometry')

    geometry = None
    if bbox:
        bbox = list(map(float, bbox.split(',')))
        geometry = box(*bbox)
    elif geometry_file:
        geometry = load_file(geometry_file)

    kwargs['geometry'] = geometry
    return kwargs


def load_file(file):
    """Load file into GeoDataFrame
    """
    import geopandas as gpd

    gdf = gpd.read_file(file)
    # Reproject to EPSG 4326
    gdf = gdf.to_crs(epsg=4326)
    # Coalesce into single geometry
    return gdf.unary_union


def write_to_stdout(features_iter):
    """Write features to stdout
    """
    for features in features_iter:
        for feature in features:
            click.echo(json.dumps(feature, separators=(',', ':')))


main.add_command(stops)
main.add_command(operators)
main.add_command(routes)
main.add_command(schedule_stop_pairs)
main.add_command(route_stop_patterns)

if __name__ == '__main__':
    main()
