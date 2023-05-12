import ujson
from fastapi.routing import serialize_response
from typing import Dict, List, Optional, Any
from aiohttp import JsonPayload


async def unzip_body_object(
    all_params: Dict[str, Any],
    necessary_params: Optional[List[str]] = None,
) -> Optional[JsonPayload]:
    if necessary_params:
        response_body_dict = {}
        for key in necessary_params:
            value = all_params.get(key)
            _body_dict = await serialize_response(response_content=value)
            response_body_dict.update(_body_dict)
        return JsonPayload(value=response_body_dict, dumps=ujson.dumps)
    return None
