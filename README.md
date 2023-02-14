# Planet CLI tool

## Getting started

This Command Line Interface (CLI) tool allows the user to access Planet images with just 3 elements: Area of interest (aoi), Time of interest (toi), and the Planet API_KEY. Additionally, it allows the user to configure the output folder.

This tool works on different geometries in GEOJSON and Shapefile formats. The acquired images belong to visual-type items, which have 3 bands and are of the asset type ortho_visual.

The result of this tool concerns images of the selected toi, with a crop to the boundaries of the aoi.

## Pre-requirments

This library has several dependencies listed in the requirements.txt file. It requires a Python version >= 3.9 and an API key with access permissions to the Data API and ORDER API. If the user does not have complete access to these APIs, the program may fail.

## Execution

```
python planet_cli_tool/main.py --help
```
```
usage: main.py [-h] [--aoi AOI] [--start-date START_DATE] [--end-date END_DATE] [--api-key API_KEY] [--output-folder [OUTPUT_FOLDER]]

CLI tool - Planet Imagery Adquisition

optional arguments:
  -h, --help            show this help message and exit
  --aoi AOI             Area of Interes file (Geojson, SHP)
  --start-date START_DATE
                        Time of Interset - start date
  --end-date END_DATE   Time of Interset - end date
  --api-key API_KEY     YOUR API KEY
  --output-folder [OUTPUT_FOLDER]
```
### Example

```
python planet_cli_tool/main.py --aoi path_dir/myfile.shp --start-date 2021-01-01 --end-date 2021-12-01 --api-key MY_API_KEY --outpot-folder path_to_my_output_folder
```

### Arguments

-  **--aoi:** Area de interes en formato Geojson o Shapefile
-  **--start-date:** Tiempo inicial del toi (formato %Y-%m-%d)
-  **--end-date:** Tiempo final del toi de  (formato %Y-%m-%d)
-  **--output-folder:** Carpeta de salida para los archivos recortados (optional)

### Default values

-  **--aoi:** `./assets/test_geojson_file.geojson`
-  **--start-date:** `2021-01-12`
-  **--end-date:** `2021-01-12`
-  **--output-folder:** `./`

### Resources

- https://developers.planet.com/docs/apis/data/reference/#tag/Item-Search/operation/QuickSearch
- https://developers.planet.com/apis/orders/scenes/
- https://corteva.github.io/rioxarray/stable/readme.html


## Test and Deploy

## Limitation

To execute this CLI, the API key must have the appropriate permissions for the acquisition and execution of orders. This CLI runs a full-type order, so it is required that:

- The requester has permissions to access any of the required asset_types in the product_bundle
- The requester has permissions to access any of the order’s specified item_types
- The requester has permissions to access any of the specified item_ids due to geometry or time of interest policy restrictions

The CLI reach just an specifict type of images following these parameters:

- Item type is PSScene
- Asset type is ortho_visual
- Product bundle (for order) is visual


## Next Steps

- Allow for more input formats for the aoi, as well as expanding to acquire different types of images.

- The unique testing trials are in the early stages and need to be developed to evaluate functionality.

- Further development of the `toi_handler` and `aoi_handler` functions.

- Optimization of image acquisition, including the development of asynchronous processes for downloading and cropping.

- Reduce model complexity and consider the orientation of the CLI and its scalability to make better development decisions.

- Allow users to route a folder with multiple file and discriminate them, emulating a batch process.

- Use the stup tool to distribute and create the wheel and dist. Currently the CLI requires the python command to be executed

# Disclamer

Due to the lack of an API key, the logic of this CLI is based solely on the documentation for the Data API and ORDER API. The program is expose to a funtional fail due to the lack of testing. 