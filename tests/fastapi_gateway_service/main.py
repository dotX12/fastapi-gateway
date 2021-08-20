from typing import List
from fastapi import Depends, FastAPI, APIRouter, Form, File, UploadFile
from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from fastapi_gateway import route
from tests.fastapi_gateway_service.depends import check_api_key
from tests.fastapi_gateway_service.models import ModelCheckPath, ModelCheckPathBody, FooModel, FooList

app = FastAPI(title='API Gateway')
router1 = APIRouter(prefix='/gateway_endpoint')
router2 = APIRouter(tags=['Without service path'])


SERVICE_URL = "http://microservice.localtest.me:8002"


@route(
    request_method=router1.get,
    service_url=SERVICE_URL,
    gateway_path='/path_param/{random_int}',
    service_path='/v1/path_param/{random_int}',
    status_code=status.HTTP_200_OK,
    override_headers=False,
    response_model=ModelCheckPath,
    query_params=['random_int'],
    tags=['Path'],
)
async def check_path_param(
        random_int: int,
        request: Request,
        response: Response
):
    pass


@route(
    request_method=router1.post,
    service_url=SERVICE_URL,
    gateway_path='/path_and_body/{path_int}',
    service_path='/v1/path_and_body/{path_int}',
    status_code=status.HTTP_200_OK,
    query_params=['path_int'],
    body_params=['foomodel'],
    tags=['Path', 'Body'],
)
async def path_param_and_body(
        path_int: int,
        foomodel: FooModel,
        request: Request,
        response: Response
):
    pass


@route(
    request_method=router1.get,
    gateway_path='/list_model',
    service_path='/v1/list_model',
    service_url=SERVICE_URL,
    status_code=status.HTTP_200_OK,
    response_model=List[FooList],
    tags=['List'],
)
async def check_list_model(
        request: Request,
        response: Response
):
    pass


@route(
    request_method=router1.get,
    service_url=SERVICE_URL,
    gateway_path='/query',
    service_path='/v1/query',
    query_params=['query_int', 'query_str'],
    status_code=status.HTTP_400_BAD_REQUEST,
    tags=['Query'],
)
async def query_params(
        query_int: int,
        query_str: str,
        request: Request,
        response: Response
):
    pass


@route(
    request_method=router1.post,
    service_url=SERVICE_URL,
    gateway_path='/query_and_body',
    service_path='/v1/query_and_body',
    query_params=['query_int', 'query_str'],
    body_params=['test_body'],
    status_code=status.HTTP_200_OK,
)
async def check_query_params_and_body(
        query_int: int,
        query_str: str,
        test_body: FooModel,
        request: Request,
        response: Response
):
    pass


@route(
    request_method=router1.post,
    service_url=SERVICE_URL,
    gateway_path='/query_and_body_path/{path}',
    service_path='/v1/query_and_body_path/{path}',
    query_params=['query_int', 'query_str'],
    body_params=['test_body'],
    status_code=status.HTTP_200_OK,
    tags=['Query', 'Body', 'Path'],
)
async def check_query_params_and_body(
        path: int,
        query_int: int,
        query_str: str,
        test_body: FooModel,
        request: Request,
        response: Response
):
    """

    :param path: сообщение
    :param query_int: хуйныя
    :param query_str:
    :param test_body:
    :param request:
    :param response:
    """
    pass


@route(
    request_method=router1.get,
    service_url=SERVICE_URL,
    gateway_path='/check_depends_header',
    service_path='/v1/list_model',
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_api_key)
    ],
    tags=['Dependency']
)
async def check_depends_header(
        request: Request,
        response: Response
):
    pass


@route(
    request_method=router1.post,
    service_url=SERVICE_URL,
    gateway_path='/form_data',
    service_path='/v1/form_data',
    status_code=status.HTTP_200_OK,
    form_params=['username', 'password'],
    tags=['Form'],
)
async def check_form_data(
        request: Request,
        response: Response,
        username: str = Form(...),
        password: str = Form(...),
):
    pass


@route(
    request_method=router1.post,
    service_url=SERVICE_URL,
    gateway_path='/upload_file',
    service_path='/v1/upload_file',
    status_code=status.HTTP_200_OK,
    form_params=['file'],
    tags=['File', 'Form'],
)
async def check_form_data(
        request: Request,
        response: Response,
        file: UploadFile = File(...),
):
    pass


@route(
    request_method=router1.post,
    service_url=SERVICE_URL,
    gateway_path='/form_and_upload_file',
    service_path='/v1/form_and_upload_file',
    status_code=status.HTTP_200_OK,
    form_params=['username', 'password', 'file'],
    tags=['File', 'Form'],
)
async def check_form_data(
        request: Request,
        response: Response,
        username: str = Form(...),
        password: str = Form(...),
        file: UploadFile = File(...),
):
    pass

app.include_router(router1)
app.include_router(router2)
