from starlette.datastructures import MutableHeaders
from typing import Dict, Any


def inheritance_service_headers(
        gateway_headers: MutableHeaders,
        service_headers: MutableHeaders,
) -> Dict[str, Any]:
    forced_gateway_headers = ['server', 'date', 'content-encoding', 'content-type']
    return {
        key: service_headers[key] for key in service_headers
        if key not in gateway_headers and key.lower() not in forced_gateway_headers
    }
