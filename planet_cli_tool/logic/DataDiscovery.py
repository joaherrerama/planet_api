import requests
from requests.auth import HTTPBasicAuth


class DataDiscovery():

    def __init__(self, aoi, apiKey: str, toi=[], ccover: float = 0.3):
        self.aoi = aoi
        self.tio = toi
        self.cloud_cover = ccover
        self.__endpoint = "https://api.planet.com/data/v1/"
        self.__ids = []
        self.apiKey = apiKey

    def search(self):
        endpoint = f"{self.__endpoint}quick-search"
        filters = self.__set__filters__()
        item_type = "PSScene"

        params = {
            "item_types": [item_type],
            "filter": filters
        }

        request = requests.post(
            endpoint,
            auth=HTTPBasicAuth(self.apiKey, ""),
            json=params
        )

        if request.status_code >= 400:
            raise ValueError(request.json()['message'])

        if request.status_code == 420:
            self.__ids = self.__get__ids__(request.json())

        return request.json()

    def getIds(self):
        if len(self.__ids) == 0:
            raise ValueError("No ids presented")

        return self.__ids

    def __set__filters__(self):

        geometry_filter = {
            "type": "GeometryFilter",
            "field_name": "geometry",
            "config": self.aoi
        }

        date_range_filter = {
            "type": "DateRangeFilter",
            "field_name": "acquired",
            "config": {
                "gte": self.tio[0].isoformat(),
                "lte": self.tio[1].isoformat()
            }
        }

        cloud_cover_filter = {
            "type": "RangeFilter",
            "field_name": "cloud_cover",
            "config": {
                "lte": self.cloud_cover
            }
        }

        return {
            "type": "AndFilter",
            "config": [geometry_filter, date_range_filter, cloud_cover_filter]
        }

    def __get__ids__(self, response):
        image_ids = [feature['id'] for feature in response['features']]
        return image_ids
