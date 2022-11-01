from typing import List, Any, Dict, Optional

from fastapi.routing import serialize_response


async def serialize_query_content(key, value) -> dict:
    serialized_data = await serialize_response(response_content=value)
    if isinstance(serialized_data, dict):
        serialized = serialized_data
    else:
        serialized = {key: serialized_data}
    return serialized


async def unzip_query_params(
    all_params: Dict[str, Any],
    necessary_params: Optional[List[str]] = None,
) -> Optional[Dict[str, Any]]:

    if necessary_params:
        response_query_params = {}
        for key in necessary_params:
            value = all_params.get(key)
            serialized_dict = await serialize_query_content(key=key, value=value)
            response_query_params.update(serialized_dict)
        return response_query_params
    return None
