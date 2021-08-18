from typing import Optional

import aiohttp
import async_timeout


async def make_request(
    url: str,
    method: str,
    query: Optional[dict] = None,
    data: Optional[dict] = None,
    timeout: int = 60,
):

    if not data:
        data = {}

    if not query:
        query = {}

    with async_timeout.timeout(timeout=timeout):
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method=method, url=url, params=query, data=data) as response:
                data = await response.json()
                return data, response.status, response.headers
