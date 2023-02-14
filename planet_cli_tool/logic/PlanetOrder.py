import time
import aiohttp
import os
import pathlib


class PlanetOrder():

    def __init__(self, apyKey: str, ids=[]):
        self.ids = ids
        self.__endpoint = "https://api.planet.com/compute/ops/orders/v2"
        self.apiKey = apyKey
        self.session = self.__create_session__()

    async def create_order(self):
        # Parameters
        headers = {'content-type': 'application/json'}
        body = self.__get_body__()

        # Http transaction
        async with aiohttp.ClientSession(
            auth=aiohttp.BasicAuth(self.apiKey, " ")
        ) as session:
            async with session.post(
                 self.__endpoint, data=body, headers=headers
            ) as response:
                order_id = response.json()['id']
                return order_id

    def __get_body__(self):
        request = {
            "name": "Order Planet Tool",
            "products": [
                {
                    "item_ids": self.ids,
                    "item_type": "PSScene",
                    "product_bundle": "visual"
                }
            ],
        }
        return request

    async def download_order(self, order_id):

        order_url = f"{self.__endpoint}/{order_id}"
        timeout = 300

        while timeout > 0:
            async with aiohttp.ClientSession(
                auth=aiohttp.BasicAuth(self.apiKey, " ")
            ) as session:
                async with session.get(
                    order_url
                ) as response:
                    r = response.json()
                    state = r['state']
                    end_states = ['success', 'failed']
                    if state in end_states:
                        if state == "sucess":
                            results = r['_links']['results']
                            return results
                        break
                    timeout -= 5
                    time.sleep(5)

        if timeout == 0:
            raise Exception('Your order is not ready')
