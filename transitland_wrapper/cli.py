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
@click.option(
    '-p',
    '--per-page',
    required=False,
    default=50,
    show_default=True,
    type=int,
    help='number of results per page')
@click.option(
    '--page-all/--no-page-all',
    is_flag=True,
    default=True,
    show_default=True,
    help='page over all responses')
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
@click.option(
    '-p',
    '--per-page',
    required=False,
    default=50,
    show_default=True,
    type=int,
    help='number of results per page')
@click.option(
    '--page-all/--no-page-all',
    is_flag=True,
    default=True,
    show_default=True,
    help='page over all responses')
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
    '--include-geometry/--no-include-geometry',
    is_flag=True,
    default=True,
    show_default=True,
    help="Include route geometry")
@click.option(
    '-p',
    '--per-page',
    required=False,
    default=50,
    show_default=True,
    type=int,
    help='number of results per page')
@click.option(
    '--page-all/--no-page-all',
    is_flag=True,
    default=True,
    show_default=True,
    help='page over all responses')
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
@click.option(
    '-p',
    '--per-page',
    required=False,
    default=50,
    show_default=True,
    type=int,
    help='number of results per page')
@click.option(
    '--page-all/--no-page-all',
    is_flag=True,
    default=True,
    show_default=True,
    help='page over all responses')
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
    '--active/--no-active',
    is_flag=True,
    default=True,
    show_default=True,
    help='Schedule Stop Pairs from active FeedVersions')
@click.option(
    '-p',
    '--per-page',
    required=False,
    default=50,
    show_default=True,
    type=int,
    help='number of results per page')
@click.option(
    '--page-all/--no-page-all',
    is_flag=True,
    default=True,
    show_default=True,
    help='page over all responses')
def schedule_stop_pairs(**kwargs):
    """Request schedule stop pairs info"""
    kwargs = handle_geometry(**kwargs)
    features_iter = transitland.schedule_stop_pairs(**kwargs)
    write_to_stdout(features_iter)


@click.command()
@click.option(
    '--oid',
    required=False,
    default=None,
    type=str,
    help='a Onestop ID for any type of entity (for example, a stop or an operator)'
)
@click.option(
    '-f',
    '--file',
    required=False,
    default=None,
    type=click.Path(exists=True, file_okay=True, readable=True),
    help='a file with one or more Onestop IDs, with each on their own line.')
def onestop_id(oid, file):
    """Request onestop_id info"""
    if sum(list(map(bool, [oid, file]))) != 1:
        raise ValueError('must provide either oid or file')

    if oid:
        r_iter = transitland.onestop_id(oid)
        for res in r_iter:
            click.echo(json.dumps(res, separators=(',', ':')))

    else:
        with open(file) as f:
            for line in f:
                _id = line.strip()
                r_iter = transitland.onestop_id(oid=_id)
                for res in r_iter:
                    click.echo(json.dumps(res, separators=(',', ':')))


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
main.add_command(onestop_id)

if __name__ == '__main__':
    main()
