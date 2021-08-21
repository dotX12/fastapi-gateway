from typing import Union, Any, Dict, Optional
from aiohttp import JsonPayload
from fastapi_gateway.utils.form import CustomFormData

T = Union[Dict[str, Any], CustomFormData, JsonPayload]


def create_dict_if_not(data: Optional[T] = None) -> Union[dict, T]:
    if data:
        return data
    return {}
