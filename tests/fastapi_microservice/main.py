from fastapi import FastAPI, Form, UploadFile, File, Body, Header
from starlette.requests import Request
from tests.fastapi_microservice.models import ExampleModel

app = FastAPI(title='Microservice #1')


@app.get(
    path='/v1/path_param/{random_int}',
    tags=['Path'],
)
async def path_param(random_int: int):
    return {'foo': 'bar', 'custom_int': random_int}


@app.post(
    path='/v1/path_and_body/{path_int}',
    tags=['Path', 'Body'],
)
async def path_and_body(path_int: int, data: ExampleModel):
    return {'foo': 'bar', 'path_int': path_int, **data.dict()}


@app.get(
    path='/v1/list_model',
    tags=['List'],
)
async def list_model():
    return [{"foo_key": "foo"}, {"foo_key": "bar"}]


@app.post(
    path='/v1/body',
    tags=['Body'],
)
async def body(example_int: int = Body(...), example_str: int = Body(...)):
    return {"query_int": example_int, "query_str": example_str}


@app.get(
    path='/v1/query',
    tags=['Query'],
)
async def query(query_int: int, query_str: str):
    return {"query_int": query_int, "query_str": query_str}


@app.post(
    path='/v1/query_and_body',
    tags=['Query', 'Body'],
)
async def query_and_body(query_int: int, query_str: str, foo_model: ExampleModel):
    return {"query_int": query_int, "query_str": query_str, **foo_model.dict()}


@app.post(
    path='/v1/query_and_body_path/{path}',
    tags=['Query', 'Body', 'Path'],
)
async def query_and_body_path(query_int: int, query_str: str, path: int, foo_model: ExampleModel):
    return {"query_int": query_int, "query_str": query_str, "path": path, **foo_model.dict()}


@app.post(
    '/v1/form_data',
    tags=['Form'],
)
async def form_data(username: str = Form(...), password: str = Form(...)):
    return {"foo": "bar", "username": username, "password": password}


@app.post(
    path='/v1/upload_file',
    tags=['Form', 'File'],
)
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "file_content_type": file.content_type
    }


@app.post(
    path='/v1/form_and_upload_file',
    tags=['Form', 'File'],
)
async def form_and_upload_file(username: str = Form(...), password: str = Form(...), file: UploadFile = File(...)):
    return {"username": username, 'pwd': password, "filename": file.filename, "content_type": file.content_type}


@app.get(
    path='/v1/check_dependency_header'
)
async def check_dependency(request: Request):
    return {'header': request.headers.get('x-api-key'), 'foo': 'bar'}