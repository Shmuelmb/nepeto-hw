import aiohttp
from typing import Dict, Any
import asyncio


class DataSparkClient:
    def __init__(
            self,
            api_key: str,
            base_url: str = 'https://dataspark.co/api/v1'):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {'api-key': api_key}
        self.default_params = {'low_price_history': 1, 'stats': 1000}

    async def get_product_data(self, item_id: str) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}/product/{item_id}'
            params = self.default_params
            headers = self.headers
            async with session.get(
                url, params=params, headers=headers
            ) as response:
                if response.status != 200:
                    msg = f"API request failed for item {
                        item_id}: {response.status}"
                    raise ValueError(msg)
                return await response.json()

    async def get_bulk_product_data(
            self, item_ids: list[str]) -> list[Dict[str, Any]]:
        tasks = [
            self.get_product_data(item_id.strip())
            for item_id in item_ids
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)
