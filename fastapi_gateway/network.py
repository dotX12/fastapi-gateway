from typing import Optional, Union

import aiohttp
import async_timeout
from aiohttp import JsonPayload

from fastapi_gateway.utils.form import CustomFormData


async def make_request(
    url: str,
    method: str,
    query: Optional[dict] = None,
    data: Union[CustomFormData, JsonPayload] = None,
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
