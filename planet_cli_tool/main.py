import asyncio
import sys
import os
import argparse

from utils.common import aio_handler, date_handler, clip_and_store
from logic.DataDiscovery import DataDiscovery
from logic.PlanetOrder import PlanetOrder


async def main(argv):
    parser = argparse.ArgumentParser(
        description="CLI tool - Planet Imagery Adquisition"
    )
    parser.add_argument(
        "--aoi",
        type=str,
        help="Area of Interes file (Geojson, SHP, WKT)",
        default='test_geojson_file.geojson'
    )
    parser.add_argument(
        "--start-date",
        type=str,
        help="Time of Interset - start date",
        default="2021-01-12"
    )
    parser.add_argument(
        "--end-date",
        type=str,
        help="Time of Interset - end date",
        default="2022-01-12"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="YOUR API KEY",
        default=''
    )

    parser.add_argument(
        "--output-folder",
        type=str,
        help="Results folder - here all imageries are store",
        nargs='?',
        default='.'
    )

    if not argv:
        print("No args provided -  Default Values will be executed")

    await executeCommand(**vars(parser.parse_args(argv)))
    return


async def executeCommand(
        aoi: str, start_date: str, end_date: str,
        api_key: str, output_folder: str):

    if api_key is None:
        raise ValueError("No api key, \
                          please provide your API KEY usinf --api-key API_KEY")

    if output_folder == '.':
        output_folder = os.path.abspath(output_folder)

    if aoi == 'test_geojson_file.geojson':
        filepath = os.path.realpath(os.path.dirname(__file__))
        aoi = filepath + '/assets/test_geojson_file.geojson'

    if os.path.isfile(output_folder):
        raise ValueError('Path is not a folder/directory')

    # Getting geojson object
    aoi_geojson = aio_handler(aoi)

    # get proper datetimes
    toi = date_handler(start_date, end_date)

    # Quick Search Data API
    search = DataDiscovery(aoi_geojson, api_key, toi)
    search.search()

    # Ordering Data
    order = PlanetOrder(api_key, search.getIds())
    order_id = await order.create_order()

    results = await order.download_order(order_id)

    # Clip and Store
    clip_and_store(results, aoi_geojson["features"], output_folder)


if __name__ == "__main__":
    sys.exit(asyncio.run(main(sys.argv[1:])))
