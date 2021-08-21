from typing import List, Union, Any, Dict
from ujson import dumps, loads
from urllib.parse import unquote


def decode_json(data: Union[List, Dict[str, Any]]):
    data_dumps = dumps(data, ensure_ascii=False)
    decoded_data_str = unquote(data_dumps)
    data_data_json = loads(decoded_data_str)
    return data_data_json
