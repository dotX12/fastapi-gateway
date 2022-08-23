<p align="center">
<img src="https://scrutinizer-ci.com/g/dotX12/fastapi-gateway/badges/quality-score.png?b=master" alt="https://scrutinizer-ci.com/g/dotX12/fastapi-gateway/">
<img src="https://scrutinizer-ci.com/g/dotX12/fastapi-gateway/badges/code-intelligence.svg?b=master" alt="https://scrutinizer-ci.com/g/dotX12/fastapi-gateway/">
<img src="https://scrutinizer-ci.com/g/dotX12/fastapi-gateway/badges/build.png?b=master" alt="https://scrutinizer-ci.com/g/dotX12/fastapi-gateway/">
<img src="https://badge.fury.io/py/fastapi-gateway.svg" alt="https://badge.fury.io/py/fastapi-gateway">
<img src="https://pepy.tech/badge/fastapi-gateway" alt="https://pepy.tech/project/fastapi-gateway">
<img src="https://pepy.tech/badge/fastapi-gateway/month" alt="https://pepy.tech/project/fastapi-gateway">
<img src="https://img.shields.io/github/license/dotX12/fastapi-gateway.svg" alt="https://github.com/dotX12/fastapi-gateway/blob/master/LICENSE">

# ⚙️ fastapi-gateway is async single entry point for microservices.

#### API Gateway performs many tasks: accepts, processes and distributes requests, controls traffic, monitors and controls access and security, caching, throttling.

Initially, this project was created for myself, I needed to implement identification, authentication and authorization. In the future, there was a need to limit requests for each user on every endpoint, create API plans. There were a lot of microservices and to keep in each microservice the logic for limiting endpoints, security logic, logging etc. - meaningless. Therefore, all this functionality is located at a single entry point, which already implements all the necessary tasks with security, limiting, etc., while microservices now directly solve their tasks.

## 💿 Installation

```
pip install fastapi_gateway
```

## ❗️ Benchmark
1.5k - 3k RPC.

```
gitshit@git ~ % wrk -t 4 -c 40 http://gateway.localtest.me:8003/gateway_endpoint/path_param/12
Running 10s test @ http://gateway.localtest.me:8003/gateway_endpoint/path_param/12
  4 threads and 40 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    30.11ms   33.65ms 312.55ms   95.98%
    Req/Sec   395.03    218.80     0.89k    73.21%
  15550 requests in 10.05s, 2.31MB read
Requests/sec:   1547.81
Transfer/sec:    235.81KB
```

## 💻 Example

<details> 
<summary>
<code>Example of use (long code)</code>
</summary>
<br>

```python3
from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from fastapi_gateway import route
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Depends
from fastapi.security import APIKeyHeader
from starlette import status
from starlette.exceptions import HTTPException

app = FastAPI(title='API Gateway')
SERVICE_URL = "http://microservice.localtest.me:8002"

API_KEY_NAME = "x-api-key"

api_key_header = APIKeyHeader(
    name=API_KEY_NAME,
    auto_error=False
)


def check_api_key(key: str = Depends(api_key_header)):
    if key:
        return key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You didn't pass the api key in the header! Header: x-api-key",
    )


class FooModel(BaseModel):
    example_int: int
    example_str: str


@route(
    request_method=app.post,
    service_url=SERVICE_URL,
    gateway_path='/query_and_body_path/{path}',
    service_path='/v1/query_and_body_path/{path}',
    query_params=['query_int', 'query_str'],
    body_params=['test_body'],
    status_code=status.HTTP_200_OK,
    tags=['Query', 'Body', 'Path'],
    dependencies=[
        Depends(check_api_key)
    ],
)
async def check_query_params_and_body(
        path: int, query_int: int, query_str: str,
        test_body: FooModel, request: Request, response: Response
):
    pass
  ```

</details>

#### See more examples here:  
##### [Tests and instructions for launch](../master/tests)  
##### [Souce code Gateway](../master/tests/fastapi_gateway_service)  
##### [Souce code Microservice #1](../master/tests/fastapi_microservice)  

 ## 🪛 How to use?

- **request_method** -  is a callable (like app.get, app.post, foo_router.patch and so on.).  
- **service_url** - the path to the endpoint on another service (like "https://microservice1.example.com").  
- **service_path** - the path to the method in microservice (like "/v1/microservice/users").  
- **gateway_path** - is the path to bind gateway.  
For example, your gateway api is located here - *https://gateway.example.com* and the path to endpoint (**gateway_path**) - "/users" then the full way to this method will be - *https://gateway.example.com/users*
- **override_headers** - Boolean value allows you to return all the headlines that were created by microservice in gateway.  
- **query_params** - used to extract query parameters from endpoint and transmission to microservice
- **form_params** -  used to extract form model parameters from endpoint and transmission to microservice
- **param body_params** - used to extract body model from endpoint and transmission to microservice

⚠️ - **Be sure to transfer the name of the argument to the router, which is in the endpoint func!**  

```
query_params - List[Query]
body_params - List[Body]
form_params - List[File, Form]
 ```

<details> 
<summary>
<code>In more detail how to transmit body, form and query (photo)</code>
</summary>
<br>
<img width="450" height="456" src="https://user-images.githubusercontent.com/64792903/130335866-82be1684-cd54-43d3-8e0e-4013176a352a.jpg">
</details>
