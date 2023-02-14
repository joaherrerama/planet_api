import geojson
from dateutil.parser import parse
import rioxarray as rxr
import shapefile
import json


def date_handler(start: str, end: str):
    start_date = parse(start)
    end_date = parse(end)
    if start_date > end_date:
        return [end_date, start_date]
    return [start_date, end_date]


def aio_handler(geom: str):
    if geom.endswith('.geojson'):
        with open(geom) as f:
            return geojson.load(f)
    elif geom.endswith('.shp'):
        return shp_handler(geom)


def shp_handler(geom):
    # read the shapefile
    reader = shapefile.Reader(geom)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(
            dict(type="Feature", geometry=geom, properties=atr)
        )

    # write the GeoJSON file
    return json.dumps(
        {"type": "FeatureCollection", "features": buffer}, indent=2
    )


def clip_and_store(results, aoi, output_folder):
    results_urls = [r['location'] for r in results]
    results_names = [r['name'] for r in results]
    print('{} items to download'.format(len(results_urls)))

    for url, name in zip(results_urls, results_names):
        raster = rxr.open_rasterio(url, masked=True)
        clipped = raster.rio.clip(aoi)
        filePath = f"{output_folder}/{name}.tif"
        clipped.rio.to_raster(
            filePath, compress='LZMA', tiled=True, dtype="int32")
        print(f"Image stored at: {filePath}")
